import re
import smtplib
import datetime, pytz

from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from smart_selects.db_fields import ChainedForeignKey


tz = pytz.timezone("America/Chicago")

SHIFTS = (  ("1st", "1st"),
            ("2nd", "2nd"))
ONETOFIVE = ((1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"))

FIRST_START = datetime.time(6, 0, 0)
FIRST_END = datetime.time(16, 30, 0)
SECOND_START = datetime.time(16, 30, 0)
SECOND_END = datetime.time(3, 0, 0)
LUNCH_FIRST_START = datetime.time(12, 0, 0)
LUNCH_FIRST_END = datetime.time(12, 30, 0)
LUNCH_SECOND_START = datetime.time(21, 0, 0)
LUNCH_SECOND_END = datetime.time(21, 30, 0)

def time_in_range(start, end, x):
    # Return true if x is in the range [start, end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def get_current_shift():
    override = TimeOverride.objects.get(pk=1)
    if override.overrides_enabled == YESNO[0][0]:
        return SHIFTS[0][1] if override.shift == SHIFTS[0][0] else SHIFTS[1][1]

    now = tz.localize(datetime.datetime.now()).time()
    if time_in_range(FIRST_START, FIRST_END, now):
        return SHIFTS[0][1]
    elif time_in_range(SECOND_START, SECOND_END, now):
        return SHIFTS[1][1]
    else:
        return ""

def get_today():
    override = TimeOverride.objects.get(pk=1)
    if override.overrides_enabled == YESNO[0][0]:
        return override.date

    return tz.localize(datetime.datetime.now()).date()

def date_validator(value):
    if value > get_today():
        raise forms.ValidationError("The date cannot be in the future!")

class Employee(models.Model):
    class Meta:
        unique_together = ("first_name", "last_name")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    hire_date = models.DateField(
        default=get_today, validators=[date_validator])
    email = models.EmailField(blank=True)
    shift = models.CharField(max_length=3, choices=SHIFTS)
    training_level = models.IntegerField(choices=ONETOFIVE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Department(models.Model):
    name = models.CharField(max_length=30)
    representative_1st = models.ForeignKey(
        Employee, related_name="representative_1st", blank=True, null=True)
    representative_2nd = models.ForeignKey(
        Employee, related_name="representative_2nd", blank=True, null=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

def nospace_validator(value):
    if " " in value:
        raise forms.ValidationError(
            "The workcell name cannot contain spaces.")

class Workcell(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[nospace_validator])
    foam_system = models.CharField(max_length=30)
    table_time_minutes = models.IntegerField(default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)])
    table_time_seconds = models.IntegerField(default=0,
        validators=[MaxValueValidator(60), MinValueValidator(0)])
    turns_per_hour = models.DecimalField(blank=True, max_digits=4, decimal_places=2)
    cell_leader_1st = models.ForeignKey(
        Employee, related_name="cell_leader_1st", blank=True, null=True)
    cell_leader_2nd = models.ForeignKey(
        Employee, related_name="cell_leader_2nd", blank=True, null=True)

    def get_tph(self):
        minutes = self.table_time_minutes + (self.table_time_seconds / 60)
        if minutes:
            return 60 / minutes
        else:
            return 0

    def save(self, *args, **kwargs):
        if not self.turns_per_hour:
            self.turns_per_hour = self.get_tph()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Part(models.Model):
    part_number = models.CharField(max_length=30)
    program = models.ForeignKey(Program)
    workcell = models.ForeignKey(Workcell)

    def __str__(self):
        return "{}".format(self.part_number)

class DowntimeCode(models.Model):
    code = models.IntegerField(
        validators=[MaxValueValidator(518), MinValueValidator(101)])
    description = models.CharField(max_length=30)

    def __str__(self):
        return "{}: {}".format(self.code, self.description)

YESNONA = ( ('yes', 'Yes'),
            ('no', 'No'),
            ('na', 'N/A'))
YESNO = YESNONA[:2]

class ProductionSchedule(models.Model):
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    part = ChainedForeignKey(Part,
        chained_field="workcell",
        chained_model_field="workcell")

    hours = models.DecimalField(max_digits=4, decimal_places=2, default=9.33)
    shots = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name="Shots per round")
    total_shots = models.IntegerField()

    def get_total_shots(self):
        return int(round(
            self.shots * self.workcell.turns_per_hour * self.hours))

    def save(self, *args, **kwargs):
        self.total_shots = self.get_total_shots()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(
            self.part.part_number, self.shots)

class StartOfShift(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell")

    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    process_verified = models.CharField(max_length=3, choices=YESNO)
    weights_verified = models.CharField(max_length=3, choices=YESNO)

    starting_shot = models.IntegerField(validators=[MinValueValidator(0)])
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
        validators=[MaxValueValidator(2500), MinValueValidator(50)])
    iso_pressure = models.IntegerField(
        validators=[MaxValueValidator(2500), MinValueValidator(50)])

    adequate_components = models.CharField(max_length=3, choices=YESNONA)
    airhose_secure = models.CharField(max_length=3, choices=YESNONA)
    poly_agitator = models.CharField(max_length=3, choices=YESNO)
    chemical_tracked = models.CharField(max_length=3, choices=YESNONA)

    poly_date = models.DateField()
    iso_date = models.DateField()

    stands_labels = models.CharField(max_length=3, choices=YESNO)
    new_product = models.CharField(max_length=3, choices=YESNO)
    opposite_parts = models.CharField(max_length=3, choices=YESNO)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class EndOfShift(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell")

    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    ending_shot = models.IntegerField(validators=[MinValueValidator(1)])
    scheduled_shots = models.IntegerField(validators=[MinValueValidator(1)])
    missed_shots = models.IntegerField(validators=[MinValueValidator(0)])
    total_scrap = models.IntegerField(validators=[MinValueValidator(0)])

    spray_pots = models.CharField(max_length=3, choices=YESNONA)
    adequate_poly = models.CharField(max_length=3, choices=YESNO)
    adequate_iso = models.CharField(max_length=3, choices=YESNO)
    replacement_poly = models.CharField(max_length=3, choices=YESNONA)
    scrap_labeled = models.CharField(max_length=3, choices=YESNO)
    cabinet_stocked = models.CharField(max_length=3, choices=YESNONA)
    pot_grounded = models.CharField(max_length=3, choices=YESNONA)
    total_manhrs = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.1)])
    comments = models.TextField(max_length=1000, blank=True)

    total_shots = models.IntegerField()
    oee = models.DecimalField(max_digits=5, decimal_places=2)
    scrap_percent = models.DecimalField(max_digits=5, decimal_places=2)
    labor_per_pc = models.DecimalField(max_digits=5, decimal_places=4)

    def get_total_shots(self):
        sos = StartOfShift.objects.filter(
            date=self.date).filter(
            shift=self.shift).filter(
            workcell=self.workcell)
        if not sos:
            raise Exception("No StartOfShift entry recorded for this workcell.")
        return self.ending_shot - sos[0].starting_shot

    def get_oee(self):
        return (self.total_shots / self.scheduled_shots) * 100

    def get_scrap_percent(self):
        return (self.total_scrap / self.total_shots) * 100

    def get_labor_per_pc(self):
        return self.total_manhrs / (self.total_shots - self.total_scrap)

    def save(self, *args, **kwargs):
        self.total_shots = self.get_total_shots()
        self.oee = self.get_oee()
        self.scrap_percent = self.get_scrap_percent()
        self.labor_per_pc = self.get_labor_per_pc()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class ScrapReport(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell", "part")

    def scrap_numbers_validator(value):
        d = ScrapReport.scrap_dict(value)
        for key, value in d.items():
            u_key = key.replace(" ", "_")
            if not hasattr(ScrapReport, u_key):
                raise forms.ValidationError(
                    "There is no defect called '{0}'!".format(key))

    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    part = ChainedForeignKey(Part,
        chained_field="workcell",
        chained_model_field="workcell")

    bad_mix = models.IntegerField(default=0)
    dents = models.IntegerField(default=0)
    mold_release = models.IntegerField(default=0)
    non_fill = models.IntegerField(default=0)
    collapse = models.IntegerField(default=0)
    tears = models.IntegerField(default=0)
    trim = models.IntegerField(default=0)
    voilds = models.IntegerField(default=0)
    open_voilds = models.IntegerField(default=0)
    under_weight = models.IntegerField(default=0)
    over_weight = models.IntegerField(default=0)
    swollen = models.IntegerField(default=0)
    contamination = models.IntegerField(default=0)

    total_scrap = models.IntegerField()
    numbers = models.TextField(
        max_length = 1000,  validators=[scrap_numbers_validator])

    @staticmethod
    def scrap_dict(txt):
        d = dict()
        for line in txt.split("\n"):
            s, i = re.split(': |:|; |;|, |,', line)
            d[s.strip()] = int(i.strip())
        return d

    def save_scrap_numbers(self):
        d = ScrapReport.scrap_dict(self.numbers)
        for key, value in d.items():
            key = key.replace(" ", "_")
            setattr(self, key, value)
        self.total_scrap = sum(d.values())

    def save(self, *args, **kwargs):
        self.save_scrap_numbers()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}, {}, {}: {}".format(
            self.date, self.shift,
            self.workcell.name, self.part.part_number)

