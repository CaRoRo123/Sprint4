from app.cqrs import dynamo


def listar_areas(empresa_id: int = None) -> list[dict]:
    items = dynamo.list_by_entity_type("AREA")
    areas = [i for i in items if i.get("activo", True)]
    if empresa_id:
        areas = [a for a in areas if str(a.get("empresa_id")) == str(empresa_id)]
    return areas


def obtener_area(area_id: int) -> dict | None:
    return dynamo.get_item(pk=f"AREA#{area_id}", sk="METADATA")


def listar_reportes(area_id: int) -> list[dict]:
    items = dynamo.query_by_pk(pk=f"AREA#{area_id}", sk_prefix="REPORT#")
    return sorted(items, key=lambda x: x["mes"], reverse=True)


def obtener_reporte(area_id: int, mes: str) -> dict | None:
    return dynamo.get_item(pk=f"AREA#{area_id}", sk=f"REPORT#{mes}")
