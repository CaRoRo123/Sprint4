from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.serializers import EmpresaWriteSerializer, GenerarReporteInputSerializer
from app.cqrs import commands
from app.reports.cost_explorer import obtener_costo_mes


class CrearEmpresaView(APIView):
    """POST /api/empresas/crear/"""
    def post(self, request):
        serializer = EmpresaWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        empresa = commands.crear_empresa(serializer.validated_data)
        return Response({"id": empresa.pk, "mensaje": "Empresa creada correctamente"}, status=status.HTTP_201_CREATED)


class ActualizarEmpresaView(APIView):
    """PATCH /api/empresas/<pk>/actualizar/"""
    def patch(self, request, pk):
        serializer = EmpresaWriteSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            empresa = commands.actualizar_empresa(pk, serializer.validated_data)
        except Exception:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": empresa.pk, "mensaje": "Empresa actualizada"})


class EliminarEmpresaView(APIView):
    """DELETE /api/empresas/<pk>/eliminar/"""
    def delete(self, request, pk):
        try:
            commands.eliminar_empresa(pk)
        except Exception:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"mensaje": "Empresa eliminada"})


class GenerarReporteEmpresaView(APIView):
    """POST /api/empresas/<pk>/reportes/generar/  — body: { mes: "2024-01" }"""
    def post(self, request, pk):
        serializer = GenerarReporteInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mes = serializer.validated_data["mes"]
        try:
            datos_costo = obtener_costo_mes(mes)
        except Exception as e:
            return Response({"error": f"AWS Cost Explorer: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            reporte = commands.crear_reporte(pk, mes, datos_costo)
        except Exception:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id": reporte.pk, "mes": reporte.mes,
            "costo_total": str(reporte.costo_total), "moneda": reporte.moneda,
            "mensaje": "Reporte generado correctamente",
        }, status=status.HTTP_201_CREATED)
