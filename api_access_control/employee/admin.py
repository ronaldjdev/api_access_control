from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Employee

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee

class EmployeesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user__id_card', 'user__name','user__is_staff','is_active')
    search_fields = ['user__id_card', 'user__name','user__is_staff','is_active']
    # resource_class = EmployeeResource  # Nota: `resource_class`, no `resources_class`

# Registro del modelo
admin.site.register(Employee, EmployeesAdmin)

