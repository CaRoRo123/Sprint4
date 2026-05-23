"""
WRITE SIDE — Aurora PostgreSQL
Fuente de verdad. Todo comando escribe aquí primero.
Después del save, una señal sincroniza con DynamoDB (read side).
"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Proyecto(models.Model):
    nombre       = models.CharField(max_length=255)
    descripcion  = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField(null=True, blank=True)
    activo       = models.BooleanField(default=True)
    # FKs externas — sin constraint DB (microservicios independientes)
    empresa_id   = models.BigIntegerField()
    area_id      = models.BigIntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "proyectos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre


class ReporteProyecto(models.Model):
    """
    Registro de cada reporte de costos AWS generado para este proyecto.
    Se guarda en Aurora para auditoría y también en DynamoDB para lectura.
    """
    proyecto     = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name="reportes"
    )
    mes          = models.CharField(max_length=7, help_text="Formato YYYY-MM")
    costo_total  = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    moneda       = models.CharField(max_length=10, default="USD")
    detalle_json = models.JSONField(
        default=dict,
        help_text="Respuesta completa de AWS Cost Explorer"
    )
    generado_en  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = "reportes_proyecto"
        unique_together     = [("proyecto", "mes")]
        ordering            = ["-mes"]

    def __str__(self):
        return f"Reporte {self.proyecto} / {self.mes}"


# ── Señales: sincronizar con DynamoDB después de escribir en Aurora ───────────

@receiver(post_save, sender=Proyecto)
def sync_proyecto_to_dynamo(sender, instance, **kwargs):
    """Cada vez que se crea/actualiza un Proyecto en Aurora → actualizar DynamoDB."""
    from app.cqrs.sync import upsert_proyecto
    upsert_proyecto(instance)


@receiver(post_save, sender=ReporteProyecto)
def sync_reporte_to_dynamo(sender, instance, **kwargs):
    """Cada vez que se guarda un Reporte en Aurora → actualizar DynamoDB."""
    from app.cqrs.sync import upsert_reporte_proyecto
    upsert_reporte_proyecto(instance)
