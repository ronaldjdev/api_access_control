from decimal import Decimal
from django.contrib import admin
from import_export import resources
from tablib import Dataset
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .models import QrCode, RegisterAccess
import holidays
from datetime import datetime
from rangefilter.filters import DateRangeFilter
from collections import defaultdict

# class RegisterAccessResource(resources.ModelResource):
#     user = Field(attribute="user", column_name="user", readonly=True)

#     class Meta:
#         model = RegisterAccess
#         exclude = ("user",)

colombia_holidays = holidays.Colombia(years=datetime.now().year)


def is_sunday_or_holiday(date):
    """
    Determines if the given date is either a Sunday or a public holiday.

    Args:
        date (datetime): The date to be checked.

    Returns:
        bool: True if the date is a Sunday or a holiday in Colombia, False otherwise.
    """

    return date.weekday() == 6 or date in colombia_holidays


class QrCodeResource(resources.ModelResource):
    user = Field(attribute="user", column_name="user", readonly=True)

    class Meta:
        model = QrCode
        exclude = ("user",)


class ExportRegisterAccessResource(resources.ModelResource):
    contrato = Field(column_name="Contrato", attribute="user__id_card")
    nombre = Field(column_name="Nombre", attribute="user__name")
    concepto = Field(column_name="concept", attribute="type_access")
    cantidad = Field(column_name="Cantidad", attribute="hours_worked")

    class Meta:
        model = RegisterAccess
        fields = ()

    def dehydrate_concepto(self, obj):
        """
        Asigna el concepto correspondiente a las horas extras trabajadas
        teniendo en cuenta si es domingo o festivo.

        Si es domingo o festivo, se asigna el concepto "DV10" para las horas
        extras diurnas y "DV11" para las horas extras nocturnas.

        Si no es domingo o festivo, se asigna el concepto "DV08" para las horas
        extras diurnas y "DV09" para las horas extras nocturnas.

        Args:
            obj (RegisterAccess): el objeto de registro de acceso

        Returns:
            str: el concepto correspondiente a las horas extras trabajadas
        """
        if is_sunday_or_holiday(obj.user_entry):
            if obj.extra_hours > 0:
                return "DV10"  # Horas extras dominicales y festivas
            elif obj.extra_hours_night > 0:
                return "DV11"  # Horas extras nocturnas dominicales y festivas

        # Mapear las horas extras a los conceptos correspondientes
        if obj.extra_hours > 0:
            return "DV08"  # Horas extras diurnas
        elif obj.extra_hours_night > 0:
            return "DV09"  # Horas extras nocturnas
        return ""

    def dehydrate_cantidad(self, obj):
        """
        Asigna la cantidad correspondiente al concepto de las horas extras diurnas o nocturnas,
        o 0 si no hay horas extras. Se utiliza para exportar la cantidad correspondiente al
        concepto en el archivo de exportación.
        """
        if obj.extra_hours > 0:
            return obj.extra_hours
        elif obj.extra_hours_night > 0:
            return obj.extra_hours_night
        # Puedes agregar más condiciones para otros conceptos si es necesario
        return 0

    def get_export_headers(self):
        """
        Devuelve los encabezados para la exportación de registros de acceso.

        Los encabezados incluyen información sobre el contrato, nombre del usuario,
        concepto de horas extras trabajadas, nombre calculado, y cantidad de horas.

        Returns:
            list: Una lista de cadenas que representan los encabezados de las columnas.
        """

        return ["Contrato", "Nombre", "Concepto", "C_Nombre", "Cantidad"]

    def export(self, queryset=None, *args, **kwargs):
        """
        Exporta un conjunto de datos de registros registrados con encabezados específicos y campos calculados
        Basado en el Queryset proporcionado. Si no se proporciona QuerySet, es predeterminado al administrador
        Queryset. El conjunto de datos incluye detalles del contrato del usuario, nombre y calcula el concepto
        y cantidad basada en horas adicionales trabajadas, teniendo en cuenta si el día es un domingo o vacaciones.

        Args:
            QuerySet (QuerySet, Opcional): un Django QuerySet de los objetos de registro
            exportado. Predeterminado no a ninguno.
            *Args: argumentos posicionales adicionales.
            **Kwargs: argumentos de palabras clave adicionales.

        Devoluciones:
            Conjunto de datos: un objeto de conjunto de datos de TAbib que contiene los datos exportados con encabezados "contrato",
            "Nombre", "Concepto", "C_nombre", "Cantidad".
        """
        dataset = Dataset(headers=self.get_export_headers())

        if queryset is None or not queryset.exists():
            queryset = self._meta.model.objects.all()

        # Diccionario para agrupar datos antes de exportarlos
        grouped_data = defaultdict(Decimal)

        for obj in queryset:
            contrato = obj.user.id_card
            nombre = f"{obj.user.name.upper()} {obj.user.last_name.upper()}"

            # Determinar los conceptos según si es domingo o festivo
            if is_sunday_or_holiday(obj.user_entry):
                if obj.extra_hours > 0:
                    grouped_data[(contrato, nombre, "DV10", "DV10")] += obj.extra_hours
                if obj.extra_hours_night > 0:
                    grouped_data[(contrato, nombre, "DV11", "DV11")] += obj.extra_hours_night
            else:
                if obj.extra_hours > 0:
                    grouped_data[(contrato, nombre, "DV08", "DV08")] += obj.extra_hours
                if obj.extra_hours_night > 0:
                    grouped_data[(contrato, nombre, "DV09", "DV09")] += obj.extra_hours_night

        # Agregar los datos agrupados al dataset
        for (contrato, nombre, concepto, c_nombre), cantidad in grouped_data.items():
            dataset.append([contrato, nombre, concepto, c_nombre, round(cantidad, 2)])

        return dataset

class ExportRegisterAccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ExportRegisterAccessResource
    list_display = (
        "user",
        "type_access",
        "user_entry",
        "user_exit",
        "hours_worked",
        "extra_hours",
        "extra_hours_night",
    )
    list_filter = (
        ("user_entry", DateRangeFilter),  # Filtro por rango de fechas
    )
    
    def get_queryset(self, request):
        # Asegurarnos de que el queryset respeta los filtros aplicados
        qs = super().get_queryset(request)
        # Filtrar el queryset basado en los parámetros de la solicitud (opcional)
        return qs


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


# class RegisterAccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):

#     list_display = (
#         "get_user_id_card",
#         "get_user_name",
#         "get_user_last_name",
#         "type_access",
#         "user_entry",
#         "user_exit",
#         "hours_worked",
#         "extra_hours",
#         "extra_hours_night",
#     )
#     search_fields = [
#         "user__name",
#         "user__id_card",
#         "type_access",
#         "user_entry",
#         "user_exit",
#     ]
#     resource_class = RegisterAccessResource

#     def get_user_id_card(self, obj):

#         return obj.user.id_card

#     get_user_id_card.short_description = "Identificación"

#     def get_user_name(self, obj):
#         return obj.user.name

#     get_user_name.short_description = "Nombre"

#     def get_user_last_name(self, obj):
#         return obj.user.last_name

#     get_user_last_name.short_description = "Apellido"

#     # Sobreescribir para buscar por valor y descripción de `type_access`
#     def get_search_results(self, request, queryset, search_term):
#         # Primero, obtenemos los resultados de la búsqueda normal
#         queryset, use_distinct = super().get_search_results(
#             request, queryset, search_term
#         )

#         # Si el término de búsqueda coincide con la descripción legible, agregamos esos resultados
#         if search_term.lower() in ["ingreso", "in"]:
#             queryset |= self.model.objects.filter(type_access="IN")
#         elif search_term.lower() in ["salida", "out"]:
#             queryset |= self.model.objects.filter(type_access="OUT")

#         return queryset, use_distinct


# Registrar el modelo en admin
admin.site.register(RegisterAccess, ExportRegisterAccessAdmin)
# admin.site.register(RegisterAccess, RegisterAccessAdmin)
admin.site.register(QrCode, QrCodeAdmin)
