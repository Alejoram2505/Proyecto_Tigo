from datetime import date, datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import OT
from .utils import dias_habiles


def _to_date(fecha):
    """Convierte datetime → date para evitar errores de comparación."""
    if isinstance(fecha, datetime):
        return fecha.date()
    return fecha


@receiver(pre_save, sender=OT)
def calcular_mtti_y_dias_cola(sender, instance: OT, **kwargs):
    """
    Calcula:
    - MTTI (solo si está cerrada)
    - días de cola al día de hoy (solo si NO está cerrada)
    """

    # Normalizar fechas (evita error: can't compare datetime.datetime to date)
    instance.fecha_ingreso = _to_date(instance.fecha_ingreso)
    instance.fecha_cierre = _to_date(instance.fecha_cierre)

    # Reset por si las fechas cambiaron
    instance.mtti = None
    instance.dias_cola_hoy = None

    # Estados que NO deben calcular días de cola
    estados_cerrados = ["cerrado", "cancelado"]

    # --- 1) MTTI (solo si cerrada)
    if instance.fecha_ingreso and instance.fecha_cierre:
        instance.mtti = dias_habiles(instance.fecha_ingreso, instance.fecha_cierre)

    # --- 2) Días de cola hoy (solo si no está cerrada)
    if instance.fecha_ingreso and instance.estado not in estados_cerrados:
        hoy = date.today()
        hoy = _to_date(hoy)
        instance.dias_cola_hoy = dias_habiles(instance.fecha_ingreso, hoy)
