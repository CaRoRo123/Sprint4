"""
cost_explorer.py — Consulta AWS Cost Explorer para obtener el gasto de un mes.

Uso:
    from app.reports.cost_explorer import obtener_costo_mes
    datos = obtener_costo_mes("2024-01")

Devuelve un dict con:
  {
    "total":   143.27,          # costo total del mes en USD
    "moneda":  "USD",
    "detalle": { ... }          # respuesta completa de AWS CE (servicios desglosados)
  }

Nota: el IAM role del EC2 debe tener permiso ce:GetCostAndUsage.
"""
import calendar
from datetime import date
import boto3
from django.conf import settings


def _rango_mes(mes: str) -> tuple[str, str]:
    """
    Convierte "2024-01" → ("2024-01-01", "2024-02-01").
    AWS Cost Explorer usa rango [start, end) — end es el primer día del mes siguiente.
    """
    anio, num_mes = int(mes[:4]), int(mes[5:7])
    inicio = date(anio, num_mes, 1)

    # Primer día del mes siguiente
    if num_mes == 12:
        fin = date(anio + 1, 1, 1)
    else:
        fin = date(anio, num_mes + 1, 1)

    return str(inicio), str(fin)


def obtener_costo_mes(mes: str) -> dict:
    """
    Llama a AWS Cost Explorer y devuelve el gasto total + desglose por servicio.

    Args:
        mes: Mes en formato "YYYY-MM" (ej: "2024-01")

    Returns:
        {
            "total":   float,
            "moneda":  str,
            "detalle": {
                "periodo":   { "inicio": str, "fin": str },
                "total_usd": str,
                "servicios": [
                    { "nombre": str, "costo": str, "unidad": str }
                ]
            }
        }
    """
    inicio, fin = _rango_mes(mes)

    client = boto3.client("ce", region_name="us-east-1")  # CE solo existe en us-east-1

    respuesta = client.get_cost_and_usage(
        TimePeriod={"Start": inicio, "End": fin},
        Granularity="MONTHLY",
        Metrics=["BlendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    # Extraer resultados
    resultados = respuesta.get("ResultsByTime", [])
    if not resultados:
        return {"total": 0, "moneda": "USD", "detalle": {}}

    periodo_dato = resultados[0]
    total_obj    = periodo_dato.get("Total", {}).get("BlendedCost", {})
    total_usd    = float(total_obj.get("Amount", 0))
    moneda       = total_obj.get("Unit", "USD")

    # Desglose por servicio
    servicios = []
    for grupo in periodo_dato.get("Groups", []):
        nombre = grupo["Keys"][0] if grupo.get("Keys") else "Desconocido"
        costo  = grupo.get("Metrics", {}).get("BlendedCost", {})
        servicios.append({
            "nombre": nombre,
            "costo":  costo.get("Amount", "0"),
            "unidad": costo.get("Unit", "USD"),
        })

    # Ordenar por costo descendente
    servicios.sort(key=lambda s: float(s["costo"]), reverse=True)

    return {
        "total":  round(total_usd, 4),
        "moneda": moneda,
        "detalle": {
            "periodo":   {"inicio": inicio, "fin": fin},
            "total_usd": str(round(total_usd, 4)),
            "servicios": servicios,
        },
    }