class LaborReport(models.Model):
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    name = models.CharField(max_length=30)
    start_time = models.TimeField()
    end_time = models.TimeField()
    man_hours = models.DecimalField(max_digits=10, decimal_places=2)

    def get_manhrs(self):
        start_time = datetime.datetime.combine(self.date,  self.start_time)
        end_time = datetime.datetime.combine(self.date,  self.end_time)
        lunch_2nd_end = datetime.datetime.combine(self.date, LUNCH_SECOND_END)

        if start_time > end_time:
            end_time += datetime.timedelta(days=1)
        delta = end_time - start_time
        man_hours = (delta.total_seconds() / 3600)

        if self.shift == "1st":
            if self.start_time <= LUNCH_FIRST_START and \
                    self.end_time >= LUNCH_FIRST_END:
                man_hours -= 0.5
        elif self.shift == "2nd":
            if self.start_time <= LUNCH_SECOND_START and \
                    end_time >= lunch_2nd_end:  # Use date-aware objects,
                man_hours -= 0.5   # because 2nd shift ends (before) lunch
        return man_hours

    def save(self, *args, **kwargs):
        self.man_hours = self.get_manhrs()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}, {}, {}: {}".format(
            self.date, self.shift,
            self.workcell.name, self.name)

class LaborAllocationReport(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell", "period")

    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    period = models.IntegerField(choices=ONETOFIVE)
    shooter = models.CharField(max_length=30)
    puller = models.CharField(max_length=30)
    sprayer = models.CharField(max_length=30)

    def __str__(self):
        return "{}, {}, {}: {}".format(
            self.date, self.shift,
            self.workcell.name, self.period)

class Downtime(models.Model):
    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    minutes = models.IntegerField(validators=[MinValueValidator(1)])
    code = models.ForeignKey(DowntimeCode)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class SpotCheckReport(models.Model):
    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    part = ChainedForeignKey(Part,
        chained_field="workcell",
        chained_model_field="workcell")

    timestamp = models.TimeField(auto_now=True)
    qty_checked = models.IntegerField(validators=[MinValueValidator(0)])
    defects = models.CharField(max_length=50)
    packer_initials = models.CharField(max_length=15)
    comments = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return "{}, {}, {}: {}".format(
            self.date, self.shift,
            self.workcell.name, self.part.part_number)

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
    employee = models.ForeignKey(
        Employee, verbose_name="Work performed by")
    date_performed = models.DateField(
        default=get_today, validators=[date_validator])

    problem_code = models.CharField(max_length=5, choices=MAINT_CODES)
    work_done = models.CharField(max_length=50, blank=True)
    repair_time = models.IntegerField(validators=[MinValueValidator(0)])
    workcell_downtime = models.IntegerField(
        validators=[MinValueValidator(0)])

    parts_used = models.CharField(max_length=3, choices=YESNO)
    parts_reordered = models.CharField(max_length=3, choices=YESNONA)
    parts_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "{}, {}: {}".format(
            self.date_performed, self.problem_code, self.work_done)

class MaintenanceRequest(models.Model):
    created_by = models.ForeignKey(Employee, related_name="created_by")
    workcell = models.ForeignKey(Workcell, blank=True, null=True)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    approved_by = models.ForeignKey(Employee, related_name="approved_by")
    department = models.ForeignKey(Department)
    problem = models.CharField(max_length=100)
    urgency = models.IntegerField(choices=ONETOFIVE)

    record = models.ForeignKey(MaintenanceRecord, blank=True, null=True)
    status = models.CharField(max_length=30,
        choices=STATUS, default=STATUS[0][0])

    def send_maintenance_request_emails(self):
        if self.status != STATUS[0][0]:
            return

        email_list = ["krichardson@aspen-tech.net",
                        "jkendrick@aspen-tech.net"]

        gmail_user = "aspendb.sendmail"
        gmail_password = "Aspen123"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)

        rep = None
        maint_dept = Department.objects.get(name="Maintenance")
        shift = get_current_shift()
        if shift == "1st":
            rep = maint_dept.representative_1st
        elif shift == "2nd":
            rep = maint_dept.representative_2nd
        if rep:
            email_list.append(rep.email)

        url = "http://192.168.1.200/admin/aspendb/maintenancerequest/"
        msg = "".join(["\nThere has been a maintenance request:\n",
            url, str(self.id), "/change/"])

        for email in email_list:
            server.sendmail("".join(gmail_user, "@gmail.com"), email, msg)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
