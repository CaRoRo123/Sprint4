from django.urls import path
from app.views import (
    ListarEmpresasView, CrearEmpresaView, DetalleEmpresaView,
    ActualizarEmpresaView, EliminarEmpresaView,
    CrearReporteEmpresaView, ListarReportesEmpresaView,
)

urlpatterns = [
    path("",                          ListarEmpresasView.as_view(),        name="empresas-list"),
    path("crear/",                    CrearEmpresaView.as_view(),           name="empresas-crear"),
    path("<int:pk>/",                 DetalleEmpresaView.as_view(),         name="empresas-detalle"),
    path("<int:pk>/actualizar/",      ActualizarEmpresaView.as_view(),      name="empresas-actualizar"),
    path("<int:pk>/eliminar/",        EliminarEmpresaView.as_view(),        name="empresas-eliminar"),
    path("<int:pk>/reportes/",        ListarReportesEmpresaView.as_view(),  name="reportes-empresa-list"),
    path("<int:pk>/reportes/crear/",  CrearReporteEmpresaView.as_view(),    name="reportes-empresa-crear"),
]
