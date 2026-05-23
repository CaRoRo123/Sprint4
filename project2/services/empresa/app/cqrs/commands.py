from app.models import Empresa, ReporteEmpresa


def crear_empresa(data: dict) -> Empresa:
    return Empresa.objects.create(**data)


def actualizar_empresa(empresa_id: int, data: dict) -> Empresa:
    empresa = Empresa.objects.get(pk=empresa_id)
    for campo, valor in data.items():
        setattr(empresa, campo, valor)
    empresa.save()
    return empresa


def eliminar_empresa(empresa_id: int) -> None:
    from app.cqrs.sync import delete_empresa
    empresa = Empresa.objects.get(pk=empresa_id)
    empresa.activo = False
    empresa.save()
    delete_empresa(empresa_id)


def crear_reporte(empresa_id: int, mes: str, datos_costo: dict) -> ReporteEmpresa:
    empresa = Empresa.objects.get(pk=empresa_id)
    reporte, _ = ReporteEmpresa.objects.update_or_create(
        empresa=empresa,
        mes=mes,
        defaults={
            "costo_total":  datos_costo.get("total", 0),
            "moneda":       datos_costo.get("moneda", "USD"),
            "detalle_json": datos_costo.get("detalle", {}),
        },
    )
    return reporte
