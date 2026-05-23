from rest_framework import serializers
from app.models import Empresa, ReporteEmpresa


class ReporteEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteEmpresa
        fields = ["id", "total_areas", "total_proyectos", "observaciones", "generado_en"]
        read_only_fields = ["id", "generado_en"]


class EmpresaSerializer(serializers.ModelSerializer):
    reportes = ReporteEmpresaSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = [
            "id", "nombre", "nit", "email_contacto", "telefono",
            "activo", "reportes", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class EmpresaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ["nombre", "nit", "email_contacto", "telefono", "activo"]
