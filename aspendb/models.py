import datetime

from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from smart_selects.db_fields import ChainedForeignKey


SHIFTS = (  ("1st", "1st"),
            ("2nd", "2nd"))

class Employee(models.Model):
    class Meta:
        unique_together = ("first_name", "last_name")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    shift = models.CharField(max_length=3, choices=SHIFTS)
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

def nospace_validator(value):
    if " " in value:
        raise forms.ValidationError(
            "The workcell name cannot contain spaces.")

class Workcell(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[nospace_validator],
        primary_key=True)
    foam_system = models.CharField(max_length=30)
    turns_per_hour = models.DecimalField(
        max_digits=4, decimal_places=2, default=10)
    cell_leader_1st = models.ForeignKey(
        Employee, related_name="cell_leader_1st", blank=True, null=True)
    cell_leader_2nd = models.ForeignKey(
        Employee, related_name="cell_leader_2nd", blank=True, null=True)

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

def date_validator(value):
    if value > datetime.date.today():
        raise forms.ValidationError("The date cannot be in the future!")

class ProductionSchedule(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell", "part")

    workcell = models.ForeignKey(Workcell)
    date = models.DateField(validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    part = ChainedForeignKey(Part,
        chained_field="workcell",
        chained_model_field="workcell")

    hours = models.DecimalField(max_digits=4, decimal_places=2, default=10)
    shots = models.IntegerField(
	validators=[MinValueValidator(1)], verbose_name="Shots per round")
    total_shots = models.IntegerField()

    def get_total_shots(self):
        return int(self.shots * self.workcell.turns_per_hour * self.hours)

    def save(self, *args, **kwargs):
        self.total_shots = self.get_total_shots()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(
            self.part.part_number, self.shots)

class StartOfShift(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell")

    workcell = models.ForeignKey(Workcell)
    date = models.DateField(validators=[date_validator])
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
    date = models.DateField(validators=[date_validator])
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
    oee = models.DecimalField(max_digits=5, decimal_places=2)
    scrap_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def get_total_shots(self):
        return self.ending_shot - self.starting_shot

    def get_oee(self):
        return (self.total_shots / self.scheduled_shots) * 100

    def get_scrap_percent(self):
        return (self.total_scrap / self.total_shots) * 100

    def save(self, *args, **kwargs):
        self.total_shots = self.get_total_shots()
        self.oee = self.get_oee()
        self.scrap_percent = self.get_scrap_percent()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class ScrapReport(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell", "part")

    workcell = models.ForeignKey(Workcell)
    date = models.DateField(validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    employee = models.ForeignKey(Employee)
    part = ChainedForeignKey(Part,
        chained_field="workcell",
        chained_model_field="workcell")

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
    date = models.DateField(validators=[date_validator])
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
MAINT_CODES = ( ("mech", "Mechanical"),
                ("elec", "Electrical"),
                ("pneu", "Pneumatic"),
                ("hydr", "Hydraulic"),
                ("water", "Water"),
                ("struc", "Structural"),
                ("chem", "Chemical"))

class MaintenanceRecord(models.Model):
    date = models.DateField(
        validators=[date_validator],
        verbose_name="Date performed")
    employee = models.ForeignKey(
        Employee, verbose_name="Work performed by")

    problem_code = models.CharField(max_length=5, choices=MAINT_CODES)
    work_done = models.CharField(max_length=50, blank=True)
    repair_time = models.IntegerField(validators=[MinValueValidator(0)])
    workcell_downtime = models.IntegerField(
        validators=[MinValueValidator(0)])

    parts_used = models.CharField(max_length=3, choices=YESNONA[:2])
    parts_reordered = models.CharField(max_length=3, choices=YESNONA)
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{}, {}: {}".format(
            self.date, self.problem_code, self.work_done)

class MaintenanceRequest(models.Model):
    workcell = models.ForeignKey(Workcell, blank=True, null=True)
    date = models.DateField(validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    created_by = models.ForeignKey(Employee, related_name="created_by")

    approved_by = models.ForeignKey(Employee, related_name="approved_by")
    department = models.ForeignKey(Department)
    problem = models.CharField(max_length=100)
    urgency = models.IntegerField(choices=URGENCY)

    record = models.ForeignKey(MaintenanceRecord, blank=True, null=True)
    status = models.CharField(max_length=30,
        choices=STATUS, default=STATUS[0][0])

    def __str_(self):
        return "{}, {}: {}".format(
            self.date, self.workcell.name, self.problem)


