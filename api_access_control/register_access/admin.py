from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .models import RegisterAccess


class RegisterAccessResourse(resources.ModelResource):
    employee_name = Field(attribute='employee', column_name='Nombre del Empleado', readonly=True)
    class Meta:
        model = RegisterAccess
        formats = ["xls", "xlsx", "csv", "tsv", "json"]
        exclude = ('employee',)
    
    def dehydrate_employee_name(self, register_access):
        return str(register_access.employee)

class RegisterAccesssAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    list_display    = ("employee__identification","employee__name", "type_access", "employee_entry", "employee_exit",)
    search_fields   = ["employee__name", "employee__identification", "type_access", "employee_entry", "employee_exit",]
    resources_class = RegisterAccessResourse

# Register your models here.
admin.site.register(RegisterAccess  , RegisterAccesssAdmin  ),
