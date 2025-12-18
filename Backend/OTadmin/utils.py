from datetime import date, datetime, timedelta

# Feriados fijos + Semana Santa para Guatemala 2023-2027
FERIADOS_GUATEMALA = {
    2023: {
        date(2023, 1, 1),
        date(2023, 5, 1),
        date(2023, 6, 30),
        date(2023, 8, 15),
        date(2023, 9, 15),
        date(2023, 10, 20),
        date(2023, 11, 1),
        date(2023, 12, 24),
        date(2023, 12, 25),
        date(2023, 12, 31),
        # Semana Santa 2023
        date(2023, 4, 6),  # Jueves Santo
        date(2023, 4, 7),  # Viernes Santo
        date(2023, 4, 8),  # Sábado Santo
    },
    2024: {
        date(2024, 1, 1),
        date(2024, 5, 1),
        date(2024, 6, 30),
        date(2024, 8, 15),
        date(2024, 9, 15),
        date(2024, 10, 20),
        date(2024, 11, 1),
        date(2024, 12, 24),
        date(2024, 12, 25),
        date(2024, 12, 31),
        # Semana Santa 2024
        date(2024, 3, 28),
        date(2024, 3, 29),
        date(2024, 3, 30),
    },
    2025: {
        date(2025, 1, 1),
        date(2025, 5, 1),
        date(2025, 6, 30),
        date(2025, 8, 15),
        date(2025, 9, 15),
        date(2025, 10, 20),
        date(2025, 11, 1),
        date(2025, 12, 24),
        date(2025, 12, 25),
        date(2025, 12, 31),
        # Semana Santa 2025
        date(2025, 4, 17),
        date(2025, 4, 18),
        date(2025, 4, 19),
    },
    2026: {
        date(2026, 1, 1),
        date(2026, 5, 1),
        date(2026, 6, 30),
        date(2026, 8, 15),
        date(2026, 9, 15),
        date(2026, 10, 20),
        date(2026, 11, 1),
        date(2026, 12, 24),
        date(2026, 12, 25),
        date(2026, 12, 31),
        # Semana Santa 2026
        date(2026, 4, 2),
        date(2026, 4, 3),
        date(2026, 4, 4),
    },
    2027: {
        date(2027, 1, 1),
        date(2027, 5, 1),
        date(2027, 6, 30),
        date(2027, 8, 15),
        date(2027, 9, 15),
        date(2027, 10, 20),
        date(2027, 11, 1),
        date(2027, 12, 24),
        date(2027, 12, 25),
        date(2027, 12, 31),
        # Semana Santa 2027
        date(2027, 3, 25),
        date(2027, 3, 26),
        date(2027, 3, 27),
    },
}


def es_feriado(d: date) -> bool:
    feriados = FERIADOS_GUATEMALA.get(d.year, set())
    return d in feriados


def dias_habiles(fecha_inicio, fecha_fin):

    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    if fecha_fin < fecha_inicio:
        return 0

    dias = 0
    actual = fecha_inicio

    # Usar solo la tabla oficial de feriados
    while actual <= fecha_fin:
        if actual.weekday() < 5 and not es_feriado(actual):
            dias += 1
        actual += timedelta(days=1)

    return dias