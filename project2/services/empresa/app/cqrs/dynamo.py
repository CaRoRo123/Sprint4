"""
Cliente DynamoDB — single-table design por servicio.

Estructura de claves:
┌───────────────────┬──────────────────────┬─────────────────────────┐
│ PK                │ SK                   │ Uso                     │
├───────────────────┼──────────────────────┼─────────────────────────┤
│ PROYECTO#<id>     │ METADATA             │ Datos del proyecto      │
│ PROYECTO#<id>     │ REPORT#2024-01       │ Reporte de ese mes      │
└───────────────────┴──────────────────────┴─────────────────────────┘

GSI `entity_type-index`:
  GSI_PK = entity_type  ("PROYECTO")
  GSI_SK = created_at   → permite listar todos los proyectos ordenados
"""
import boto3
from django.conf import settings


def _get_table():
    dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
    return dynamodb.Table(settings.DYNAMODB_TABLE)


# ── Escritura ─────────────────────────────────────────────────────────────────

def put_item(pk: str, sk: str, entity_type: str, data: dict) -> None:
    """Inserta o reemplaza un ítem en DynamoDB."""
    table = _get_table()
    item = {
        "PK":          pk,
        "SK":          sk,
        "entity_type": entity_type,
        **data,
    }
    table.put_item(Item=item)


def delete_item(pk: str, sk: str) -> None:
    table = _get_table()
    table.delete_item(Key={"PK": pk, "SK": sk})


# ── Lectura ───────────────────────────────────────────────────────────────────

def get_item(pk: str, sk: str) -> dict | None:
    """Devuelve un ítem por clave exacta o None si no existe."""
    table = _get_table()
    resp  = table.get_item(Key={"PK": pk, "SK": sk})
    return resp.get("Item")


def query_by_pk(pk: str, sk_prefix: str | None = None) -> list[dict]:
    """
    Devuelve todos los ítems de un PK dado.
    Si se pasa sk_prefix, filtra los SK que empiecen con ese prefijo.
    """
    from boto3.dynamodb.conditions import Key

    table      = _get_table()
    condition  = Key("PK").eq(pk)
    if sk_prefix:
        condition &= Key("SK").begins_with(sk_prefix)

    resp  = table.query(KeyConditionExpression=condition)
    return resp.get("Items", [])


def list_by_entity_type(entity_type: str) -> list[dict]:
    """
    Lista todos los ítems de un tipo usando el GSI entity_type-index.
    Devuelve solo los ítems con SK=METADATA (cabeceras, sin sub-ítems).
    """
    from boto3.dynamodb.conditions import Key

    table = _get_table()
    resp  = table.query(
        IndexName="entity_type-index",
        KeyConditionExpression=Key("entity_type").eq(entity_type),
    )
    return resp.get("Items", [])
