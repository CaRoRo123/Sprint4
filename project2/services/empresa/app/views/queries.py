from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.cqrs import queries


class ListarEmpresasView(APIView):
    """GET /api/empresas/"""
    def get(self, request):
        return Response(queries.listar_empresas())


class DetalleEmpresaView(APIView):
    """GET /api/empresas/<pk>/"""
    def get(self, request, pk):
        empresa = queries.obtener_empresa(pk)
        if not empresa:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response(empresa)


class ListarReportesEmpresaView(APIView):
    """GET /api/empresas/<pk>/reportes/"""
    def get(self, request, pk):
        return Response(queries.listar_reportes(pk))


class ObtenerReporteEmpresaView(APIView):
    """GET /api/empresas/<pk>/reportes/<mes>/"""
    def get(self, request, pk, mes):
        reporte = queries.obtener_reporte(pk, mes)
        if not reporte:
            return Response({"error": f"Sin reporte para {mes}"}, status=status.HTTP_404_NOT_FOUND)
        return Response(reporte)
