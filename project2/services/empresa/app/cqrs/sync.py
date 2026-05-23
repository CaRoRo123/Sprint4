from app.cqrs import dynamo


def _pk(empresa_id: int) -> str:
    return f"EMPRESA#{empresa_id}"


def upsert_empresa(empresa) -> None:
    dynamo.put_item(
        pk          = _pk(empresa.pk),
        sk          = "METADATA",
        entity_type = "EMPRESA",
        data        = {
            "id":            empresa.pk,
            "nombre":        empresa.nombre,
            "nit":           empresa.nit,
            "email_contacto":empresa.email_contacto,
            "telefono":      empresa.telefono,
            "activo":        empresa.activo,
            "created_at":    empresa.created_at.isoformat(),
            "updated_at":    empresa.updated_at.isoformat(),
        },
    )


def upsert_reporte_empresa(reporte) -> None:
    dynamo.put_item(
        pk          = _pk(reporte.empresa_id),
        sk          = f"REPORT#{reporte.mes}",
        entity_type = "REPORTE_EMPRESA",
        data        = {
            "id":           reporte.pk,
            "empresa_id":   reporte.empresa_id,
            "mes":          reporte.mes,
            "costo_total":  str(reporte.costo_total),
            "moneda":       reporte.moneda,
            "detalle_json": reporte.detalle_json,
            "generado_en":  reporte.generado_en.isoformat(),
        },
    )


def delete_empresa(empresa_id: int) -> None:
    items = dynamo.query_by_pk(_pk(empresa_id))
    for item in items:
        dynamo.delete_item(pk=item["PK"], sk=item["SK"])
