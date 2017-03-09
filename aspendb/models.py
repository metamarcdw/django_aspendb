from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Employee(models.Model):
    class Meta:
        unique_together = ("first_name", "last_name")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    training_level = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Department(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name

class Workcell(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    foam_system = models.CharField(max_length=30)
    cell_leader_1st = models.ForeignKey(
        Employee, related_name="cell_leader_1st")
    cell_leader_2nd = models.ForeignKey(
        Employee, related_name="cell_leader_2nd")

    def __str__(self):
        return self.name

class Part(models.Model):
    part_number = models.CharField(max_length=30, primary_key=True)
    program = models.ForeignKey(Program)
    workcell = models.ForeignKey(Workcell)

    def __str__(self):
        return "{}".format(self.part_number)

class DowntimeCode(models.Model):
    code = models.IntegerField(
        validators=[MaxValueValidator(518), MinValueValidator(101)],
        primary_key=True)
    description = models.CharField(max_length=30)

    def __str__(self):
        return "{}: {}".format(self.code, self.description)

YESNONA = ( ('yes', 'Yes'),
            ('no', 'No'),
            ('na', 'N/A'))
SHIFTS = (  ("1st", "1st"),
            ("2nd", "2nd"))

class StartOfShift(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell")

    workcell = models.ForeignKey(Workcell)
    date = models.DateField()
    shift = models.CharField(max_length=3, choices=SHIFTS)
    employee = models.ForeignKey(Employee)

    process_verified = models.CharField(
        verbose_name="Process parameters verified?",
        max_length=3, choices=YESNONA[:2])
    weights_verified = models.CharField(
        verbose_name="Shot weights verified?",
        max_length=3, choices=YESNONA[:2])

    mix_ratio = models.FloatField(
        validators=[MaxValueValidator(2), MinValueValidator(0)])
    poly_temp = models.FloatField(
        validators=[MaxValueValidator(90), MinValueValidator(60)])
    iso_temp = models.FloatField(
        validators=[MaxValueValidator(90), MinValueValidator(60)])
    poly_flow = models.FloatField(
        validators=[MaxValueValidator(200), MinValueValidator(20)])
    iso_flow = models.FloatField(
        validators=[MaxValueValidator(200), MinValueValidator(20)])
    poly_pressure = models.IntegerField(
        validators=[MaxValueValidator(2500), MinValueValidator(500)])
    iso_pressure = models.IntegerField(
        validators=[MaxValueValidator(2500), MinValueValidator(500)])

    adequate_components = models.CharField(
        verbose_name="Is there an adequate supply of components?",
        max_length=3, choices=YESNONA)
    airhose_secure = models.CharField(
        verbose_name="Are all air hose nozzles secure?",
        max_length=3, choices=YESNONA)
    poly_agitator = models.CharField(
        verbose_name="Is poly agitator functioning?",
        max_length=3, choices=YESNONA[:2])
    chemical_tracked = models.CharField(
        verbose_name="Is poly/iso recorded in lot tracking book?",
        max_length=3, choices=YESNONA)

    poly_date = models.DateField()
    iso_date = models.DateField()

    stands_labels = models.CharField(
        verbose_name="Are all pack stands/pack instructions " + \
            "& barcode labels in place?",
        max_length=3, choices=YESNONA[:2])
    new_product = models.CharField(
        verbose_name="Are there any NEW production parts " + \
            "scheduled to run today?",
        max_length=3, choices=YESNONA[:2])
    opposite_parts = models.CharField(
        verbose_name="Are the NEW parts - symetrically opposite " + \
            "parts on the same turntable?",
        max_length=3, choices=YESNONA[:2])

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class EndOfShift(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell")

    workcell = models.ForeignKey(Workcell)
    date = models.DateField()
    shift = models.CharField(max_length=3, choices=SHIFTS)
    employee = models.ForeignKey(Employee)

    starting_shot = models.IntegerField(validators=[MinValueValidator(0)])
    ending_shot = models.IntegerField(validators=[MinValueValidator(1)])
    scheduled_shots = models.IntegerField(validators=[MinValueValidator(1)])
    missed_shots = models.IntegerField(validators=[MinValueValidator(0)])
    total_scrap = models.IntegerField(validators=[MinValueValidator(0)])

    spray_pots = models.CharField(
        verbose_name="Is your spray pot topped off?",
        max_length=3, choices=YESNONA)
    adequate_poly = models.CharField(
        verbose_name="Is there an adequate supply of poly?",
        max_length=3, choices=YESNONA[:2])
    adequate_iso = models.CharField(
        verbose_name="Is there an adequate supply of iso?",
        max_length=3, choices=YESNONA[:2])
    replacement_poly = models.CharField(
        verbose_name="Is replacement poly agitating?",
        max_length=3, choices=YESNONA)
    scrap_labeled = models.CharField(
        verbose_name="Is all scrap properly labeled?",
        max_length=3, choices=YESNONA[:2])
    cabinet_stocked = models.CharField(
        verbose_name="Are all supplies in cell leader cabinet stocked?",
        max_length=3, choices=YESNONA)
    pot_grounded = models.CharField(
        verbose_name="Is spray pot ground connected?",
        max_length=3, choices=YESNONA)
    comments = models.CharField(max_length=500, blank=True)

    total_shots = models.IntegerField()
    oee = models.FloatField()

    def get_total_shots(self):
        return self.ending_shot - self.starting_shot

    def get_oee(self):
        return (self.total_shots / self.scheduled_shots) * 100

    def save(self, *args, **kwargs):
        self.total_shots = self.get_total_shots()
        self.oee = self.get_oee()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class ScrapReport(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell", "part")

    workcell = models.ForeignKey(Workcell)
    date = models.DateField()
    shift = models.CharField(max_length=3, choices=SHIFTS)
    employee = models.ForeignKey(Employee)
    part = models.ForeignKey(Part)

    bad_mix = models.IntegerField(validators=[MinValueValidator(0)])
    non_fill = models.IntegerField(validators=[MinValueValidator(0)])
    collapse = models.IntegerField(validators=[MinValueValidator(0)])
    tears = models.IntegerField(validators=[MinValueValidator(0)])
    trim = models.IntegerField(validators=[MinValueValidator(0)])
    voilds = models.IntegerField(validators=[MinValueValidator(0)])
    open_voilds = models.IntegerField(validators=[MinValueValidator(0)])
    under_weight = models.IntegerField(validators=[MinValueValidator(0)])
    over_weight = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return "{}, {}, {}: {}".format(
            self.date, self.shift,
            self.workcell.name, self.part.part_number)

class Downtime(models.Model):
    workcell = models.ForeignKey(Workcell)
    date = models.DateField()
    shift = models.CharField(max_length=3, choices=SHIFTS)
    employee = models.ForeignKey(Employee)

    minutes = models.IntegerField(validators=[MinValueValidator(1)])
    code = models.ForeignKey(DowntimeCode)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

URGENCY = ( (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"))
STATUS = (  ("open", "Open"),
            ("completed", "Completed"))

class MaintenanceRequest(models.Model):
    workcell = models.ForeignKey(Workcell)
    date = models.DateField()
    shift = models.CharField(max_length=3, choices=SHIFTS)
    created_by = models.ForeignKey(Employee, related_name="created_by")

    department = models.ForeignKey(Department)
    problem = models.CharField(max_length=100)
    urgency = models.IntegerField(choices=URGENCY)
    approved_by = models.ForeignKey(Employee, related_name="approved_by")
    status = models.CharField(max_length=30, choices=STATUS)

    def __str_(self):
        return "{}, {}: {}".format(
            self.date, self.workcell.name, self.problem)

