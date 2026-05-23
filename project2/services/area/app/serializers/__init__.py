from rest_framework import serializers
from app.models import Area, ReporteArea


class ReporteAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReporteArea
        fields = ["id", "mes", "costo_total", "moneda", "detalle_json", "generado_en"]
        read_only_fields = ["id", "generado_en"]


class AreaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Area
        fields = ["nombre", "descripcion", "responsable_nombre", "activo", "empresa_id"]


class GenerarReporteInputSerializer(serializers.Serializer):
    mes = serializers.RegexField(
        regex=r"^\d{4}-(0[1-9]|1[0-2])$",
        error_messages={"invalid": "Formato requerido: YYYY-MM (ej: 2024-01)"},
    )
