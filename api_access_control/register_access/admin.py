from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .models import RegisterAccess

class RegisterAccessResource(resources.ModelResource):
    employee_name = Field(attribute='employee', column_name='employee_name', readonly=True)

    class Meta:
        model = RegisterAccess
        exclude = ('employee',)

    # def dehydrate_employee_name(self, register_access):
    #     return str(register_access.employee)

class RegisterAccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display    = ("get_employee_identification", "get_employee_name", "type_access", "employee_entry", "employee_exit","hours_worked", "extra_hours")
    search_fields   = ["employee__name", "employee__identification", "type_access", "employee_entry", "employee_exit"]
    resource_class  = RegisterAccessResource

    def get_employee_identification(self, obj):
        return obj.employee.identification
    get_employee_identification.short_description = 'Identificación del Empleado'

    def get_employee_name(self, obj):
        return obj.employee.name
    get_employee_name.short_description = 'Nombre del Empleado'

# Registrar el modelo en admin
admin.site.register(RegisterAccess, RegisterAccessAdmin)
