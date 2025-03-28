from django.contrib import admin
from django.http import HttpResponse
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
    actions = ["export_default_data"]
    def export_default_data(self, request, queryset):
        """
        Exportar la data por defecto del modelo RegisterAccess.
        """
        resource = EmployeeResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="employees.xlsx"'
        return response

    export_default_data.short_description = "Exportar datos por defecto"



admin.site.register(Employee, EmployeesAdmin)
