"""
commands.py — Write side del CQRS.
Toda operación que muta estado pasa por aquí.
Escribe en Aurora; la señal post_save se encarga de sincronizar DynamoDB.
"""
from app.models import Proyecto, ReporteProyecto


def crear_proyecto(data: dict) -> Proyecto:
    """
    Crea un Proyecto nuevo en Aurora.
    La señal post_save proyecta el resultado a DynamoDB automáticamente.
    """
    proyecto = Proyecto.objects.create(**data)
    return proyecto


def actualizar_proyecto(proyecto_id: int, data: dict) -> Proyecto:
    """Actualiza campos de un Proyecto existente."""
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    for campo, valor in data.items():
        setattr(proyecto, campo, valor)
    proyecto.save()         
    return proyecto


def eliminar_proyecto(proyecto_id: int) -> None:
    """
    Soft-delete: marca activo=False en Aurora y elimina del read side (DynamoDB).
    """
    from app.cqrs.sync import delete_proyecto as sync_delete

    proyecto = Proyecto.objects.get(pk=proyecto_id)
    proyecto.activo = False
    proyecto.save()

    sync_delete(proyecto_id)


def crear_reporte(proyecto_id: int, mes: str, datos_costo: dict) -> ReporteProyecto:
    """
    Persiste un ReporteProyecto en Aurora con el resultado de Cost Explorer.
    La señal post_save proyecta a DynamoDB.
    """
    proyecto = Proyecto.objects.get(pk=proyecto_id)

    # upsert: si ya existe el reporte de ese mes, lo reemplaza
    reporte, _ = ReporteProyecto.objects.update_or_create(
        proyecto=proyecto,
        mes=mes,
        defaults={
            "costo_total":  datos_costo.get("total", 0),
            "moneda":       datos_costo.get("moneda", "USD"),
            "detalle_json": datos_costo.get("detalle", {}),
        },
    )
    return reporte
