import pandas as pd
from django.shortcuts import render
from .models import OT
from datetime import datetime, timedelta

def parsear_fecha(valor):
    """
    Devuelve una fecha válida o None.
    """

    if pd.isna(valor) or valor is None:
        return None

    # 1. Si es número de Excel
    if isinstance(valor, (int, float)):
        try:
            return datetime(1899, 12, 30) + timedelta(days=int(valor))
        except:
            pass

    # 2. Intentos comunes
    posibles_formatos = [
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%y",
        "%m/%d/%y",
    ]

    for formato in posibles_formatos:
        try:
            return datetime.strptime(str(valor), formato)
        except:
            continue

    # 3. Parser automático final
    try:
        f = pd.to_datetime(valor, errors="coerce")
        if pd.isna(f):
            return None
        return f.to_pydatetime()
    except:
        return None


def subir_backlog(request):
    if request.method == "POST":
        archivo = request.FILES.get("archivo")

        if not archivo:
            return render(request, "subir_backlog.html", {"error": "No se seleccionó archivo."})

        try:
            # Leer sin headers
            df_raw = pd.read_excel(archivo, header=None)

            # Detectar fila donde está el encabezado real
            header_row = df_raw[df_raw.apply(
                lambda row: row.astype(str).str.contains('SR_NO_INSTALACION').any(),
                axis=1
            )].index[0]

            # Leer Excel usando esa fila como encabezado
            df = pd.read_excel(archivo, header=header_row)

            # Normalizar columnas
            df.columns = df.columns.str.strip().str.upper()

            # Validar columna GRUPO
            if "GRUPO" not in df.columns:
                return render(request, "subir_backlog.html", {
                    "error": f"Error: no se encontró columna GRUPO. Detectadas: {list(df.columns)}"
                })

            # Filtrar solo backlog del grupo correcto
            df = df[df["GRUPO"] == "VAS IMPLEMENTATION"]

            agregadas = 0
            ignoradas = 0
            duplicadas = []

            for index, row in df.iterrows():
                ot_num = row.get("SR_NO_INSTALACION")

                if pd.isna(ot_num):
                    continue

                if OT.objects.filter(ot=ot_num).exists():
                    ignoradas += 1
                    duplicadas.append(f"Fila {index + 1} → OT {ot_num}")
                    continue


                # Usar el parser personalizado
                fecha = parsear_fecha(row.get("FECHA_LIBERACION"))
                fecha_estimada = False

                # Si no tiene fecha, asignar fecha actual automáticamente
                if fecha is None:
                    fecha = datetime.today()
                    fecha_estimada = True


                OT.objects.create(
                    segmento=row.get("SEGMENTO_CLIENTE", ""),
                    cliente=row.get("CLIENTE_NOMBRE", ""),
                    producto=row.get("PRODUCTO", ""),
                    ot=row.get("SR_NO_INSTALACION", ""),
                    sol=row.get("ID_SOLUCION", ""),
                    producto_hijo=row.get("SUB_PRODUCTO", ""),
                    fecha_ingreso=fecha,
                    fecha_estimada=fecha_estimada,
                    enlace_id=row.get("NUMERO_DE_ENLACE"),
                    comercial=row.get("SR_USUARIO_CREADOR", ""),
                )

                agregadas += 1

            return render(request, "subir_backlog.html", {
                "ok": f"OT agregadas: {agregadas}, OT duplicadas ignoradas: {ignoradas}",
                "duplicadas": duplicadas
            })

        except Exception as e:
            return render(request, "subir_backlog.html", {
                "error": f"Error al procesar archivo: {str(e)}"
            })

    return render(request, "subir_backlog.html")




## PANTALLA VER SR ##

from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

def ver_sr(request):
    query = request.GET.get("q", "")
    estado = request.GET.get("estado", "")
    cliente = request.GET.get("cliente", "")
    producto = request.GET.get("producto", "")
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")
    ing = request.GET.get("ing", "")

    ots = OT.objects.all().order_by("-fecha_ingreso")

    # Filtro general (barra de búsqueda)
    if query:
        ots = ots.filter(
            Q(ot__icontains=query) |
            Q(cliente__icontains=query) |
            Q(producto__icontains=query) |
            Q(sol__icontains=query) |
            Q(enlace_id__icontains=query)
        )

    # Filtro por estado
    if estado:
        ots = ots.filter(estado__iexact=estado)

    # Filtro por cliente
    if cliente:
        ots = ots.filter(cliente__icontains=cliente)

    # Filtro por producto
    if producto:
        ots = ots.filter(producto__icontains=producto)

    # Filtro por ingeniero responsable
    if ing:
        ots = ots.filter(ingeniero__icontains=ing)

    # Filtro por rango de fechas
    if fecha_inicio:
        ots = ots.filter(fecha_ingreso__gte=fecha_inicio)
    if fecha_fin:
        ots = ots.filter(fecha_ingreso__lte=fecha_fin)

    # Calcular días de cola
    for ot in ots:
        ot.dias = ot.dias_cola()
        ot.color = ot.color_cola()

    # PAGINACIÓN → 300 por página
    paginator = Paginator(ots, 300)
    page = request.GET.get("page")
    ots_paginated = paginator.get_page(page)

    return render(request, "ver_sr.html", {
        "ots": ots_paginated,
        "query": query,
        "estado": estado,
        "cliente": cliente,
        "producto": producto,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "ing": ing,
        "paginator": paginator,
    })

