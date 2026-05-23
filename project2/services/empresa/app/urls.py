from django.urls import path
from app.views.commands import CrearEmpresaView, ActualizarEmpresaView, EliminarEmpresaView, GenerarReporteEmpresaView
from app.views.queries  import ListarEmpresasView, DetalleEmpresaView, ListarReportesEmpresaView, ObtenerReporteEmpresaView

urlpatterns = [
    # ── QUERIES (read → DynamoDB) ────────────────────────────────────────────
    path("",                             ListarEmpresasView.as_view(),         name="empresas-list"),
    path("<int:pk>/",                    DetalleEmpresaView.as_view(),          name="empresas-detalle"),
    path("<int:pk>/reportes/",           ListarReportesEmpresaView.as_view(),   name="reportes-empresa-list"),
    path("<int:pk>/reportes/<str:mes>/", ObtenerReporteEmpresaView.as_view(),   name="reportes-empresa-mes"),

    # ── COMMANDS (write → Aurora → sync DynamoDB) ────────────────────────────
    path("crear/",                       CrearEmpresaView.as_view(),            name="empresas-crear"),
    path("<int:pk>/actualizar/",         ActualizarEmpresaView.as_view(),       name="empresas-actualizar"),
    path("<int:pk>/eliminar/",           EliminarEmpresaView.as_view(),         name="empresas-eliminar"),
    path("<int:pk>/reportes/generar/",   GenerarReporteEmpresaView.as_view(),   name="reportes-empresa-generar"),
]
