from django.contrib import admin
from django import forms
from aspendb.models import *

admin.site.site_title = "Aspen Technologies Database"
admin.site.site_header = "Aspen Technologies Database"

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
    today = get_today()
    shift = get_current_shift()
    initials = get_initials(self, request)

    schedules = ProductionSchedule.objects.filter(
        date=today).filter(
        shift=shift).filter(
        workcell=initials["workcell"])
    total_shots = sum(schedules.values_list('total_shots', flat=True))
    initials["scheduled_shots"] = total_shots

    scrap_reports = ScrapReport.objects.filter(
        date=today).filter(
        shift=shift).filter(
        workcell=initials["workcell"])
    total_scrap = sum(scrap_reports.values_list('total_scrap', flat=True))
    initials["total_scrap"] = total_scrap

    labor_reports = LaborReport.objects.filter(
        date=today).filter(
        shift=shift).filter(
        workcell=initials["workcell"])
    total_manhrs = sum(labor_reports.values_list('man_hours', flat=True))
    initials["total_manhrs"] = total_manhrs

    return initials

def get_initials_lr(self, request):
    shift = get_current_shift()
    initials = get_initials(self, request)
    if shift == "1st":
        initials["start_time"] = FIRST_START
        initials["end_time"] = FIRST_END
    elif shift == "2nd":
        initials["start_time"] = SECOND_START
        initials["end_time"] = SECOND_END
    return initials

def get_radio_formfield(label, choices, initial=None):
    return forms.ChoiceField(label=label, choices=choices,
        initial=initial, widget=forms.widgets.RadioSelect())

def get_integer_formfield(initial=None):
    return forms.IntegerField(initial=initial, localize=False)


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
    shots = get_integer_formfield()
class ProductionScheduleAdmin(admin.ModelAdmin):
    form = ProductionScheduleForm
    exclude = ("total_shots",)
    list_display = ("part", "shots", "date", "shift", "workcell")
    list_filter = ("date", "shift", "workcell")
    date_hierarchy = "date"
    ordering = ("-date", "shift", "workcell")


class StartOfShiftForm(forms.ModelForm):
    class Meta:
        model = StartOfShift
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    starting_shot = get_integer_formfield(initial=0)
    poly_pressure = get_integer_formfield()
    iso_pressure = get_integer_formfield()
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
    ordering = ("-date", "shift")


class EndOfShiftForm(forms.ModelForm):
    class Meta:
        model = EndOfShift
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    ending_shot = get_integer_formfield()
    scheduled_shots = get_integer_formfield()
    missed_shots = get_integer_formfield()
    total_scrap = get_integer_formfield()
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
    ordering = ("-date", "shift")

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
    ordering = ("-date", "shift", "workcell")

class LaborReportForm(forms.ModelForm):
    class Meta:
        model = LaborReport
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
class LaborReportAdmin(admin.ModelAdmin):
    get_changeform_initial_data = get_initials_lr
    form = LaborReportForm
    exclude = ("man_hours",)
    list_display = ("date", "shift", "workcell", "name", "man_hours")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("-date", "shift", "workcell")

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
    ordering = ("-date", "shift", "workcell")

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
    ordering = ("-date", "shift", "workcell")

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
    ordering = ("-date", "shift", "workcell")

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
    ordering = ("-date_performed", "problem_code")

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
    ordering = ("-date",)

class ProcessActivityReportForm(forms.ModelForm):
    class Meta:
        model = ProcessActivityReport
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    effect = get_radio_formfield(None, ONETOFIVE, ONETOFIVE[2][1])
    change_reverted = get_radio_formfield(None, YESNONA[:2])
class ProcessActivityReportAdmin(admin.ModelAdmin):
    form = ProcessActivityReportForm
    list_display = ("process_change", "date", "shift", "workcell")
    list_filter = ("date", "shift", "workcell")
    date_hierarchy = "date"
    ordering = ("-date", "shift", "workcell")


