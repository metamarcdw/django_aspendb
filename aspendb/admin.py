import datetime

from django.contrib import admin
from django import forms
from aspendb.models import *

admin.site.site_title = "Aspen Technologies Database"
admin.site.site_header = "Aspen Technologies Database"

def time_in_range(start, end, x):
    # Return true if x is in the range [start, end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def get_current_shift():
    first_start = datetime.time(6, 0, 0)
    first_end = datetime.time(16, 30, 0)
    second_start = datetime.time(16, 30, 0)
    second_end = datetime.time(3, 0, 0)
    now = tz.localize(datetime.datetime.now()).time()
    if time_in_range(first_start, first_end, now):
        return SHIFTS[0][1]
    elif time_in_range(second_start, second_end, now):
        return SHIFTS[1][1]
    else:
        return ""

def get_my_workcell(request):
    if request.user.is_authenticated():
        username = request.user.username
        workcells = Workcell.objects.values_list('name', flat=True)
        if username in workcells:
            return Workcell.objects.get(name=username)

def get_initials(self, request):
    leader = ""
    workcell_name = ""

    my_workcell = get_my_workcell(request)
    if my_workcell:
        shift = get_current_shift()
        if shift == "1st":
            leader = my_workcell.cell_leader_1st
        elif shift == "2nd":
            leader = my_workcell.cell_leader_2nd
        workcell_name = my_workcell.name

    return {'employee': leader, 'created_by': leader,
            'workcell': workcell_name}

def get_initials_eos(self, request):
    initials = get_initials(self, request)
    shift = get_current_shift()
    schedules = ProductionSchedule.objects.filter(
        date=get_today()).filter(
        shift=shift).filter(
        workcell=initials["workcell"])
    total = sum(schedules.values_list('total_shots', flat=True))
    initials["scheduled_shots"] = total
    return initials

def get_radio_formfield(label, choices, initial=None):
    return forms.ChoiceField(label=label, choices=choices,
        initial=initial, widget=forms.widgets.RadioSelect())


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    training_level = get_radio_formfield(None, ONETOFIVE)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ("first_name", "last_name", "shift", "email")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")

class WorkcellAdmin(admin.ModelAdmin):
    list_display = ("name", "foam_system", "turns_per_hour")
    ordering = ("name",)

class PartAdmin(admin.ModelAdmin):
    list_display = ("part_number", "program_name")

    def program_name(self, obj):
        return obj.program.name

class ProductionScheduleForm(forms.ModelForm):
    class Meta:
        model = ProductionSchedule
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
class ProductionScheduleAdmin(admin.ModelAdmin):
    form = ProductionScheduleForm
    exclude = ("total_shots",)
    list_display = ("part", "shots", "date", "shift", "workcell")
    list_filter = ("date", "shift", "workcell")
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")


class StartOfShiftForm(forms.ModelForm):
    class Meta:
        model = StartOfShift
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    process_verified = get_radio_formfield(
        "Process parameters verified?", YESNONA[:2])
    weights_verified = get_radio_formfield(
        "Shot weights verified?", YESNONA[:2])
    adequate_components = get_radio_formfield(
        "Is there an adequate supply of components?", YESNONA)
    airhose_secure = get_radio_formfield(
        "Are all air hose nozzles secure?", YESNONA)
    poly_agitator = get_radio_formfield(
        "Is poly agitator functioning?", YESNONA[:2])
    chemical_tracked = get_radio_formfield(
        "Is poly/iso recorded in lot tracking book?", YESNONA)
    stands_labels = get_radio_formfield(
        "Are all pack stands/pack instructions " + \
        "& barcode labels in place?", YESNONA[:2])
    new_product = get_radio_formfield(
        "Are there any NEW production parts " + \
        "scheduled to run today?", YESNONA[:2])
    opposite_parts = get_radio_formfield(
        "Are the NEW parts - symetrically opposite " + \
        "parts on the same turntable?", YESNONA[:2])

class StartOfShiftAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials
    form = StartOfShiftForm
    list_display = ("date", "shift", "workcell")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift")


class EndOfShiftForm(forms.ModelForm):
    class Meta:
        model = EndOfShift
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    spray_pots = get_radio_formfield(
        "Is your spray pot topped off?", YESNONA)
    adequate_poly = get_radio_formfield(
        "Is there an adequate supply of poly?", YESNONA[:2])
    adequate_iso = get_radio_formfield(
        "Is there an adequate supply of iso?", YESNONA[:2])
    replacement_poly = get_radio_formfield(
        "Is replacement poly agitating?", YESNONA)
    scrap_labeled = get_radio_formfield(
        "Is all scrap properly labeled?", YESNONA[:2])
    cabinet_stocked = get_radio_formfield(
        "Are all supplies in cell leader cabinet stocked?", YESNONA)
    pot_grounded = get_radio_formfield(
        "Is spray pot ground connected?", YESNONA)

class EndOfShiftAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials_eos
    form = EndOfShiftForm
    exclude = ("total_shots", "oee", "scrap_percent")
    list_display = (
        "date", "shift", "workcell", "_oee", "_scrap_percent")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift")

    def _oee(self, obj):
        return "{}%".format(obj.oee)

    def _scrap_percent(self, obj):
        return "{}%".format(obj.scrap_percent)


class ScrapReportForm(forms.ModelForm):
    class Meta:
        model = ScrapReport
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
class ScrapReportAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials
    form = ScrapReportForm
    exclude = ("bad_mix", "dents", "mold_release", "non_fill",
                "collapse", "tears", "trim", "voilds", "open_voilds",
                "under_weight", "over_weight", "swollen",
                "contamination", "total_scrap")
    list_display = ("part", "date", "shift", "workcell", "total_scrap")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class LaborAllocationReportForm(forms.ModelForm):
    class Meta:
        model = LaborAllocationReport
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    period = get_radio_formfield(None, ONETOFIVE)
class LaborAllocationReportAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials
    form = LaborAllocationReportForm
    list_display = ("date", "shift", "workcell", "period")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class DowntimeForm(forms.ModelForm):
    class Meta:
        model = Downtime
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
class DowntimeAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials
    form = DowntimeForm
    list_display = ("date", "shift", "workcell", "code")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class SpotCheckReportForm(forms.ModelForm):
    class Meta:
        model = SpotCheckReport
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
class SpotCheckReportAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials
    form = SpotCheckReportForm
    list_display = ("date", "shift", "workcell", "part")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = "__all__"
    parts_used = get_radio_formfield(None, YESNONA[:2])
    parts_reordered = get_radio_formfield(None, YESNONA)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    form = MaintenanceRecordForm
    list_display = ("date_performed", "problem_code", "work_done")
    list_filter = ("date_performed", "problem_code")
    date_hierarchy = "date_performed"
    ordering = ("date_performed", "problem_code")

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    urgency = get_radio_formfield(None, ONETOFIVE)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials
    form = MaintenanceRequestForm
    list_display = ("date", "shift", "problem", "status")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date",)

# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Workcell, WorkcellAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(DowntimeCode)
admin.site.register(ProductionSchedule, ProductionScheduleAdmin)
admin.site.register(StartOfShift, StartOfShiftAdmin)
admin.site.register(EndOfShift, EndOfShiftAdmin)
admin.site.register(ScrapReport, ScrapReportAdmin)
admin.site.register(LaborAllocationReport, LaborAllocationReportAdmin)
admin.site.register(Downtime, DowntimeAdmin)
admin.site.register(SpotCheckReport, SpotCheckReportAdmin)
admin.site.register(MaintenanceRecord, MaintenanceRecordAdmin)
admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)

