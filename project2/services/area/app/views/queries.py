from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.cqrs import queries


class ListarAreasView(APIView):
    """GET /api/areas/?empresa_id=1"""
    def get(self, request):
        empresa_id = request.query_params.get("empresa_id")
        areas = queries.listar_areas(empresa_id=empresa_id)
        return Response(areas)


class DetalleAreaView(APIView):
    """GET /api/areas/<pk>/"""
    def get(self, request, pk):
        area = queries.obtener_area(pk)
        if not area:
            return Response({"error": "Área no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response(area)


class ListarReportesAreaView(APIView):
    """GET /api/areas/<pk>/reportes/"""
    def get(self, request, pk):
        return Response(queries.listar_reportes(pk))


class ObtenerReporteAreaView(APIView):
    """GET /api/areas/<pk>/reportes/<mes>/"""
    def get(self, request, pk, mes):
        reporte = queries.obtener_reporte(pk, mes)
        if not reporte:
            return Response({"error": f"Sin reporte para {mes}"}, status=status.HTTP_404_NOT_FOUND)
        return Response(reporte)
