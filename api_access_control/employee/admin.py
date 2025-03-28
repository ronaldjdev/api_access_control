from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Employee


class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee


class EmployeesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EmployeeResource
    list_display = (
        "user",
        "is_active",
    )
    search_fields = ["user", "is_active"]



admin.site.register(Employee, EmployeesAdmin)
