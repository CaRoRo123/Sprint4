from rest_framework import serializers
from app.models import Area, ReporteArea


class ReporteAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteArea
        fields = ["id", "total_proyectos", "proyectos_activos", "observaciones", "generado_en"]
        read_only_fields = ["id", "generado_en"]


class AreaSerializer(serializers.ModelSerializer):
    reportes = ReporteAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = [
            "id", "nombre", "descripcion", "empresa_id",
            "responsable_nombre", "activo", "reportes",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AreaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ["nombre", "descripcion", "empresa_id", "responsable_nombre", "activo"]
