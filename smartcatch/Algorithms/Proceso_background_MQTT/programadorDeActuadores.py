import pymysql
from tasks import process_name_related_actuators_id
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
        consulta ="""
        SELECT s.id, s.name, se.id as sensor_id, se.name, se.stationID_id
        FROM Station_station s
        INNER JOIN Sensor_actuator se ON s.id = se.stationID_id
        """

        cursor.execute(consulta)
        
        # Recupera los resultados de la consulta
        resultados = cursor.fetchall()

        # Imprime la lista de nombres relacionados junto con el valor de stationID_id y el ID del sensor
        for station_id, nombre_station, sensor_id, nombre_sensor, station_id_value in resultados:
            nombre_relacionado = f"/{nombre_station}/{nombre_sensor}/"
            #print(f"ID del Sensor: {sensor_id}, Nombre relacionado: {nombre_relacionado}, Valor de stationID_id: {station_id_value}")
            process_name_related_actuators_id(nombre_relacionado, sensor_id)

except pymysql.Error as e:
    print(f"Error de MySQL: {e}")

finally:
    if conexion:
        conexion.close()