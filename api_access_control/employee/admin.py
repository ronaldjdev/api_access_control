from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Employee

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee

class EmployeesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_card', 'name','is_staff','is_active')
    search_fields = ['name']
    # resource_class = EmployeeResource  # Nota: `resource_class`, no `resources_class`

# Registro del modelo
admin.site.register(Employee, EmployeesAdmin)

