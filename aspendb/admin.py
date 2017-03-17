from django.contrib import admin
from aspendb.models import *

admin.site.site_title = "Aspen Technologies Database"
admin.site.site_header = "Aspen Technologies Database"

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "shift", "email")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")

class WorkcellAdmin(admin.ModelAdmin):
    list_display = ("name", "foam_system", "turns_per_hour")
    ordering = ("name",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['cell_leader_1st'].widget = \
            autocomplete.ModelSelect2(url='employee-autocomplete')
        form.base_fields['cell_leader_2nd'].widget = \
            autocomplete.ModelSelect2(url='employee-autocomplete')
        return form

class PartAdmin(admin.ModelAdmin):
    list_display = ("part_number", "program_name")

    def program_name(self, obj):
        return obj.program.name

class ProductionScheduleAdmin(admin.ModelAdmin):
    exclude = ("total_shots",)
    list_display = ("part", "shots", "date", "shift", "workcell")
    list_filter = ("date", "shift", "workcell")
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class StartOfShiftAdmin(admin.ModelAdmin):
    list_display = ("date", "shift", "workcell")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift")

class EndOfShiftAdmin(admin.ModelAdmin):
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

class ScrapReportAdmin(admin.ModelAdmin):
    exclude = ("bad_mix", "dents", "mold_release", "non_fill",
                "collapse", "tears", "trim", "voilds", "open_voilds",
                "under_weight", "over_weight", "total_scrap")
    list_display = ("part", "date", "shift", "workcell", "total_scrap")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class DowntimeAdmin(admin.ModelAdmin):
    list_display = ("date", "shift", "workcell", "code")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("date", "problem_code", "work_done")
    list_filter = ("date", "problem_code")
    date_hierarchy = "date"
    ordering = ("date", "problem_code")

class MaintenanceRequestAdmin(admin.ModelAdmin):
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

