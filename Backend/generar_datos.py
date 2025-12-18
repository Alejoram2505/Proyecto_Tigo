from OTadmin.models import OT
from accounts.models import CustomUser
from datetime import datetime, timedelta
import random

print("Creando datos falsos...")

familias = ["CLOUD", "CIBER", "FIJO", "SDWAN", "UCASS", "VAS"]
segmentos = ["SMALL", "LARGE", "ENTERPRISE", "GOVERNMENT", "WHOLESALE", "MNC"]

ing, _ = CustomUser.objects.get_or_create(
    username="fake_ing",
    defaults={"nombre": "Ing", "apellido": "Prueba", "rol": "ing"}
)
ing.set_password("1234")
ing.save()

OT.objects.all().delete()

for i in range(120):
    fam = random.choice(familias)
    seg = random.choice(segmentos)

    fecha_ing = datetime.today() - timedelta(days=random.randint(10, 80))

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
        cliente=f"Cliente_{i}",
        producto=f"Producto_{fam}",
        familia=fam,
        ot=f"FAKE-{100000+i}",
        sol=f"S-{i}",
        producto_hijo="X",
        fecha_ingreso=fecha_ing,
        fecha_cierre=fecha_cierre,
        enlace_id=i,
        comercial="Comercial X",
        ing_encargado=ing
    )

print("LISTO. Datos falsos creados exitosamente.")
