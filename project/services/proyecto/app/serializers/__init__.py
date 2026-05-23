from rest_framework import serializers
from app.models import Proyecto, ReporteProyecto


class ReporteProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteProyecto
        fields = ["id", "estado", "avance_porcentaje", "observaciones", "generado_en"]
        read_only_fields = ["id", "generado_en"]


class ProyectoSerializer(serializers.ModelSerializer):
    reportes = ReporteProyectoSerializer(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = [
            "id",
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "activo",
            "empresa_id",
            "area_id",
            "reportes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProyectoWriteSerializer(serializers.ModelSerializer):
    """Serializer para creación/actualización (sin reportes anidados)."""

    class Meta:
        model = Proyecto
        fields = [
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "activo",
            "empresa_id",
            "area_id",
        ]
