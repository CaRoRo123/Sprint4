"""
sync.py — Proyecta los modelos de Aurora hacia DynamoDB (read side).
Llamado automáticamente por las señales post_save de los modelos.
"""
from decimal import Decimal
from app.cqrs import dynamo


def _pk(proyecto_id: int) -> str:
    return f"PROYECTO#{proyecto_id}"


def upsert_proyecto(proyecto) -> None:
    """
    Sincroniza un Proyecto de Aurora → DynamoDB.
    SK = METADATA
    """
    dynamo.put_item(
        pk          = _pk(proyecto.pk),
        sk          = "METADATA",
        entity_type = "PROYECTO",
        data        = {
            "id":          proyecto.pk,
            "nombre":      proyecto.nombre,
            "descripcion": proyecto.descripcion,
            "fecha_inicio": str(proyecto.fecha_inicio),
            "fecha_fin":   str(proyecto.fecha_fin) if proyecto.fecha_fin else None,
            "activo":      proyecto.activo,
            "empresa_id":  proyecto.empresa_id,
            "area_id":     proyecto.area_id,
            "created_at":  proyecto.created_at.isoformat(),
            "updated_at":  proyecto.updated_at.isoformat(),
        },
    )


def upsert_reporte_proyecto(reporte) -> None:
    """
    Sincroniza un ReporteProyecto de Aurora → DynamoDB.
    SK = REPORT#<YYYY-MM>
    """
    dynamo.put_item(
        pk          = _pk(reporte.proyecto_id),
        sk          = f"REPORT#{reporte.mes}",
        entity_type = "REPORTE_PROYECTO",
        data        = {
            "id":           reporte.pk,
            "proyecto_id":  reporte.proyecto_id,
            "mes":          reporte.mes,
            "costo_total":  str(reporte.costo_total),   # Decimal → str para DynamoDB
            "moneda":       reporte.moneda,
            "detalle_json": reporte.detalle_json,
            "generado_en":  reporte.generado_en.isoformat(),
        },
    )


def delete_proyecto(proyecto_id: int) -> None:
    """Elimina el proyecto y todos sus reportes del read side."""
    items = dynamo.query_by_pk(_pk(proyecto_id))
    for item in items:
        dynamo.delete_item(pk=item["PK"], sk=item["SK"])