## COMENTARIOS EN SR ##
from .models import OT, Comentario
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required
def borrar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)

    # Solo el dueño puede borrar su comentario
    if comentario.usuario != request.user:
        return HttpResponseForbidden("No puedes borrar comentarios de otros usuarios.")

    ot_id = comentario.ot.id
    comentario.delete()

    return redirect("detalle_sr", ot_id=ot_id)

@login_required
def detalle_sr(request, ot_id):
    ot = get_object_or_404(OT, id=ot_id)

    # Crear comentario
    if request.method == "POST":
        texto = request.POST.get("comentario")
        if texto:
            Comentario.objects.create(
                ot=ot,
                usuario=request.user,
                texto=texto
            )
        return redirect("detalle_sr", ot_id=ot.id)

    # Obtener comentarios (solo 5 para inicio)
    comentarios = ot.comentarios.all()

    # Si tiene SOL, buscar otras OT con el mismo SOL
    ot_relacionadas = []
    if ot.sol:
        ot_relacionadas = OT.objects.filter(sol=ot.sol).exclude(id=ot.id)

    return render(request, "detalle_sr.html", {
        "ot": ot,
        "comentarios": comentarios,
        "ot_relacionadas": ot_relacionadas,
    })


## EDITAR SR ##
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from .models import OT, Comentario
from django.utils.timezone import now


@login_required
def editar_sr(request, ot_id):
    ot = get_object_or_404(OT, id=ot_id)

    # Bloquear a clientes
    if request.user.rol == "cliente":
        return HttpResponseForbidden("No tienes permisos para editar esta SR.")

    # Lista de ingenieros (admin + ing)
    ingenieros = CustomUser.objects.filter(rol__in=["admin", "ing"])

    # OT relacionadas por SOL
    relacionadas = []
    if ot.sol:
        relacionadas = OT.objects.filter(sol=ot.sol).exclude(id=ot.id)

    # Comentarios ordenados por fecha
    comentarios = ot.comentarios.order_by("-fecha")

    # ---------------------------------------- #
    #              POST (GUARDAR)              #
    # ---------------------------------------- #
    if request.method == "POST":

        # Estado de la OT
        ot.estado = request.POST.get("estado")

        # Ingeniero encargado
        ing_id = request.POST.get("ing_encargado")
        if ing_id:
            ot.ing_encargado = CustomUser.objects.get(id=ing_id)
        else:
            ot.ing_encargado = None

        # Solo admin puede cambiar fechas
        if request.user.rol == "admin":
            fecha_ing = request.POST.get("fecha_ingreso")
            fecha_cierre = request.POST.get("fecha_cierre")

            if fecha_ing:
                ot.fecha_ingreso = fecha_ing

            if fecha_cierre:
                ot.fecha_cierre = fecha_cierre

        ot.save()

        # Guardar nuevo comentario
        comentario_texto = request.POST.get("nuevo_comentario")
        if comentario_texto:
            Comentario.objects.create(
                ot=ot,
                usuario=request.user,
                texto=comentario_texto,
                fecha=now(),
            )

        return redirect("detalle_sr", ot_id=ot.id)

    # ---------------------------------------- #
    #              GET (MOSTRAR)               #
    # ---------------------------------------- #
    return render(request, "editar_sr.html", {
        "ot": ot,
        "ingenieros": ingenieros,
        "comentarios": comentarios,
        "relacionadas": relacionadas,
        "es_admin": request.user.rol == "admin",
    })



## AGREGAR USUARIO ##
import random
import string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from accounts.models import CustomUser


def generar_password(longitud=10):
    letras = string.ascii_letters
    numeros = string.digits
    simbolos = "!@#$%&*?"

    all_chars = letras + numeros + simbolos
    return "".join(random.choice(all_chars) for _ in range(longitud))


@login_required
def agregar_usuario(request):

    # Solo ADMIN puede entrar
    if request.user.rol != "admin":
        return HttpResponseForbidden("No tienes permisos para crear usuarios.")

    mensaje_ok = None
    mensaje_error = None

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        rol = request.POST.get("rol")

        # Validar duplicado
        if CustomUser.objects.filter(email=correo).exists():
            mensaje_error = "Ya existe un usuario con ese correo."
        else:
            # Generar contraseña aleatoria
            password = generar_password()

            usuario = CustomUser.objects.create_user(
                username=correo,
                email=correo,
                nombre=nombre,
                apellido=apellido,
                rol=rol,
                password=password,
            )

            mensaje_ok = f"Usuario creado con éxito. Contraseña generada: {password}"

    return render(request, "agregar_usuario.html", {
        "mensaje_ok": mensaje_ok,
        "mensaje_error": mensaje_error,
    })
