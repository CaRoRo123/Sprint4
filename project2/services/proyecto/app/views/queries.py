"""
views/queries.py — Endpoints de solo lectura.
Leen SIEMPRE de DynamoDB, nunca tocan Aurora directamente.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.cqrs import queries


class ListarProyectosView(APIView):
    """
    GET /api/proyectos/
    Lee la lista de proyectos desde DynamoDB (GSI entity_type-index).
    """
    def get(self, request):
        proyectos = queries.listar_proyectos()
        return Response(proyectos)


class DetalleProyectoView(APIView):
    """
    GET /api/proyectos/<pk>/
    Lee los metadatos del proyecto desde DynamoDB.
    """
    def get(self, request, pk):
        proyecto = queries.obtener_proyecto(pk)
        if not proyecto:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(proyecto)


class ListarReportesView(APIView):
    """
    GET /api/proyectos/<pk>/reportes/
    Lista todos los reportes de costos AWS del proyecto, desde DynamoDB.
    """
    def get(self, request, pk):
        reportes = queries.listar_reportes(pk)
        return Response(reportes)


class ObtenerReporteView(APIView):
    """
    GET /api/proyectos/<pk>/reportes/<mes>/
    Devuelve el reporte de un mes específico (ej: 2024-01) desde DynamoDB.
    """
    def get(self, request, pk, mes):
        reporte = queries.obtener_reporte(pk, mes)
        if not reporte:
            return Response(
                {"error": f"No hay reporte para el mes {mes}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(reporte)
