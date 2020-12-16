# Generated by Django 3.1.2 on 2020-10-14 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminCine', '0003_auto_20201013_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pelicula',
            old_name='activo',
            new_name='estado',
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('id_proyeccion', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('hora', models.CharField(max_length=5)),
                ('estado', models.BooleanField(default=False)),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminCine.pelicula')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminCine.sala')),
            ],
        ),
        migrations.CreateModel(
            name='Butaca',
            fields=[
                ('id_butaca', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('fila', models.IntegerField()),
                ('asiento', models.IntegerField()),
                ('proyeccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminCine.proyeccion')),
            ],
        ),
    ]