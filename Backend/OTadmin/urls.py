from .views import ver_sr, detalle_sr, editar_sr, borrar_comentario, subir_backlog,agregar_usuario, subir_segmento, ver_clientes, graficas_view, exportar_kpis_excel
from django.urls import path
from OTadmin.views import graficas_view, exportar_kpis_excel

urlpatterns = [
    path("ver-sr/", ver_sr, name="ver_sr"),
    path("sr/<int:ot_id>/", detalle_sr, name="detalle_sr"),
    path("sr/<int:ot_id>/editar/", editar_sr, name="editar_sr"),
    path("comentario/<int:id>/borrar/", borrar_comentario, name="borrar_comentario"),
    path("subir-backlog/", subir_backlog, name="subir_backlog"),
    path("agregar-usuario/", agregar_usuario, name="agregar_usuario"),
    path("subir-segmento/", subir_segmento, name="subir_segmento"),
    path("ver-clientes/", ver_clientes, name="ver_clientes"),
    path("graficas/", graficas_view, name="graficas"),
    path("graficas/exportar-excel/", exportar_kpis_excel, name="exportar_kpis_excel"),
    path("graficas/export/", exportar_kpis_excel, name="exportar_kpis_excel"),

]
