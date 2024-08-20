import pymysql

# Configura los parámetros de conexión
conexion = pymysql.connect(
    host="192.168.100.33",
    user="root",
    password="daniel586",
    database="Gae"
)

try:
    with conexion.cursor() as cursor:
        # Consulta SQL para obtener los nombres relacionados de ambas tablas
        consulta = """
        SELECT s.id, s.name, se.id as sensor_id, se.sensorName, se.stationID_id
        FROM Stations_station s
        INNER JOIN Sensors_sensor se ON s.id = se.stationID_id
        """
        cursor.execute(consulta)
        
        # Recupera los resultados de la consulta
        resultados = cursor.fetchall()

        # Imprime la lista de nombres relacionados junto con el valor de stationID_id y el ID del sensor
        for station_id, nombre_station, sensor_id, nombre_sensor, station_id_value in resultados:
            nombre_relacionado = f"/{nombre_station}/{nombre_sensor}/"
            print(f"ID del Sensor: {sensor_id}, Nombre relacionado: {nombre_relacionado}, Valor de stationID_id: {station_id_value}")

except pymysql.Error as e:
    print(f"Error de MySQL: {e}")

finally:
    # Cierra la conexión
    conexion.close()