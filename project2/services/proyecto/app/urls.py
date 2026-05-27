from django.urls import path
from app.views.commands import CrearProyectoView, ActualizarProyectoView, EliminarProyectoView, GenerarReporteView
from app.views.queries  import ListarProyectosView, DetalleProyectoView, ListarReportesView, ObtenerReporteView

urlpatterns = [
    # ── COMMANDS (write → Aurora → sync DynamoDB) ────────────────────────────
    path("crear/",                          CrearProyectoView.as_view(),    name="proyectos-crear"),
    path("<int:pk>/actualizar/",            ActualizarProyectoView.as_view(),name="proyectos-actualizar"),
    path("<int:pk>/eliminar/",              EliminarProyectoView.as_view(), name="proyectos-eliminar"),
    path("<int:pk>/reportes/generar/",      GenerarReporteView.as_view(),   name="reportes-generar"),
    
    # ── QUERIES (read → DynamoDB) ────────────────────────────────────────────
    path("",                                ListarProyectosView.as_view(),  name="proyectos-list"),
    path("<int:pk>/",                       DetalleProyectoView.as_view(),  name="proyectos-detalle"),
    path("<int:pk>/reportes/",              ListarReportesView.as_view(),   name="reportes-list"),
    path("<int:pk>/reportes/<str:mes>/",    ObtenerReporteView.as_view(),   name="reportes-mes"),

    
]
