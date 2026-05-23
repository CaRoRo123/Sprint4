from app.cqrs import dynamo


def _pk(area_id: int) -> str:
    return f"AREA#{area_id}"


def upsert_area(area) -> None:
    dynamo.put_item(
        pk          = _pk(area.pk),
        sk          = "METADATA",
        entity_type = "AREA",
        data        = {
            "id":                 area.pk,
            "nombre":             area.nombre,
            "descripcion":        area.descripcion,
            "responsable_nombre": area.responsable_nombre,
            "activo":             area.activo,
            "empresa_id":         area.empresa_id,
            "created_at":         area.created_at.isoformat(),
            "updated_at":         area.updated_at.isoformat(),
        },
    )


def upsert_reporte_area(reporte) -> None:
    dynamo.put_item(
        pk          = _pk(reporte.area_id),
        sk          = f"REPORT#{reporte.mes}",
        entity_type = "REPORTE_AREA",
        data        = {
            "id":          reporte.pk,
            "area_id":     reporte.area_id,
            "mes":         reporte.mes,
            "costo_total": str(reporte.costo_total),
            "moneda":      reporte.moneda,
            "detalle_json":reporte.detalle_json,
            "generado_en": reporte.generado_en.isoformat(),
        },
    )


def delete_area(area_id: int) -> None:
    items = dynamo.query_by_pk(_pk(area_id))
    for item in items:
        dynamo.delete_item(pk=item["PK"], sk=item["SK"])
