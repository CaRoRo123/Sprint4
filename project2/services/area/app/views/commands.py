from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.serializers import AreaWriteSerializer, GenerarReporteInputSerializer
from app.cqrs import commands
from app.reports.cost_explorer import obtener_costo_mes


class CrearAreaView(APIView):
    """POST /api/areas/crear/"""
    def post(self, request):
        serializer = AreaWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        area = commands.crear_area(serializer.validated_data)
        return Response({"id": area.pk, "mensaje": "Área creada correctamente"}, status=status.HTTP_201_CREATED)


class ActualizarAreaView(APIView):
    """PATCH /api/areas/<pk>/actualizar/"""
    def patch(self, request, pk):
        serializer = AreaWriteSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            area = commands.actualizar_area(pk, serializer.validated_data)
        except Exception:
            return Response({"error": "Área no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": area.pk, "mensaje": "Área actualizada"})


class EliminarAreaView(APIView):
    """DELETE /api/areas/<pk>/eliminar/"""
    def delete(self, request, pk):
        try:
            commands.eliminar_area(pk)
        except Exception:
            return Response({"error": "Área no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"mensaje": "Área eliminada"})


class GenerarReporteAreaView(APIView):
    """POST /api/areas/<pk>/reportes/generar/  — body: { mes: "2024-01" }"""
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
            return Response({"error": "Área no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id": reporte.pk, "mes": reporte.mes,
            "costo_total": str(reporte.costo_total), "moneda": reporte.moneda,
            "mensaje": "Reporte generado correctamente",
        }, status=status.HTTP_201_CREATED)
