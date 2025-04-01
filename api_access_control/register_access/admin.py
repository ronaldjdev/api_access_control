from decimal import Decimal
from django.contrib import admin
from django.http import HttpResponse
# from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from tablib import Dataset
from datetime import datetime, timedelta
import holidays
from rangefilter.filters import DateRangeFilter
from collections import defaultdict
from .models import RegisterAccess
from django.urls import reverse
import json

colombia_holidays = holidays.Colombia(years=datetime.now().year)


def is_sunday_or_holiday(date):
    return date.weekday() == 6 or date in colombia_holidays


class DefaultRegisterAccessResource(resources.ModelResource):
    class Meta:
        model = RegisterAccess


class CustomRegisterAccessResource(resources.ModelResource):
    contrato = Field(column_name="Contrato", attribute="user__id_card")
    nombre = Field(column_name="Nombre", attribute="user__name")
    concepto = Field(column_name="Concepto", attribute="type_access")
    cantidad = Field(column_name="Cantidad", attribute="hours_worked")

    class Meta:
        model = RegisterAccess
        fields = ()

    def dehydrate_concepto(self, obj):
        if is_sunday_or_holiday(obj.user_entry):
            if obj.extra_hours > 0:
                return "DV10"
            elif obj.extra_hours_night > 0:
                return "DV11"
        if obj.extra_hours > 0:
            return "DV08"
        elif obj.extra_hours_night > 0:
            return "DV09"
        return ""

    def dehydrate_cantidad(self, obj):
        if obj.extra_hours > 0:
            return obj.extra_hours
        elif obj.extra_hours_night > 0:
            return obj.extra_hours_night
        return 0

    def get_export_headers(self):
        return ["Contrato", "Nombre", "Concepto", "C_Nombre", "Cantidad"]

    def export(self, queryset=None, *args, **kwargs):
        dataset = Dataset(headers=self.get_export_headers())
        if queryset is None or not queryset.exists():
            queryset = self._meta.model.objects.all()

        grouped_data = defaultdict(Decimal)

        for obj in queryset:
            contrato = obj.user.id_card
            nombre = f"{obj.user.name.upper()} {obj.user.last_name.upper()}"

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

        for (contrato, nombre, concepto, c_nombre), cantidad in grouped_data.items():
            dataset.append([contrato, nombre, concepto, c_nombre, round(cantidad, 2)])

        return dataset


class ExportRegisterAccessAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DefaultRegisterAccessResource
    list_display = (
        "user",
        "type_access",
        "user_entry",
        "user_exit",
        "hours_worked",
        "extra_hours",
        "extra_hours_night",
        "entry_observation",
        "exit_observation",
    )
    search_fields = [
        "user__name",
        "user__id_card",
        "type_access",
        "user_entry",
        "user_exit",
    ]
    list_filter = (("user_entry", DateRangeFilter),)

    actions = ["export_default_data", "export_custom_data", "recalculate_hours"]
    
    def get_remark_data(self, obj):
        """Devuelve el JSON del campo remark como diccionario."""
        if isinstance(obj.remark, dict):
            return obj.remark  # Ya es un diccionario
        try:
            return json.loads(obj.remark) if obj.remark else {}
        except json.JSONDecodeError:
            return {}

    def entry_observation(self, obj):
        """Extrae entry_observation del campo JSON remark."""
        remark_data = self.get_remark_data(obj)
        return remark_data.get("entry_observation", "-")

    def exit_observation(self, obj):
        """Extrae exit_observation del campo JSON remark."""
        remark_data = self.get_remark_data(obj)
        return remark_data.get("exit_observation", "-")

    entry_observation.short_description = "Observación Entrada"
    exit_observation.short_description = "Observación Salida"

    def export_custom_data(self, request, queryset):
        """
        Exportar la data con el formato personalizado.
        """
        resource = CustomRegisterAccessResource()
        dataset = resource.export(queryset)
        file_name = f'register_access_zeus_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        response = HttpResponse(dataset.xlsx, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response

    export_custom_data.short_description = "Exportar datos personalizados"

    def export_default_data(self, request, queryset):
        """
        Exportar la data por defecto del modelo RegisterAccess.
        """
        file_name = f'register_access_data_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        resource = DefaultRegisterAccessResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response

    export_default_data.short_description = "Exportar datos por defecto"

    def recalculate_hours(self, request, queryset):
        """
        Acción para recalcular las horas trabajadas y las horas extras
        de todos los registros seleccionados.
        """
        updated_count = 0
        for register in queryset:

            if register.remark.get("exit_observation") == "" or register.remark == {}  and register.hours_worked > 8 :
                if register.user_entry:
                    register.user_exit = register.user_entry + timedelta (hours=8)

            # Recalcular las horas y horas extras
            if not register.user_exit:
                register.hours_worked = 0
                register.extra_hours = 0
                register.extra_hours_night = 0
                register.save()
            register.save()  # Recalcula las horas 
            updated_count += 1

        success_message = f"{updated_count} registros actualizados con éxito."

        # Código JavaScript para alert y redirección
        script = f"""
        <script type="text/javascript">
            alert("{success_message}");
            window.location.href = "{reverse('admin:{0}_{1}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))}";
        </script>
        """

        return HttpResponse(script)

    recalculate_hours.short_description = "Recalcular horas y horas extras"


admin.site.register(RegisterAccess, ExportRegisterAccessAdmin)
