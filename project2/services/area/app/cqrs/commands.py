from app.models import Area, ReporteArea


def crear_area(data: dict) -> Area:
    return Area.objects.create(**data)


def actualizar_area(area_id: int, data: dict) -> Area:
    area = Area.objects.get(pk=area_id)
    for campo, valor in data.items():
        setattr(area, campo, valor)
    area.save()
    return area


def eliminar_area(area_id: int) -> None:
    from app.cqrs.sync import delete_area
    area = Area.objects.get(pk=area_id)
    area.activo = False
    area.save()
    delete_area(area_id)


def crear_reporte(area_id: int, mes: str, datos_costo: dict) -> ReporteArea:
    area = Area.objects.get(pk=area_id)
    reporte, _ = ReporteArea.objects.update_or_create(
        area=area,
        mes=mes,
        defaults={
            "costo_total":  datos_costo.get("total", 0),
            "moneda":       datos_costo.get("moneda", "USD"),
            "detalle_json": datos_costo.get("detalle", {}),
        },
    )
    return reporte
