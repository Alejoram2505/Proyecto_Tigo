from .views import ver_sr, detalle_sr, editar_sr, borrar_comentario, subir_backlog, agregar_usuario
from django.urls import path

urlpatterns = [
    path("ver-sr/", ver_sr, name="ver_sr"),
    path("sr/<int:ot_id>/", detalle_sr, name="detalle_sr"),
    path("sr/<int:ot_id>/editar/", editar_sr, name="editar_sr"),
    path("comentario/<int:id>/borrar/", borrar_comentario, name="borrar_comentario"),
    path("subir-backlog/", subir_backlog, name="subir_backlog"),
    path("agregar-usuario/", agregar_usuario, name="agregar_usuario"),

]
