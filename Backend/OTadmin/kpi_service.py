# OTadmin/kpi_service.py
from datetime import date, timedelta

from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth

from .models import OT


def rango_default_30_dias():
    hoy = date.today()
    inicio = hoy - timedelta(days=30)
    return inicio, hoy


def _base_qs(fecha_inicio, fecha_fin):
    """
    QS base para KPIs:
    - Solo OT con fecha de cierre
    - Con MTTI calculado
    - Con familia y segmento
    """
    return (
        OT.objects
        .filter(
            fecha_cierre__isnull=False,
            fecha_cierre__range=(fecha_inicio, fecha_fin),
            mtti__isnull=False,
        )
        .exclude(familia__isnull=True)
        .exclude(familia__exact="")
        .exclude(segmento__isnull=True)
        .exclude(segmento__exact="")
    )


def kpi_familias(fecha_inicio, fecha_fin):
    qs = _base_qs(fecha_inicio, fecha_fin)

    data = (
        qs.values("familia")
        .annotate(
            total=Count("id"),
            mtti_promedio=Avg("mtti"),
        )
        .order_by("familia")
    )

    total_global = sum(item["total"] for item in data) or 1

    resultado = []
    for item in data:
        resultado.append({
            "familia": item["familia"],
            "total": item["total"],
            "mtti_promedio": round(item["mtti_promedio"] or 0, 2),
            "porcentaje": round(item["total"] * 100.0 / total_global, 2),
        })

    return resultado


def kpi_segmentos(fecha_inicio, fecha_fin):
    qs = _base_qs(fecha_inicio, fecha_fin)

    data = (
        qs.values("segmento")
        .annotate(
            total=Count("id"),
            mtti_promedio=Avg("mtti"),
        )
        .order_by("segmento")
    )

    total_global = sum(item["total"] for item in data) or 1

    resultado = []
    for item in data:
        resultado.append({
            "segmento": item["segmento"],
            "total": item["total"],
            "mtti_promedio": round(item["mtti_promedio"] or 0, 2),
            "porcentaje": round(item["total"] * 100.0 / total_global, 2),
        })

    return resultado


def kpi_histograma_familias(fecha_inicio, fecha_fin):
    """
    Distribución de MTTI por familia en rangos:
    0-8, 9-16, 17-20, >20
    """
    qs = _base_qs(fecha_inicio, fecha_fin)

    familias = (
        qs.values_list("familia", flat=True)
        .distinct()
        .order_by("familia")
    )

    resultado = []

    for fam in familias:
        f_qs = qs.filter(familia=fam)

        r_0_8 = 0
        r_9_16 = 0
        r_17_20 = 0
        r_mas_20 = 0

        for ot in f_qs:
            mtti = ot.mtti or 0
            if mtti <= 8:
                r_0_8 += 1
            elif mtti <= 16:
                r_9_16 += 1
            elif mtti <= 20:
                r_17_20 += 1
            else:
                r_mas_20 += 1

        resultado.append({
            "familia": fam,
            "rango_0_8": r_0_8,
            "rango_9_16": r_9_16,
            "rango_17_20": r_17_20,
            "rango_mas_20": r_mas_20,
        })

    return resultado


def kpi_cierres_temporales(fecha_inicio, fecha_fin):
    """
    Cierres agrupados por mes (YYYY-MM) con total y MTTI promedio.
    """
    qs = _base_qs(fecha_inicio, fecha_fin)

    data = (
        qs.annotate(periodo=TruncMonth("fecha_cierre"))
        .values("periodo")
        .annotate(
            total=Count("id"),
            mtti_promedio=Avg("mtti"),
        )
        .order_by("periodo")
    )

    resultado = []
    for item in data:
        periodo = item["periodo"]
        etiqueta = periodo.strftime("%Y-%m")
        resultado.append({
            "periodo": etiqueta,
            "total": item["total"],
            "mtti_promedio": round(item["mtti_promedio"] or 0, 2),
        })

    return resultado


def kpi_globales(fecha_inicio, fecha_fin):
    qs = _base_qs(fecha_inicio, fecha_fin)

    total = qs.count()
    mtti_promedio = qs.aggregate(avg=Avg("mtti"))["avg"] or 0

    return {
        "total_ot_cerradas": total,
        "mtti_promedio": round(mtti_promedio, 2),
    }
