import pymysql

# Configura los parámetros de conexión
conexion = pymysql.connect(
    host="192.168.10.201",
    user="root",
    password="daniel586",
    database="Gae"
)

# Nombre que deseas buscar
nombre_a_buscar = "TemperaturaS"

try:
    with conexion.cursor() as cursor:
        # Consulta SQL para obtener el ID según el nombre
        consulta = "SELECT id FROM Sensors_sensor WHERE sensorName = %s"
        cursor.execute(consulta, (nombre_a_buscar,))
        
        # Recupera el resultado de la consulta (debería ser una sola fila si el nombre es único)
        resultado = cursor.fetchone()

        if resultado:
            id_encontrado = resultado[0]
            print(f"El ID correspondiente al nombre '{nombre_a_buscar}' es {id_encontrado}")
        else:
            print(f"No se encontró ningún registro con el nombre '{nombre_a_buscar}'")

except pymysql.Error as e:
    print(f"Error de MySQL: {e}")

finally:
    # Cierra la conexión
    conexion.close()