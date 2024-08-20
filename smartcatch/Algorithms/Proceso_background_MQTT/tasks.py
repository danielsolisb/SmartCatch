#Cod para evitar fallo de numero de id
#cod para evitar lecturas falsas
import time
from celery_app import celery
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import pymysql
from datetime import datetime
import sys

HOSTASIGN= "34.135.10.201"
#No olvidar cambiar el pass
class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def Open(self):
        self.connection = pymysql.connect(
            host=HOSTASIGN,
            user='root',
            password='daniel586',
            db='Smartcatch'
        )
        self.cursor = self.connection.cursor()
        print("Conexión establecida")

    def Close(self):
        if self.connection:
            self.connection.close()
            print("Cerrando conexión")
            self.connection = None
            self.cursor = None
    
    def obtener_limites_para_sensor(self, sensor_id, max_intentos=3):
        intento = 0
        max_value = None
        min_value = None
        valores_obtenidos = False  # Bandera para indicar si se obtuvieron valores

        while intento < max_intentos and (max_value is None or min_value is None):
            sql = "SELECT max_value, min_value FROM Sensor_sensor WHERE id = %s"
            try:
                self.cursor.execute(sql, (sensor_id,))
                result = self.cursor.fetchone()
                if result:
                    max_value, min_value = result
                    valores_obtenidos = True  # Se obtuvieron valores
                    break  # Rompe el ciclo si se obtienen los valores
            except Exception as e:
                print("Error al obtener los límites para el sensor en el intento", intento + 1, ":", e)
            intento += 1

        if not valores_obtenidos:
            print("No se pudieron obtener los valores después de", max_intentos, "intentos")
            return None, None, False  # Retornar valores individuales
        
        return (
            float(max_value) if max_value is not None else None,
            float(min_value) if min_value is not None else None,
            valores_obtenidos  # Retorna la bandera
        )

    ######Función para agregar alarmas############
    def Ingresar_alarma(self, timestamp, value, alarm_type, message, sensor_id):
        sql = "INSERT INTO Sensor_alarm (timestamp, value, alarm_type, message, sensor_id) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (timestamp, value, alarm_type, message, sensor_id))
            self.connection.commit()
        except Exception as e:
            print("Error de MySQL de Alarms:", e)

    
    #def Ingresar_datos(self,ide, valor,timestamp,sensor_id):
    #    sql = "INSERT INTO Measurements_measurements VALUES ('{}','{}',{},'{}')".format(ide,valor,timestamp,sensor_id)
    #    try:
    #        self.cursor.execute(sql)
    #        self.connection.commit()
    #    except Exception as e:
    #        print(f"Error de MySQL")
    
    def Ingresar_datos(self, valor,timestamp,sensor_id):
        sql = "INSERT INTO Measurement_measurements (value, timestamp, sensorID_id) VALUES (%s, %s, %s)"
        #sql = "INSERT INTO Measurements_measurements VALUES ('{}',{},'{}')".format(ide,valor,timestamp,sensor_id)
        try:
            self.cursor.execute(sql, (valor, timestamp, sensor_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error de MySQL", e)
    
    def Ingresar_datos_actuators(self, valor,timestamp,sensor_id):
        sql = "INSERT INTO Measurement_measurements_actuators (value, timestamp, actuatorsID_id) VALUES (%s, %s, %s)"
        #sql = "INSERT INTO Measurements_measurements VALUES ('{}',{},'{}')".format(ide,valor,timestamp,sensor_id)
        try:
            self.cursor.execute(sql, (valor, timestamp, sensor_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error de MySQL", e)

###############################

def subscripcion(topico, ids):
    database.Open()
    msg = subscribe.simple(topico, hostname=HOSTASIGN)
    print("se suscribio")
    payload = msg.payload.decode("utf-8")
    print("Altern %s %s" % (msg.topic, payload))
    
    fecha="NOW()"
    fecha_actual = datetime.now()
    #IDE=(database.Select_lastID())
    if (payload == "EXIT"):
        print("saliendo")
        sys.exit()
    if (payload == "ALARMD"):
        dato = 0
        database.Ingresar_alarma(fecha_actual, dato, "alarm", f"SENSOR DISCONNECTED", ids)

    try:
        dato= float(msg.payload)
        print(f"Mensaje recibido en el tema '{topico}': Es un número ({dato})")
    except ValueError:
        print(f"Mensaje recibido en el tema '{topico}': Es un texto ({payload})")
    #database.Ingresar_datos(IDE,dato,fecha,ids)

     # Obtener los valores máximos y mínimos para el sensor específico
    max_value, min_value, habilitado = database.obtener_limites_para_sensor(ids)
    database.Ingresar_datos(dato,fecha_actual,ids)
    if habilitado == True:
        print('Maximo:', max_value,'Minimo', min_value )
        #fecha_actual = datetime.now()
        if max_value is not None and min_value is not None:
            if dato > max_value:
                database.Ingresar_alarma(fecha_actual, dato, "alarm", "value HIGHER than the MAXIMUM allowed", ids)
            elif dato < min_value:
                database.Ingresar_alarma(fecha_actual, dato, "alarm", "value LESS than the MINIMUN allowed", ids)
            elif dato > max_value * 0.9 and dato < max_value:
                database.Ingresar_alarma(fecha_actual, dato, "warning", f"Value between 90% and 100% of the sensor maximum", ids)
            elif dato < min_value * 1.1 and dato > min_value:
                database.Ingresar_alarma(fecha_actual, dato, "warning", f"Value between the minimum and 110% of the minimum for the sensor", ids)
    else:
        print("No se puede almacenar datos")
    
    database.Close()
    
def subscripcion_actuador(topico, ids):
    database.Open()
    msg = subscribe.simple(topico, hostname=HOSTASIGN)
    print("se suscribio")
    payload = msg.payload.decode("utf-8")
    print("Altern %s %s" % (msg.topic, payload))
    
    fecha="NOW()"
    fecha_actual = datetime.now()
    #IDE=(database.Select_lastID())
    if (payload == "EXIT"):
        print("saliendo")
        sys.exit()

    try:
        dato= float(msg.payload)
        print(f"Mensaje recibido en el tema '{topico}': Es un número ({dato})")
    except ValueError:
        print(f"Mensaje recibido en el tema '{topico}': Es un texto ({payload})")
    #database.Ingresar_datos(IDE,dato,fecha,ids)
    database.Ingresar_datos_actuators(dato,fecha_actual,ids)
    database.Close()
    

database = DataBase()

@celery.task
def process_name_related_with_sensor_id(name_related : str , sensor_id : int):
    topic = name_related
    print(topic)
    idsensor = sensor_id
    while True:
        try:
            subscripcion(topic, idsensor)
            
        except KeyboardInterrupt:  #precionar Crtl + C para salir
            database.Close()
            print("cerrando proceso")
            break

@celery.task
def process_name_related_actuators_id(name_related_actuator: str, actuator_id : int):
    topic = name_related_actuator
    idactuator = actuator_id
    while True:
        try:
            subscripcion_actuador(topic, idactuator)
        except KeyboardInterrupt:  #precionar Crtl + C para salir
            database.Close()
            print("cerrando proceso")
            break
        
    pass