from django.contrib import admin

from Aplicaciones.Colaboracion.models import Comentario, Proyecto, Tarea, Usuario

# Register your models here.
admin.site.register (Usuario)
admin.site.register (Proyecto)
admin.site.register (Tarea)
admin.site.register (Comentario)