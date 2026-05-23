import logging

logger = logging.getLogger(__name__)

def upsert_proyecto(proyecto_instance):
    """
    [Read Side] Próximamente: Sincronizar con DynamoDB.
    Por ahora solo simula la recepción del evento.
    """
    logger.info(f"[CQRS Sync] Proyecto detectado: {proyecto_instance.nombre} (ID: {proyecto_instance.id}). Listo para enviar a DynamoDB.")
    # Aquí irá tu boto3 cuando configures AWS
    pass

def upsert_reporte_proyecto(reporte_instance):
    """
    [Read Side] Próximamente: Sincronizar reporte de costos con DynamoDB.
    """
    logger.info(f"[CQRS Sync] Reporte detectado para el mes: {reporte_instance.mes}. Listo para enviar a DynamoDB.")
    # Aquí irá tu boto3 cuando configures AWS
    pass