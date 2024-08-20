import pymysql
from tasks import process_name_related_with_sensor_id  # Importa la tarea Celery

HOSTASIGN="34.135.10.201"
# Configura los parámetros de conexión
mysql_config = {
    "host": HOSTASIGN,
    "user": "root",
    "password": "daniel586",
    "database": "Smartcatch",
}

try:
    conexion = pymysql.connect(**mysql_config)
    with conexion.cursor() as cursor:
        # Consulta SQL para obtener los nombres relacionados de ambas tablas
        consulta = """
        SELECT s.name, se.id as sensor_id, se.sensorName
        FROM Station_station s
        INNER JOIN Sensor_sensor se ON s.id = se.stationID_id
        """
        cursor.execute(consulta)
        
        # Recupera los resultados de la consulta
        resultados = cursor.fetchall()

        # Inicia una tarea Celery para cada nombre relacionado
        for nombre_station, sensor_id, nombre_sensor in resultados:
            nombre_relacionado = f"/{nombre_station}/{nombre_sensor}/"
            process_name_related_with_sensor_id.delay(nombre_relacionado, sensor_id)

except pymysql.Error as e:
    print(f"Error de MySQL: {e}")
finally:
    if conexion:
        conexion.close()
