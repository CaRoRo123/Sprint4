from rest_framework.views import APIView
from app.serializers import EmpresaSerializer, EmpresaWriteSerializer, ReporteEmpresaSerializer


class ListarEmpresasView(APIView):
    def get(self, request):
        # TODO: listar empresas
        pass


class CrearEmpresaView(APIView):
    def post(self, request):
        # TODO: crear empresa
        pass


class DetalleEmpresaView(APIView):
    def get(self, request, pk):
        # TODO: detalle de empresa con reportes
        pass


class ActualizarEmpresaView(APIView):
    def patch(self, request, pk):
        # TODO: actualizar empresa
        pass


class EliminarEmpresaView(APIView):
    def delete(self, request, pk):
        # TODO: soft-delete
        pass


class CrearReporteEmpresaView(APIView):
    def post(self, request, pk):
        # TODO: crear reporte
        pass


class ListarReportesEmpresaView(APIView):
    def get(self, request, pk):
        # TODO: historial de reportes
        pass
