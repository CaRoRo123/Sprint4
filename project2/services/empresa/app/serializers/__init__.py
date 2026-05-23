from rest_framework import serializers
from app.models import Empresa, ReporteEmpresa


class ReporteEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReporteEmpresa
        fields = ["id", "mes", "costo_total", "moneda", "detalle_json", "generado_en"]
        read_only_fields = ["id", "generado_en"]


class EmpresaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Empresa
        fields = ["nombre", "nit", "email_contacto", "telefono", "activo"]


class GenerarReporteInputSerializer(serializers.Serializer):
    mes = serializers.RegexField(
        regex=r"^\d{4}-(0[1-9]|1[0-2])$",
        error_messages={"invalid": "Formato requerido: YYYY-MM (ej: 2024-01)"},
    )
