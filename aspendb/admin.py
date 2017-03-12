from django.contrib import admin
from aspendb.models import *

admin.site.site_title = "Aspen Technologies Database"
admin.site.site_header = "Aspen Technologies Database"

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "shift", "email")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")

class PartAdmin(admin.ModelAdmin):
    list_display = ("part_number", "program_name")

    def program_name(self, obj):
        return obj.program.name

class StartOfShiftAdmin(admin.ModelAdmin):
    list_display = ("date", "shift", "workcell")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date",)

class EndOfShiftAdmin(admin.ModelAdmin):
    exclude = ("total_shots", "oee", "scrap_percent")
    list_display = ("date", "shift", "workcell", "oee", "scrap_percent")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date",)

class ScrapReportAdmin(admin.ModelAdmin):
    list_display = ("part", "date", "shift", "workcell")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class DowntimeAdmin(admin.ModelAdmin):
    list_display = ("date", "shift", "workcell", "code")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date", "shift", "workcell")

class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ("date", "shift", "problem")
    list_filter = ("date",)
    date_hierarchy = "date"
    ordering = ("date",)

# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Workcell)
admin.site.register(Part, PartAdmin)
admin.site.register(DowntimeCode)
admin.site.register(StartOfShift, StartOfShiftAdmin)
admin.site.register(EndOfShift, EndOfShiftAdmin)
admin.site.register(ScrapReport, ScrapReportAdmin)
admin.site.register(Downtime, DowntimeAdmin)
admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)

