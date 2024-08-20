#!/bin/bash
source /home/dsb586/background/MQTT_Alarms/env/bin/activate  # Activa tu entorno virtual si lo estás utilizando
cd /home/dsb586/background/MQTT_Alarms  # Cambia a la ubicación de tu proyecto
celery -A celery_app:celery worker --loglevel=info  # Ejecuta Celery con tu configuración
