import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread
import time
import pyqtgraph as pg


# Configuración inicial
fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 1000)
line, = ax.plot(x, np.sin(x))  # Señal inicial

# Función para actualizar la animación
def update(frame):
    y = np.sin(x + frame/10)  # Simula una señal dinámica
    line.set_ydata(y)
    return line,

# Función para ejecutar en segundo plano (simula tu software)
def background_task():
    while True:
        print("Ejecutando tarea en segundo plano...")
        time.sleep(1)  # Simula trabajo

# Iniciar el hilo para el software
thread = Thread(target=background_task)
thread.daemon = True  # Termina cuando el programa principal termine
thread.start()

# Iniciar animación
ani = animation.FuncAnimation(fig, update, interval=50, blit=True)
plt.show()


"""Solución con PyQtGraph (Más eficiente para tiempo real)

PyQtGraph es ideal para visualizaciones de alta frecuencia (como audio o señales de sensores)PyQt5.QtWidgets."""



import numpy as np
from PyQt5 import QApplication
from threading import Thread
import time

# Configuración de la ventana
app = QApplication([])
win = pg.GraphicsLayoutWidget()
plot = win.addPlot()
curve = plot.plot(pen='y')

# Datos iniciales
x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x)

# Función para actualizar la gráfica
def update():
    global y
    y = np.sin(x + time.time())  # Señal dinámica
    curve.setData(y)

# Función en segundo plano
def background_task():
    while True:
        print("Tarea en segundo plano ejecutándose...")
        time.sleep(1)

# Iniciar hilo
thread = Thread(target=background_task)
thread.daemon = True
thread.start()

# Timer para actualizar la gráfica
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)  # Actualizar cada 50 ms

win.show()
app.exec_()


"""Solución con audio en tiempo real (PyAudio + matplotlib)

Si quieres visualizar audio como un osciloscopio:"""


import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuración de PyAudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Configuración del gráfico
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.random.rand(CHUNK), 'r-')

# Función para actualizar el gráfico con datos del micrófono
def update(frame):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    line.set_ydata(data)
    return line,

ani = animation.FuncAnimation(fig, update, interval=0, blit=True)
plt.show()

# Cerrar stream al terminar
stream.stop_stream()
stream.close()
p.terminate()