from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Employee

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        exclude = ('user',)

class EmployeesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('get_user_id_card', 'get_user_name','get_user_is_staff','is_active')
    search_fields = ['user__id_card', 'user__name','user__is_staff','is_active']
    resource_class = EmployeeResource  # Nota: `resource_class`, no `resources_class
    
    def get_user_id_card(self, obj):
        
        return obj.user.id_card
    get_user_id_card.short_description = 'Identificación'

    def get_user_name(self, obj):
        return obj.user.name
    get_user_name.short_description = 'Nombre'

    def get_user_last_name(self, obj):
        return obj.user.last_name
    get_user_last_name.short_description = 'Apellido'

    def get_user_is_staff(self, obj):
        return obj.user.is_staff
    get_user_is_staff.short_description = 'Staff'
    get_user_is_staff.boolean = True
    # Registro del modelo
admin.site.register(Employee, EmployeesAdmin)

