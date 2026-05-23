from rest_framework import serializers
from app.models import Proyecto, ReporteProyecto


class ReporteProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReporteProyecto
        fields = ["id", "mes", "costo_total", "moneda", "detalle_json", "generado_en"]
        read_only_fields = ["id", "generado_en"]


class ProyectoReadSerializer(serializers.ModelSerializer):
    """Solo lectura — se usa para serializar lo que viene de DynamoDB."""

    class Meta:
        model  = Proyecto
        fields = [
            "id", "nombre", "descripcion", "fecha_inicio", "fecha_fin",
            "activo", "empresa_id", "area_id", "created_at", "updated_at",
        ]


class ProyectoWriteSerializer(serializers.ModelSerializer):
    """Validación de entrada para creación/actualización."""

    class Meta:
        model  = Proyecto
        fields = [
            "nombre", "descripcion", "fecha_inicio", "fecha_fin",
            "activo", "empresa_id", "area_id",
        ]


class GenerarReporteInputSerializer(serializers.Serializer):
    """Valida el body del endpoint de generar reporte."""
    mes = serializers.RegexField(
        regex=r"^\d{4}-(0[1-9]|1[0-2])$",
        error_messages={"invalid": "El mes debe tener formato YYYY-MM (ej: 2024-01)"},
    )
