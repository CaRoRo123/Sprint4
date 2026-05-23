from django.urls import path
from app.views import (
    ListarProyectosView,
    CrearProyectoView,
    DetalleProyectoView,
    ActualizarProyectoView,
    EliminarProyectoView,
    CrearReporteView,
    ListarReportesView,
)

urlpatterns = [
    # Comandos + Queries sobre Proyecto
    path("",           ListarProyectosView.as_view(),    name="proyectos-list"),
    path("crear/",     CrearProyectoView.as_view(),      name="proyectos-crear"),
    path("<int:pk>/",  DetalleProyectoView.as_view(),    name="proyectos-detalle"),
    path("<int:pk>/actualizar/", ActualizarProyectoView.as_view(), name="proyectos-actualizar"),
    path("<int:pk>/eliminar/",   EliminarProyectoView.as_view(),   name="proyectos-eliminar"),

    # Reportes (sub-recurso)
    path("<int:pk>/reportes/",        ListarReportesView.as_view(), name="reportes-list"),
    path("<int:pk>/reportes/crear/",  CrearReporteView.as_view(),   name="reportes-crear"),
]