#        self.send_maintenance_request_emails()

    def __str_(self):
        return "{}, {}: {}".format(
            self.date, self.workcell.name, self.problem)

class ProcessActivityReport(models.Model):
    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)
    part = ChainedForeignKey(Part,
        chained_field="workcell",
        chained_model_field="workcell",
        blank=True, null=True)

    timestamp = models.TimeField(auto_now=True)
    defect = models.CharField(max_length=20, blank=True)
    process_change = models.CharField(max_length=50)
    effect = models.IntegerField(choices=ONETOFIVE)
    change_reverted = models.CharField(max_length=3, choices=YESNO)
    comments = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return "{}, {}, {}: {}".format(
            self.date, self.shift,
            self.workcell.name, self.defect)

class LayeredProcessAudit(models.Model):
    class Meta:
        unique_together = ("date", "shift", "workcell")

    employee = models.ForeignKey(Employee)
    workcell = models.ForeignKey(Workcell)
    date = models.DateField(
        default=get_today, validators=[date_validator])
    shift = models.CharField(max_length=3, choices=SHIFTS)

    verified_parameters = models.CharField(max_length=3, choices=YESNONA)
    weight_inspection = models.CharField(max_length=3, choices=YESNONA)
    chemicals_tracked = models.CharField(max_length=3, choices=YESNONA)
    components_tracked = models.CharField(max_length=3, choices=YESNONA)

    setup_posted = models.CharField(max_length=3, choices=YESNONA)
    chemicals_correct = models.CharField(max_length=3, choices=YESNONA)
    event_missed_shot = models.CharField(max_length=3, choices=YESNONA)

    demold_criteria = models.CharField(max_length=3, choices=YESNONA)
    demold_ncm = models.CharField(max_length=3, choices=YESNONA)
    mold_release = models.CharField(max_length=3, choices=YESNONA)

    work_instructions = models.CharField(max_length=3, choices=YESNONA)
    proper_equipment = models.CharField(max_length=3, choices=YESNONA)
    trim_criteria = models.CharField(max_length=3, choices=YESNONA)
    inspecting_prior = models.CharField(max_length=3, choices=YESNONA)
    trim_dcm = models.CharField(max_length=3, choices=YESNONA)
    quality_alerts = models.CharField(max_length=3, choices=YESNONA)
    boxes_marked = models.CharField(max_length=3, choices=YESNONA)
    pack_criteria = models.CharField(max_length=3, choices=YESNONA)
    labels_match = models.CharField(max_length=3, choices=YESNONA)
    fifo_product = models.CharField(max_length=3, choices=YESNONA)
    product_tracked = models.CharField(max_length=3, choices=YESNONA)

    ppe = models.CharField(max_length=3, choices=YESNO)
    ppe_info = models.CharField(max_length=3, choices=YESNO)
    sds = models.CharField(max_length=3, choices=YESNO)
    iso_exposure = models.CharField(max_length=3, choices=YESNO)
    comments = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return "{}, {}, {}".format(
            self.date, self.shift, self.workcell.name)

class TimeOverride(models.Model):
    overrides_enabled = models.CharField(max_length=3, choices=YESNO)
    shift = models.CharField(max_length=3, choices=SHIFTS)
    date = models.DateField(default=get_today)

