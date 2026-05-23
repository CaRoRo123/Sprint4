from django.db import models


class Proyecto(models.Model):
    """Representa un proyecto dentro del sistema."""

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    empresa_id = models.BigIntegerField(
        help_text="FK externa al Servicio Empresa (sin constraint DB)"
    )
    area_id = models.BigIntegerField(
        help_text="FK externa al Servicio Area (sin constraint DB)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "proyectos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre


class ReporteProyecto(models.Model):
    """Snapshot de estado de un proyecto (append-only, CQRS read side)."""

    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name="reportes"
    )
    estado = models.CharField(max_length=100)
    avance_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    generado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reportes_proyecto"
        ordering = ["-generado_en"]

    def __str__(self):
        return f"Reporte {self.proyecto} @ {self.generado_en:%Y-%m-%d}"
