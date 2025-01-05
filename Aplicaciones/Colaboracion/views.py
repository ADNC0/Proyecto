from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario, Proyecto, Tarea, Comentario
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime



def home(request):
    return render(request, "home.html")

# ---------------------------
# Vistas para Usuario
# ---------------------------
def listadoUsuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuario/listadoUsuario.html", {'usuarios': usuarios})

def nuevoUsuario(request):
    return render(request, 'usuario/nuevaUsuario.html')

def guardarUsuario(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            correo = request.POST['correo']
            fecha_registro = request.POST['fecha_registro']
            
            if not fecha_registro:
                fecha_registro = datetime.now().date()
            else:
                fecha_registro = fecha_registro

            Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                fecha_registro=fecha_registro,
            )
            
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('listado_usuarios')
        except KeyError as e:
            messages.error(request, f"Error: El campo {str(e)} no fue enviado.")
            return redirect('nuevaUsuario')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('nuevaUsuario')

def editarUsuario(request, id):
    usuarioEditar = get_object_or_404(Usuario, id=id)
    return render(request, 'usuario/editarUsuario.html', {'usuarioEditar': usuarioEditar})

def procesoActualizarUsuario(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        usuario = get_object_or_404(Usuario, id=id)

        # Actualizar los campos de nombre y correo
        usuario.nombre = request.POST.get('nombre')
        usuario.correo = request.POST.get('correo')

        # Obtener la fecha de registro del formulario (si se proporcionó)
        fecha_registro = request.POST.get('fecha_registro')

        if fecha_registro:
            # Convertir la fecha en un objeto datetime
            from datetime import datetime
            fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%dT%H:%M')
            usuario.fecha_registro = fecha_registro

        # Guardar los cambios
        usuario.save()

        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('listado_usuarios')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listado_usuarios')

def eliminarUsuario(request, id):
    usuarioEliminar = get_object_or_404(Usuario, id=id)
    usuarioEliminar.delete()
    messages.success(request, "Usuario eliminado exitosamente.")
    return redirect('listado_usuarios')

# ---------------------------
# Vistas para Proyecto
# ---------------------------

def listadoProyectos(request):
    proyectos = Proyecto.objects.all()

    # Calcular los proyectos en cada estado
    proyectos_pendientes = proyectos.filter(estado='Pendiente').count()
    proyectos_en_progreso = proyectos.filter(estado='En Progreso').count()
    proyectos_finalizados = proyectos.filter(estado='Finalizado').count()

    # Calcular el total de proyectos
    total_proyectos = proyectos.count()

    # Calcular los porcentajes
    if total_proyectos > 0:
        porcentaje_pendientes = (proyectos_pendientes / total_proyectos) * 100
        porcentaje_en_progreso = (proyectos_en_progreso / total_proyectos) * 100
        porcentaje_finalizados = (proyectos_finalizados / total_proyectos) * 100
    else:
        porcentaje_pendientes = porcentaje_en_progreso = porcentaje_finalizados = 0

    # Pasar los valores al contexto
    return render(request, "proyecto/listadoProyecto.html", {
        'proyectos': proyectos,
        'proyectos_pendientes': proyectos_pendientes,
        'proyectos_en_progreso': proyectos_en_progreso,
        'proyectos_finalizados': proyectos_finalizados,
        'total_proyectos': total_proyectos,
        'porcentaje_pendientes': porcentaje_pendientes,
        'porcentaje_en_progreso': porcentaje_en_progreso,
        'porcentaje_finalizados': porcentaje_finalizados
    })



def nuevoProyecto(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    return render(request, 'proyecto/nuevaProyecto.html', {'usuarios': usuarios})

def guardarProyecto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            fecha_inicio = request.POST['fecha_inicio']
            fecha_fin = request.POST['fecha_fin']
            estado = request.POST['estado']
            usuario_id = request.POST['usuario']
            
            if not nombre or not descripcion or not fecha_inicio or not fecha_fin or not estado or not usuario_id:
                messages.error(request, "Todos los campos son obligatorios.")
                return redirect('nuevoProyecto')
            
            Proyecto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=estado,
                usuario_id=usuario_id,
            )
            
            messages.success(request, "Proyecto creado exitosamente.")
            return redirect('listado_proyectos')
        except KeyError as e:
            messages.error(request, f"Error: El campo {str(e)} no fue enviado.")
            return redirect('nuevoProyecto')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('nuevoProyecto')

def editarProyecto(request, id):
    proyectoEditar = get_object_or_404(Proyecto, id=id)
    usuarios = Usuario.objects.all()  # Obtén todos los usuarios
    return render(request, 'proyecto/editarProyecto.html', {'proyectoEditar': proyectoEditar, 'usuarios': usuarios})

def procesoActualizarProyecto(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        proyecto = get_object_or_404(Proyecto, id=id)

        proyecto.nombre = request.POST.get('nombre')
        proyecto.descripcion = request.POST.get('descripcion')
        proyecto.fecha_inicio = request.POST.get('fecha_inicio')
        proyecto.fecha_fin = request.POST.get('fecha_fin')
        proyecto.estado = request.POST.get('estado')

        usuario_id = request.POST.get('usuario')
        if usuario_id:
            try:
                proyecto.usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                messages.error(request, "El usuario seleccionado no existe.")
                return redirect('editarProyecto', id=id)

        proyecto.save()

        messages.success(request, "Proyecto actualizado correctamente.")
        return redirect('listado_proyectos')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listado_proyectos')

def eliminarProyecto(request, id):
    proyectoEliminar = get_object_or_404(Proyecto, id=id)
    proyectoEliminar.delete()
    messages.success(request, "Proyecto eliminado exitosamente.")
    return redirect('listado_proyectos')

# ---------------------------
# Vistas para Tarea
# ---------------------------
def listadoTareas(request):
    # Obtener todas las tareas
    tareas = Tarea.objects.all()

    # Contar las tareas por estado
    tareas_pendientes = tareas.filter(estado='Pendiente').count()
    tareas_en_progreso = tareas.filter(estado='En progreso').count()
    tareas_finalizadas = tareas.filter(estado='Finalizado').count()

    # Crear los datos para las barras de progreso
    total_tareas = tareas_pendientes + tareas_en_progreso + tareas_finalizadas
    porcentaje_pendiente = (tareas_pendientes / total_tareas) * 100 if total_tareas > 0 else 0
    porcentaje_en_progreso = (tareas_en_progreso / total_tareas) * 100 if total_tareas > 0 else 0
    porcentaje_finalizado = (tareas_finalizadas / total_tareas) * 100 if total_tareas > 0 else 0

    context = {
        'tareas': tareas,
        'tareas_pendientes': tareas_pendientes,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_finalizadas': tareas_finalizadas,
        'porcentaje_pendiente': porcentaje_pendiente,
        'porcentaje_en_progreso': porcentaje_en_progreso,
        'porcentaje_finalizado': porcentaje_finalizado,
    }

    return render(request, "tarea/listadoTarea.html", context)

def nuevaTarea(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    proyectos = Proyecto.objects.all()  # Para asociar tareas con proyectos
    return render(request, 'tarea/nuevaTarea.html', {'proyectos': proyectos, 'usuarios': usuarios})

def guardarTarea(request):
    if request.method == 'POST':
        try:
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            fecha_limite = request.POST['fecha_limite']
            estado = request.POST['estado']
            proyecto_id = request.POST['proyecto']
            usuario_id = request.POST['usuario']
            
            proyecto = Proyecto.objects.get(id=proyecto_id)
            usuario = Usuario.objects.get(id=usuario_id)
            
            Tarea.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_limite=fecha_limite,
                estado=estado,
                proyecto=proyecto,
                usuario=usuario
            )
            
            messages.success(request, "Tarea creada exitosamente.")
            return redirect('listado_tareas')
        
        except KeyError as e:
            messages.error(request, f"Error: El campo {str(e)} no fue enviado.")
            return redirect('nuevaTarea')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('nuevaTarea')

def editarTarea(request, id):
    tareaEditar = get_object_or_404(Tarea, id=id)
    proyectos = Proyecto.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'tarea/editarTarea.html', {'tareaEditar': tareaEditar, 'proyectos': proyectos, 'usuarios': usuarios})

def procesoActualizarTarea(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        tarea = get_object_or_404(Tarea, id=id)

        tarea.titulo = request.POST.get('titulo')
        tarea.descripcion = request.POST.get('descripcion')
        proyecto_id = request.POST.get('proyecto')
        usuario_id = request.POST.get('usuario')
        
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        tarea.proyecto = proyecto
        tarea.usuario = usuario
        tarea.estado = request.POST.get('estado')
        tarea.fecha_limite = request.POST.get('fecha_limite')
        
        tarea.save()

        messages.success(request, "Tarea actualizada correctamente.")
        return redirect('listado_tareas')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listado_tareas')

def eliminarTarea(request, id):
    tareaEliminar = get_object_or_404(Tarea, id=id)
    tareaEliminar.delete()
    messages.success(request, "Tarea eliminada exitosamente.")
    return redirect('listado_tareas')
# ---------------------------
# Vistas para Comentarios
# ---------------------------
def listadoComentarios(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios
    comentarios = Comentario.objects.all()
    estados = {
        "Pendiente": 0,
        "En progreso": 0,
        "Finalizado": 0
    }

    for comentario in comentarios:
        if comentario.tarea.estado == "Pendiente":
            estados["Pendiente"] += 1
        elif comentario.tarea.estado == "En progreso":
            estados["En progreso"] += 1
        elif comentario.tarea.estado == "Finalizado":
            estados["Finalizado"] += 1

    return render(request, "comentario/listadoComentario.html", {'comentarios': comentarios, 'usuarios': usuarios, 'estados': estados})


def nuevoComentario(request):
    # Obtener todos los usuarios y tareas
    usuarios = Usuario.objects.all()
    tareas = Tarea.objects.all()

    if request.method == 'POST':
        # Obtener los datos del formulario
        texto_comentario = request.POST.get('texto')
        tarea_id = request.POST.get('tarea')
        usuario_id = request.POST.get('usuario')

        # Obtener la tarea y usuario seleccionados
        tarea = Tarea.objects.get(id=tarea_id)
        usuario = Usuario.objects.get(id=usuario_id)

        # Crear y guardar el nuevo comentario
        comentario = Comentario(
            texto=texto_comentario,
            tarea=tarea,
            usuario=usuario,
        )
        comentario.save()

        # Devolver una respuesta JSON para la actualización automática del gráfico
        return JsonResponse({'message': 'Comentario agregado con éxito'})

    return render(request, 'comentario/nuevaComentario.html', {'tareas': tareas, 'usuarios': usuarios})

def guardarComentario(request):
    if request.method == 'POST':
        try:
            # Obtener los valores del formulario
            texto = request.POST['texto']  # Aquí es 'texto' y no 'contenido'
            tarea_id = request.POST['tarea']
            usuario_id = request.POST['usuario']

            # Obtener el objeto de la tarea y usuario correspondiente
            tarea = get_object_or_404(Tarea, id=tarea_id)
            usuario = get_object_or_404(Usuario, id=usuario_id)

            # Crear y guardar el comentario
            Comentario.objects.create(
                texto=texto,  # Aquí usamos 'texto' en lugar de 'contenido'
                tarea=tarea,
                usuario=usuario,
            )

            # Mensaje de éxito
            messages.success(request, "Comentario creado exitosamente.")
            # Redirigir al listado de comentarios
            return redirect('listado_comentarios')
        except KeyError as e:
            messages.error(request, f"Error: El campo {str(e)} no fue enviado.")
            return redirect('nuevaComentario')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('nuevaComentario')

def editarComentario(request, id):
    comentarioEditar = get_object_or_404(Comentario, id=id)
    tareas = Tarea.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'comentario/editarComentario.html', {'comentarioEditar': comentarioEditar, 'tareas': tareas, 'usuarios': usuarios})

def procesoActualizarComentario(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        comentario = get_object_or_404(Comentario, id=id)

        comentario.texto = request.POST.get('texto')  # Usar 'texto' aquí también
        tarea_id = request.POST.get('tarea')
        usuario_id = request.POST.get('usuario')
        
        tarea = get_object_or_404(Tarea, id=tarea_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        comentario.tarea = tarea
        comentario.usuario = usuario
        comentario.save()

        messages.success(request, "Comentario actualizado correctamente.")
        return redirect('listado_comentarios')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listado_comentarios')

def eliminarComentario(request, id):
    comentarioEliminar = get_object_or_404(Comentario, id=id)
    comentarioEliminar.delete()
    messages.success(request, "Comentario eliminado exitosamente.")
    return redirect('listado_comentarios')
