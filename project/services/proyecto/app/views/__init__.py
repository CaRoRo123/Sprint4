from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers import ProyectoSerializer, ProyectoWriteSerializer, ReporteProyectoSerializer


# ─── CQRS: COMMAND SIDE ─────────────────────────────────────────────────────

class CrearProyectoView(APIView):
    """POST /api/proyectos/ — crea un proyecto nuevo."""

    def post(self, request):
        # TODO: implementar lógica de creación
        pass


class ActualizarProyectoView(APIView):
    """PATCH /api/proyectos/<pk>/ — actualiza un proyecto existente."""

    def patch(self, request, pk):
        # TODO: implementar lógica de actualización
        pass


class EliminarProyectoView(APIView):
    """DELETE /api/proyectos/<pk>/ — elimina (soft-delete) un proyecto."""

    def delete(self, request, pk):
        # TODO: implementar soft-delete
        pass


# ─── CQRS: QUERY SIDE ───────────────────────────────────────────────────────

class ListarProyectosView(APIView):
    """GET /api/proyectos/ — lista proyectos con filtros opcionales."""

    def get(self, request):
        # TODO: implementar listado con filtros (empresa_id, area_id, activo)
        # Sugerencia: cachear resultado en Redis con django_redis
        pass


class DetalleProyectoView(APIView):
    """GET /api/proyectos/<pk>/ — detalle de un proyecto con sus reportes."""

    def get(self, request, pk):
        # TODO: implementar detalle + reportes anidados
        pass


# ─── REPORTES ────────────────────────────────────────────────────────────────

class CrearReporteView(APIView):
    """POST /api/proyectos/<pk>/reportes/ — genera un reporte de estado."""

    def post(self, request, pk):
        # TODO: implementar creación de reporte (append-only)
        pass


class ListarReportesView(APIView):
    """GET /api/proyectos/<pk>/reportes/ — historial de reportes."""

    def get(self, request, pk):
        # TODO: implementar listado de reportes
        pass
