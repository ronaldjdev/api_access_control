from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UsersAdmin(ImportExportModelAdmin, UserAdmin):
    list_display = ('id_card', 'username', 'name', 'last_name', 'email', 'is_staff', 'is_active')
    search_fields = ['id_card', 'username', 'name', 'last_name', 'email']

    fieldsets = (
        (None, {'fields': ('id_card', 'username', 'name', 'last_name', 'email', 'password')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Información adicional', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id_card', 'username', 'name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    resource_class = UserResource

admin.site.register(User, UsersAdmin)
