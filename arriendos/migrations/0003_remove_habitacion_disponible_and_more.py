# Generated by Django 5.1.2 on 2024-12-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arriendos', '0002_remove_habitacion_ubicacion_habitacion_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitacion',
            name='disponible',
        ),
        migrations.RemoveField(
            model_name='habitacion',
            name='numero',
        ),
        migrations.AddField(
            model_name='habitacion',
            name='capacidad',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habitacion',
            name='estado',
            field=models.CharField(choices=[('Disponible', 'Disponible'), ('Reservada', 'Reservada')], default='Disponible', max_length=20),
        ),
    ]
