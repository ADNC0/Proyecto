from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # Rutas de Usuario

    path('listadoUsuario/', views.listadoUsuarios, name='listado_usuarios'),
    path('nuevaUsuario/', views.nuevoUsuario, name='nuevaUsuario'),
    path('guardarUsuario/', views.guardarUsuario, name='guardarUsuario'),
    path('editarUsuario/<int:id>/', views.editarUsuario, name='editarUsuario'),
    path('procesoActualizarUsuario/', views.procesoActualizarUsuario, name='procesoActualizarUsuario'),
    path('eliminarUsuario/<int:id>/', views.eliminarUsuario, name='eliminarUsuario'),

    # Rutas de Proyecto
    path('listadoProyecto/', views.listadoProyectos, name='listado_proyectos'),
    path('nuevaProyecto/', views.nuevoProyecto, name='nuevaProyecto'),
    path('guardarProyecto/', views.guardarProyecto, name='guardarProyecto'),
    path('editarProyecto/<int:id>/', views.editarProyecto, name='editarProyecto'),
    path('procesoActualizarProyecto/', views.procesoActualizarProyecto, name='procesoActualizarProyecto'),
    path('eliminarProyecto/<int:id>/', views.eliminarProyecto, name='eliminarProyecto'),

    # Rutas de Tarea
    path('listadoTarea/', views.listadoTareas, name='listado_tareas'),
    path('nuevaTarea/', views.nuevaTarea, name='nuevaTarea'),
    path('guardarTarea/', views.guardarTarea, name='guardarTarea'),
    path('editarTarea/<int:id>/', views.editarTarea, name='editarTarea'),
    path('procesoActualizarTarea/', views.procesoActualizarTarea, name='procesoActualizarTarea'),
    path('eliminarTarea/<int:id>/', views.eliminarTarea, name='eliminarTarea'),

    # Rutas de Comentario

    path('listadoComentario/', views.listadoComentarios, name='listado_comentarios'),
    path('nuevaComentario/', views.nuevoComentario, name='nuevaComentario'),
    path('guardarComentario/', views.guardarComentario, name='guardarComentario'),
    path('editarComentario/<int:id>/', views.editarComentario, name='editarComentario'),
    path('procesoActualizarComentario/', views.procesoActualizarComentario, name='procesoActualizarComentario'),
    path('eliminarComentario/<int:id>/', views.eliminarComentario, name='eliminarComentario'),

    # Rutas de Estados


]
