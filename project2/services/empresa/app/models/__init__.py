from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Empresa(models.Model):
    nombre         = models.CharField(max_length=255)
    nit            = models.CharField(max_length=20, unique=True)
    email_contacto = models.EmailField(blank=True)
    telefono       = models.CharField(max_length=30, blank=True)
    activo         = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "empresas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nombre} ({self.nit})"


class ReporteEmpresa(models.Model):
    empresa      = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="reportes")
    mes          = models.CharField(max_length=7, help_text="YYYY-MM")
    costo_total  = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    moneda       = models.CharField(max_length=10, default="USD")
    detalle_json = models.JSONField(default=dict)
    generado_en  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = "reportes_empresa"
        unique_together = [("empresa", "mes")]
        ordering        = ["-mes"]

    def __str__(self):
        return f"Reporte {self.empresa} / {self.mes}"


@receiver(post_save, sender=Empresa)
def sync_empresa_to_dynamo(sender, instance, **kwargs):
    from app.cqrs.sync import upsert_empresa
    upsert_empresa(instance)


@receiver(post_save, sender=ReporteEmpresa)
def sync_reporte_empresa_to_dynamo(sender, instance, **kwargs):
    from app.cqrs.sync import upsert_reporte_empresa
    upsert_reporte_empresa(instance)
