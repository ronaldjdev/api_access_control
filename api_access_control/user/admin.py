from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UsersAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id_card', 'name','last_name','email','is_staff','is_active')
    search_fields = ['id_card', 'name','last_name','email','is_staff','is_active']
    # resource_class = UserResource  # Nota: `resource_class`, no `resources_class`

# Registro del modelo
admin.site.register(User, UsersAdmin)

