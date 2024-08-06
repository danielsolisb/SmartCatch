# Generated by Django 4.2.4 on 2024-08-06 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Sensor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurements_actuators',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.FloatField(verbose_name='Data')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('actuatorsID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sensor.actuator', verbose_name='Associated Actuators')),
            ],
        ),
        migrations.CreateModel(
            name='Measurements',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.FloatField(verbose_name='Data')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sensorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sensor.sensor', verbose_name='Associated Sensor')),
            ],
            options={
                'indexes': [models.Index(fields=['sensorID'], name='Measurement_sensorI_943ca7_idx'), models.Index(fields=['timestamp'], name='Measurement_timesta_b6da99_idx')],
            },
        ),
    ]
