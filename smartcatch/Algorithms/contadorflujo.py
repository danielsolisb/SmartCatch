import tkinter as tk
from tkinter import ttk
import serial
import threading

def start_serial_communication():
    try:
        # Configura el puerto serial
        ser = serial.Serial('COM7', 9600, timeout=1)

        def read_serial():
            while running:
                ser.write(b'R')  # Envía la letra R
                data = ser.readline().decode('utf-8').strip()  # Lee el valor recibido
                if data:
                    value_label.config(text=data)  # Actualiza el valor en la interfaz
                root.update()  # Refresca la ventana

        # Inicia un hilo para leer el puerto serial continuamente
        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()

    except serial.SerialException as e:
        value_label.config(text=f"Error: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Monitor Serial")
root.geometry("300x150")

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiqueta para mostrar el valor recibido
value_label = ttk.Label(frame, text="Esperando datos...", font=("Helvetica", 16))
value_label.grid(column=0, row=0, padx=5, pady=10)

# Botón para salir
exit_button = ttk.Button(frame, text="Salir", command=lambda: close_program())
exit_button.grid(column=0, row=1, padx=5, pady=10)

# Variable para controlar el hilo
running = True

def close_program():
    global running
    running = False
    root.destroy()

# Inicia la comunicación serial
start_serial_communication()

# Inicia la interfaz gráfica
root.mainloop()
