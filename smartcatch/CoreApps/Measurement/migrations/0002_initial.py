# Generated by Django 4.2.4 on 2024-08-17 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Sensor', '0001_initial'),
        ('Measurement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurements_actuators',
            name='actuatorsID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sensor.actuator', verbose_name='Associated Actuators'),
        ),
        migrations.AddField(
            model_name='measurements',
            name='sensorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sensor.sensor', verbose_name='Associated Sensor'),
        ),
        migrations.AddIndex(
            model_name='measurements',
            index=models.Index(fields=['sensorID'], name='Measurement_sensorI_943ca7_idx'),
        ),
        migrations.AddIndex(
            model_name='measurements',
            index=models.Index(fields=['timestamp'], name='Measurement_timesta_b6da99_idx'),
        ),
    ]
