from OTadmin.models import OT
from accounts.models import CustomUser
from datetime import datetime, timedelta
import random

print("Creando nuevas OTs falsas...")

# Familias reales
familias = ["CLOUD", "CIBER", "FIJO", "SDWAN", "UCASS", "VAS"]

# Segmentos reales
segmentos = ["SMALL", "LARGE", "ENTERPRISE", "GOVERNMENT", "WHOLESALE", "MNC"]

# Crear ingeniero fake
ing, _ = CustomUser.objects.get_or_create(
    username="fake_ing2",
    defaults={"nombre": "Ing", "apellido": "Demo", "rol": "ing"}
)
ing.set_password("1234")
ing.save()

# ------------------------
# Crear 100 OTs CERRADAS
# ------------------------
for i in range(100):
    fam = random.choice(familias)
    seg = random.choice(segmentos)

    # Fecha ingreso entre últimos 120 días
    fecha_ing = datetime.today().date() - timedelta(days=random.randint(20, 120))

    # MTTI simulado con rangos similares a tus métricas reales
    r = random.random()
    if r < 0.30:
        dias = random.randint(1, 8)
    elif r < 0.60:
        dias = random.randint(9, 16)
    elif r < 0.80:
        dias = random.randint(17, 20)
    else:
        dias = random.randint(21, 40)

    fecha_cierre = fecha_ing + timedelta(days=dias)

    OT.objects.create(
        segmento=seg,
        cliente=f"Cliente_Cerrado_{i}",
        producto=f"Producto_{fam}",
        familia=fam,
        ot=f"FAKE-C-{10000+i}",
        sol=f"S-{i}",
        producto_hijo="X",
        fecha_ingreso=fecha_ing,
        fecha_cierre=fecha_cierre,
        enlace_id=i,
        comercial="Comercial X",
        estado="cerrado",
        ing_encargado=ing
    )

# ------------------------
# Crear 50 OTs ABIERTAS
# ------------------------
for i in range(50):
    fam = random.choice(familias)
    seg = random.choice(segmentos)

    # Fechas de ingreso recientes para días de cola
    fecha_ing = datetime.today().date() - timedelta(days=random.randint(1, 40))

    OT.objects.create(
        segmento=seg,
        cliente=f"Cliente_Abierto_{i}",
        producto=f"Producto_{fam}",
        familia=fam,
        ot=f"FAKE-A-{20000+i}",
        sol=f"S-A-{i}",
        producto_hijo="X",
        fecha_ingreso=fecha_ing,
        fecha_cierre=None,
        enlace_id=i + 500,
        comercial="Comercial X",
        estado="abierto",
        ing_encargado=ing
    )

print("✔ LISTO — Se crearon 100 OTs cerradas y 50 abiertas correctamente.")
