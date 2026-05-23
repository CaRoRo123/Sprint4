"""
views/commands.py — Endpoints que mutan estado.
Usan el comando correspondiente, que escribe en Aurora.
La señal post_save propaga el cambio a DynamoDB automáticamente.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.serializers import ProyectoWriteSerializer, GenerarReporteInputSerializer
from app.cqrs import commands
from app.reports.cost_explorer import obtener_costo_mes


class CrearProyectoView(APIView):
    """
    POST /api/proyectos/crear/
    Body: { nombre, descripcion, fecha_inicio, fecha_fin, empresa_id, area_id }
    Crea el Proyecto en Aurora. La señal post_save sincroniza DynamoDB.
    """
    def post(self, request):
        serializer = ProyectoWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        proyecto = commands.crear_proyecto(serializer.validated_data)
        return Response(
            {"id": proyecto.pk, "mensaje": "Proyecto creado correctamente"},
            status=status.HTTP_201_CREATED,
        )


class ActualizarProyectoView(APIView):
    """
    PATCH /api/proyectos/<pk>/actualizar/
    Actualiza campos en Aurora → sincroniza DynamoDB.
    """
    def patch(self, request, pk):
        serializer = ProyectoWriteSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            proyecto = commands.actualizar_proyecto(pk, serializer.validated_data)
        except Exception:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"id": proyecto.pk, "mensaje": "Proyecto actualizado"})


class EliminarProyectoView(APIView):
    """
    DELETE /api/proyectos/<pk>/eliminar/
    Soft-delete en Aurora + elimina nodo de DynamoDB.
    """
    def delete(self, request, pk):
        try:
            commands.eliminar_proyecto(pk)
        except Exception:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"mensaje": "Proyecto eliminado"}, status=status.HTTP_200_OK)


class GenerarReporteView(APIView):
    """
    POST /api/proyectos/<pk>/reportes/generar/
    Body: { "mes": "2024-01" }

    1. Llama a AWS Cost Explorer para obtener el gasto del mes.
    2. Persiste el ReporteProyecto en Aurora (upsert).
    3. La señal post_save proyecta el reporte a DynamoDB.
    """
    def post(self, request, pk):
        serializer = GenerarReporteInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mes = serializer.validated_data["mes"]

        # Llamar a AWS Cost Explorer
        try:
            datos_costo = obtener_costo_mes(mes)
        except Exception as e:
            return Response(
                {"error": f"No se pudo consultar AWS Cost Explorer: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Persistir en Aurora (y auto-sync a DynamoDB vía señal)
        try:
            reporte = commands.crear_reporte(pk, mes, datos_costo)
        except Exception:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "id":          reporte.pk,
                "mes":         reporte.mes,
                "costo_total": str(reporte.costo_total),
                "moneda":      reporte.moneda,
                "mensaje":     "Reporte generado y almacenado correctamente",
            },
            status=status.HTTP_201_CREATED,
        )
