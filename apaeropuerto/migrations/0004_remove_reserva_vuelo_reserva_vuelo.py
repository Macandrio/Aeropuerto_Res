# Generated by Django 5.1.5 on 2025-02-16 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apaeropuerto', '0003_reserva_vuelo_alter_contactoaeropuerto_aeropuerto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='vuelo',
        ),
        migrations.AddField(
            model_name='reserva',
            name='vuelo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reserva_vuelo', to='apaeropuerto.vuelo'),
        ),
    ]
