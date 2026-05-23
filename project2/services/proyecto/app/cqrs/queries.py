"""
queries.py — Read side del CQRS.
Toda consulta lee de DynamoDB, nunca de Aurora.
"""
from app.cqrs import dynamo


def listar_proyectos() -> list[dict]:
    """Lista todos los proyectos activos desde DynamoDB (GSI entity_type-index)."""
    items = dynamo.list_by_entity_type("PROYECTO")
    return [i for i in items if i.get("activo", True)]


def obtener_proyecto(proyecto_id: int) -> dict | None:
    """Devuelve los metadatos de un proyecto desde DynamoDB."""
    return dynamo.get_item(pk=f"PROYECTO#{proyecto_id}", sk="METADATA")


def listar_reportes(proyecto_id: int) -> list[dict]:
    """Devuelve todos los reportes de un proyecto desde DynamoDB."""
    items = dynamo.query_by_pk(
        pk        = f"PROYECTO#{proyecto_id}",
        sk_prefix = "REPORT#",
    )
    return sorted(items, key=lambda x: x["mes"], reverse=True)


def obtener_reporte(proyecto_id: int, mes: str) -> dict | None:
    """Devuelve el reporte de un mes específico desde DynamoDB."""
    return dynamo.get_item(
        pk=f"PROYECTO#{proyecto_id}",
        sk=f"REPORT#{mes}",
    )