class LayeredProcessAuditForm(forms.ModelForm):
    class Meta:
        model = LayeredProcessAudit
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS, get_current_shift())
    verified_parameters = get_radio_formfield(
        "Has team leader verified that the processing parameters on " + \
        "the Process Setup sheet match the actual machine setup?", YESNONA)
    weight_inspection = get_radio_formfield(
        "Has the In-Process Weight & Gage Inspection been " + \
        "performed as required by quality?", YESNONA)
    chemicals_tracked = get_radio_formfield(
        "Does the Raw Material in use at the mix unit match the " + \
        "information on the lot Traceability form?", YESNONA)
    components_tracked = get_radio_formfield(
        "Is the procedure for Lot Tracking of components " + \
        "being followed correctly?", YESNONA)

    setup_posted = get_radio_formfield(
        "Is the set-up sheet posted?", YESNONA)
    chemicals_correct = get_radio_formfield(
        "Are Raw materials in use correct per set-up sheet?", YESNONA)
    event_missed_shot = get_radio_formfield(
        "Does employee know what to do in the " + \
        "event of a missed shot?", YESNONA)

    demold_criteria = get_radio_formfield(
        "Does employee know the acceptance criteria for the " + \
        "part(s) they are demolding?", YESNONA)
    demold_ncm = get_radio_formfield(
        "Does employee know what to do with " + \
        "Non-Conforming Material?", YESNONA)
    mold_release = get_radio_formfield(
        "Visual check for proper application of mold release.", YESNONA)

    work_instructions = get_radio_formfield(
        "Are current work intructions available?", YESNONA)
    proper_equipment = get_radio_formfield(
        "Does the operator have the proper equipment to " + \
        "perform their job duties?", YESNONA)
    trim_criteria = get_radio_formfield(
        "Does employee know the acceptance criteria for the " + \
        "part(s) they are inspecting?", YESNONA)
    inspecting_prior = get_radio_formfield(
        "Are parts inspected prior to trim?", YESNONA)
    trim_dcm = get_radio_formfield(
        "Is the Control of Non-Conforming Product Procedure " + \
        "being followed?", YESNONA)
    quality_alerts = get_radio_formfield(
        "If there are quality alerts posted for any part in the cell, " + \
        "do employees have knowledge of QA?", YESNONA)
    boxes_marked = get_radio_formfield(
        "Are boxes properly marked with the Shift " + \
        "and Operator I.D.?", YESNONA)
    pack_criteria = get_radio_formfield(
        "Do parts meet acceptance criteria and " + \
        "are correct parts in box?", YESNONA)
    labels_match = get_radio_formfield(
        "Does part# on label match parts in box?", YESNONA)
    fifo_product = get_radio_formfield(
        "Is FIFO being followed for all finished product?", YESNONA)
    product_tracked = get_radio_formfield(
        "Is final audit process correctly followed?", YESNONA)

    ppe = get_radio_formfield(
        "Do all employees know: What is PPE?", YESNONA[:2])
    ppe_info = get_radio_formfield(
        "Do all employees know: Where can you find " + \
        "information for the PPE you must wear?", YESNONA[:2])
    sds = get_radio_formfield(
        "Do all employees know: What is the SDS " + \
        "and where would you find it?", YESNONA[:2])
    iso_exposure = get_radio_formfield(
        "Do all employees know: Are you ever " + \
        "exposed to isocyanate?", YESNONA[:2])

class LayeredProcessAuditAdmin(admin.ModelAdmin):
    form = LayeredProcessAuditForm
    fieldsets = (
        ('Cell/Leader Questions:', {
            'fields': ('verified_parameters', 
                        'weight_inspection',
                        'chemicals_tracked',
                        'components_tracked',
                        'setup_posted',
                        'chemicals_correct'),
        }),
        ('Table Questions:', {
            'fields': ('event_missed_shot',
                        'demold_criteria',
                        'demold_ncm',
                        'mold_release'),
        }),
        ('Trim/Pack Questions:', {
            'fields': ('work_instructions',
                        'proper_equipment',
                        'trim_criteria',
                        'inspecting_prior',
                        'trim_dcm',
                        'quality_alerts',
                        'boxes_marked',
                        'pack_criteria',
                        'labels_match',
                        'fifo_product',
                        'product_tracked'),
        }),
        ('Safety Questions:', {
            'fields': ('ppe', 'ppe_info', 'sds', 'iso_exposure'),
        }),
        ('Comments:', {
            'fields': ('comments',),
        }),
    )
    list_display = ("workcell", "date", "shift", "employee")
    list_filter = ("date", "shift", "workcell")
    date_hierarchy = "date"
    ordering = ("-date", "shift", "workcell")


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
admin.site.register(LaborReport, LaborReportAdmin)
admin.site.register(LaborAllocationReport, LaborAllocationReportAdmin)
admin.site.register(Downtime, DowntimeAdmin)
admin.site.register(SpotCheckReport, SpotCheckReportAdmin)
admin.site.register(MaintenanceRecord, MaintenanceRecordAdmin)
admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)
admin.site.register(ProcessActivityReport, ProcessActivityReportAdmin)
admin.site.register(LayeredProcessAudit, LayeredProcessAuditAdmin)

