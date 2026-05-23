from rest_framework.views import APIView
from app.serializers import AreaSerializer, AreaWriteSerializer, ReporteAreaSerializer


class ListarAreasView(APIView):
    def get(self, request):
        # TODO: listar áreas con filtro opcional por empresa_id
        pass


class CrearAreaView(APIView):
    def post(self, request):
        # TODO: crear área
        pass


class DetalleAreaView(APIView):
    def get(self, request, pk):
        # TODO: detalle de área con reportes
        pass


class ActualizarAreaView(APIView):
    def patch(self, request, pk):
        # TODO: actualizar área
        pass


class EliminarAreaView(APIView):
    def delete(self, request, pk):
        # TODO: soft-delete
        pass


class CrearReporteAreaView(APIView):
    def post(self, request, pk):
        # TODO: crear reporte de área
        pass


class ListarReportesAreaView(APIView):
    def get(self, request, pk):
        # TODO: historial de reportes
        pass
