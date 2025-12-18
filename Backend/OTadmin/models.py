from django.db import models
from accounts.models import CustomUser
import unicodedata
import re

class OT(models.Model):
    ESTADOS = (
        ("abierto", "Abierto"),
        ("pospuesto", "Pospuesto"),
        ("cancelado", "Cancelado"),
        ("cerrado", "Cerrado"),
    )

    segmento = models.CharField(max_length=100)
    cliente = models.CharField(max_length=200)
    producto = models.CharField(max_length=200)
    ot = models.CharField(max_length=100, unique=True)  # SR_NO_INSTALACION
    req = models.CharField(max_length=200, blank=True, null=True)
    sol = models.CharField(max_length=200, blank=True, null=True)
    producto_hijo = models.CharField(max_length=200, blank=True, null=True)
    fecha_ingreso = models.DateField()
    fecha_estimada = models.BooleanField(default=False)
    enlace_id = models.CharField(max_length=200)
    ing_encargado = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    comercial = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="abierto")
    fecha_cierre = models.DateField(blank=True, null=True)
    familia = models.CharField(max_length=100, blank=True, null=True)
    cliente_normalizado = models.CharField(max_length=200, blank=True, null=True)
    mtti = models.IntegerField(null=True, blank=True)
    dias_cola_hoy = models.IntegerField(null=True, blank=True)

    # días de cola no se guarda, se calcula
    def dias_cola(self):
        from datetime import date, timedelta

        hoy = date.today()
        dias = 0
        fecha_actual = self.fecha_ingreso

        while fecha_actual < hoy:
            if fecha_actual.weekday() < 5:  # 0–4 = Lunes a Viernes
                dias += 1
            fecha_actual += timedelta(days=1)

        return dias

    def color_cola(self):
        d = self.dias_cola()
        if d <= 10:
            return "green"
        elif d <= 20:
            return "yellow"
        return "red"

    def __str__(self):
        return f"OT {self.ot} - {self.cliente}"
    
    
class Comentario(models.Model):
    ot = models.ForeignKey(OT, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey("accounts.CustomUser", on_delete=models.SET_NULL, null=True)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Comentario en OT {self.ot.ot} por {self.usuario}"

class SegmentoCliente(models.Model):
    cliente = models.CharField(max_length=200, unique=True)
    cliente_normalizado = models.CharField(max_length=200, unique=True)
    segmento = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.cliente} → {self.segmento}"


def normalizar_texto(txt):
    if not txt:
        return ""
    txt = str(txt).lower().strip()
    
    # quitar acentos
    txt = ''.join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )

    # quitar caracteres raros
    txt = re.sub(r'[^a-z0-9 ]', '', txt)

    # quitar dobles espacios
    txt = re.sub(r'\s+', ' ', txt)
    
    return txt