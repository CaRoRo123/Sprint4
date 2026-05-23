from django.urls import path
from app.views import (
    ListarAreasView, CrearAreaView, DetalleAreaView,
    ActualizarAreaView, EliminarAreaView,
    CrearReporteAreaView, ListarReportesAreaView,
)

urlpatterns = [
    path("",                          ListarAreasView.as_view(),       name="areas-list"),
    path("crear/",                    CrearAreaView.as_view(),          name="areas-crear"),
    path("<int:pk>/",                 DetalleAreaView.as_view(),        name="areas-detalle"),
    path("<int:pk>/actualizar/",      ActualizarAreaView.as_view(),     name="areas-actualizar"),
    path("<int:pk>/eliminar/",        EliminarAreaView.as_view(),       name="areas-eliminar"),
    path("<int:pk>/reportes/",        ListarReportesAreaView.as_view(), name="reportes-area-list"),
    path("<int:pk>/reportes/crear/",  CrearReporteAreaView.as_view(),   name="reportes-area-crear"),
]
