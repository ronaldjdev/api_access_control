from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import RegisterAccess


class RegisterAccessResourse(resources.ModelResource):
    class Meta:
        model = RegisterAccess

class RegisterAccesssAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    list_display    = ("employee__name",)
    search_fields   = ["employee__name"]
    resources_class = RegisterAccessResourse

# Register your models here.
admin.site.register(RegisterAccess  , RegisterAccesssAdmin  ),
