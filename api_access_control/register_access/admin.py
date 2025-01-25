from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .models import QrCode, RegisterAccess


class RegisterAccessResource(resources.ModelResource):
    user = Field(attribute="user", column_name="user", readonly=True)

    class Meta:
        model = RegisterAccess
        exclude = ("user",)


class QrCodeResource(resources.ModelResource):
    user = Field(attribute="user", column_name="user", readonly=True)

    class Meta:
        model = QrCode
        exclude = ("user",)


class QrCodeAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        "get_user_id_card",
        "get_user_name",
        "get_user_last_name",
        "qr_code",
    )
    search_fields = ["user__name", "user__id_card"]
    resource_class = QrCodeResource

    def get_user_id_card(self, obj):
        return obj.user.id_card

    get_user_id_card.short_description = "Identificación"

    def get_user_name(self, obj):
        return obj.user.name

    get_user_name.short_description = "Nombre"

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = "Apellido"


class RegisterAccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        "get_user_id_card",
        "get_user_name",
        "get_user_last_name",
        "type_access",
        "user_entry",
        "user_exit",
        "hours_worked",
        "extra_hours",
        "extra_hours_night",
    )
    search_fields = [
        "user__name",
        "user__id_card",
        "type_access",
        "user_entry",
        "user_exit",
    ]
    resource_class = RegisterAccessResource

    def get_user_id_card(self, obj):

        return obj.user.id_card

    get_user_id_card.short_description = "Identificación"

    def get_user_name(self, obj):
        return obj.user.name

    get_user_name.short_description = "Nombre"

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = "Apellido"

    # Sobreescribir para buscar por valor y descripción de `type_access`
    def get_search_results(self, request, queryset, search_term):
        # Primero, obtenemos los resultados de la búsqueda normal
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        # Si el término de búsqueda coincide con la descripción legible, agregamos esos resultados
        if search_term.lower() in ["ingreso", "in"]:
            queryset |= self.model.objects.filter(type_access="IN")
        elif search_term.lower() in ["salida", "out"]:
            queryset |= self.model.objects.filter(type_access="OUT")

        return queryset, use_distinct


# Registrar el modelo en admin
admin.site.register(RegisterAccess, RegisterAccessAdmin)
admin.site.register(QrCode, QrCodeAdmin)
