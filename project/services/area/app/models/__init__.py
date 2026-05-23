from django.db import models


class Area(models.Model):
    """Representa un área organizacional dentro de una empresa."""

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    empresa_id = models.BigIntegerField(
        help_text="FK externa al Servicio Empresa"
    )
    responsable_nombre = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "areas"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre


class ReporteArea(models.Model):
    """Snapshot de estado de un área (append-only, CQRS read side)."""

    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name="reportes"
    )
    total_proyectos = models.IntegerField(default=0)
    proyectos_activos = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)
    generado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reportes_area"
        ordering = ["-generado_en"]
