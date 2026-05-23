from app.cqrs import dynamo


def listar_empresas() -> list[dict]:
    items = dynamo.list_by_entity_type("EMPRESA")
    return [i for i in items if i.get("activo", True)]


def obtener_empresa(empresa_id: int) -> dict | None:
    return dynamo.get_item(pk=f"EMPRESA#{empresa_id}", sk="METADATA")


def listar_reportes(empresa_id: int) -> list[dict]:
    items = dynamo.query_by_pk(pk=f"EMPRESA#{empresa_id}", sk_prefix="REPORT#")
    return sorted(items, key=lambda x: x["mes"], reverse=True)


def obtener_reporte(empresa_id: int, mes: str) -> dict | None:
    return dynamo.get_item(pk=f"EMPRESA#{empresa_id}", sk=f"REPORT#{mes}")
