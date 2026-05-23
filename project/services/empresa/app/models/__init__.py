from django.db import models


class Empresa(models.Model):
    """Representa una empresa registrada en el sistema."""

    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=20, unique=True)
    email_contacto = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "empresas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nombre} ({self.nit})"


class ReporteEmpresa(models.Model):
    """Snapshot de estado de una empresa (append-only, CQRS read side)."""

    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="reportes"
    )
    total_areas = models.IntegerField(default=0)
    total_proyectos = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)
    generado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reportes_empresa"
        ordering = ["-generado_en"]
