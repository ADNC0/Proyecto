# Generated by Django 5.0 on 2024-12-30 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado', models.CharField(default='En progreso', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=100)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_limite', models.DateField()),
                ('estado', models.CharField(default='Pendiente', max_length=50)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Colaboracion.proyecto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Colaboracion.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Colaboracion.usuario'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('fecha_comentario', models.DateTimeField(auto_now_add=True)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Colaboracion.tarea')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Colaboracion.usuario')),
            ],
        ),
    ]