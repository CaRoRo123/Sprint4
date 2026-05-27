from django.urls import path
from app.views.commands import CrearAreaView, ActualizarAreaView, EliminarAreaView, GenerarReporteAreaView
from app.views.queries  import ListarAreasView, DetalleAreaView, ListarReportesAreaView, ObtenerReporteAreaView

urlpatterns = [
    path("crear/",                       CrearAreaView.as_view(),           name="areas-crear"),
    path("<int:pk>/actualizar/",         ActualizarAreaView.as_view(),      name="areas-actualizar"),
    path("<int:pk>/eliminar/",           EliminarAreaView.as_view(),        name="areas-eliminar"),
    path("<int:pk>/reportes/generar/",   GenerarReporteAreaView.as_view(),  name="reportes-area-generar"),

    path("",                             ListarAreasView.as_view(),        name="areas-list"),
    path("<int:pk>/",                    DetalleAreaView.as_view(),         name="areas-detalle"),
    path("<int:pk>/reportes/",           ListarReportesAreaView.as_view(),  name="reportes-area-list"),
    path("<int:pk>/reportes/<str:mes>/", ObtenerReporteAreaView.as_view(),  name="reportes-area-mes"),

    ]
