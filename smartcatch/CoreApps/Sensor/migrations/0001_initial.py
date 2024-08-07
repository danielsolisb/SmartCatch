# Generated by Django 4.2.4 on 2024-08-07 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actuator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('actuators_type', models.CharField(max_length=20)),
                ('actuators_brand', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('value', models.FloatField()),
                ('alarm_type', models.CharField(max_length=20)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorName', models.CharField(blank=True, max_length=100, null=True, verbose_name='SensorName')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='Type')),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('serial', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('notes', models.TextField(blank=True, max_length=100, null=True)),
                ('min_value', models.FloatField(blank=True, null=True)),
                ('max_value', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
