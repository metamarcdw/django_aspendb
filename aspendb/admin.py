from django.contrib import admin
from django import forms
from aspendb.models import *

admin.site.site_title = "Aspen Technologies Database"
admin.site.site_header = "Aspen Technologies Database"

def get_radio_formfield(label, choices):
    return forms.ChoiceField(label=label, choices=choices,
        initial="", widget=forms.widgets.RadioSelect())

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS)
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
    shift = get_radio_formfield(None, SHIFTS)
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
    shift = get_radio_formfield(None, SHIFTS)
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
    form = StartOfShiftForm
    list_display = ("date", "shift", "workcell")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift")


class EndOfShiftForm(forms.ModelForm):
    class Meta:
        model = EndOfShift
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS)
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
    shift = get_radio_formfield(None, SHIFTS)
class ScrapReportAdmin(admin.ModelAdmin):
    form = ScrapReportForm
    exclude = ("bad_mix", "dents", "mold_release", "non_fill",
                "collapse", "tears", "trim", "voilds", "open_voilds",
                "under_weight", "over_weight", "cracks", "swollen",
                "contamination", "total_scrap")
    list_display = ("part", "date", "shift", "workcell", "total_scrap")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class DowntimeForm(forms.ModelForm):
    class Meta:
        model = Downtime
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS)
class DowntimeAdmin(admin.ModelAdmin):
    form = DowntimeForm
    list_display = ("date", "shift", "workcell", "code")
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
    list_display = ("date", "problem_code", "work_done")
    list_filter = ("date", "problem_code")
    date_hierarchy = "date"
    ordering = ("date", "problem_code")

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = "__all__"
    shift = get_radio_formfield(None, SHIFTS)
class MaintenanceRequestAdmin(admin.ModelAdmin):
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
admin.site.register(Downtime, DowntimeAdmin)
admin.site.register(MaintenanceRecord, MaintenanceRecordAdmin)
admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)

