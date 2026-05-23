from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Area(models.Model):
    nombre             = models.CharField(max_length=255)
    descripcion        = models.TextField(blank=True)
    responsable_nombre = models.CharField(max_length=255, blank=True)
    activo             = models.BooleanField(default=True)
    empresa_id         = models.BigIntegerField(help_text="FK externa al Servicio Empresa")
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "areas"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre


class ReporteArea(models.Model):
    area         = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="reportes")
    mes          = models.CharField(max_length=7, help_text="YYYY-MM")
    costo_total  = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    moneda       = models.CharField(max_length=10, default="USD")
    detalle_json = models.JSONField(default=dict)
    generado_en  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = "reportes_area"
        unique_together = [("area", "mes")]
        ordering        = ["-mes"]

    def __str__(self):
        return f"Reporte {self.area} / {self.mes}"


@receiver(post_save, sender=Area)
def sync_area_to_dynamo(sender, instance, **kwargs):
    from app.cqrs.sync import upsert_area
    upsert_area(instance)


@receiver(post_save, sender=ReporteArea)
def sync_reporte_area_to_dynamo(sender, instance, **kwargs):
    from app.cqrs.sync import upsert_reporte_area
    upsert_reporte_area(instance)
