import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
import matplotlib.dates as mdates
import random
plt.style.use('_mpl-gallery')

"""# make data
x = np.linspace(0, 10, 10)
y = 4 + 1 * np.sin(2 * x)
x2 = np.linspace(0, 10, 25)
y2 = 4 + 1 * np.sin(2 * x2)

# plot
fig, ax = plt.subplots()

ax.plot(x2, y2 + 2.5, 'x', markeredgewidth=2.0)
ax.plot(x, y, linewidth=1.0)
ax.plot(x2, y2 - 2.5, 'o-', linewidth=2)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()"""




# Datos
x_data = []
y_data = []

fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')

# Formato para eje X de tiempo
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

def init():
    ax.set_ylim(0, 10)  # Ajustá según el rango esperado de Y
    return line,

def update(frame):
    tiempo_actual = datetime.now()
    valor_y = obtener_valor_eje_y()
    x_data.append(tiempo_actual)
    y_data.append(valor_y)
    
    # Mantenemos solo los últimos 100 puntos
    if len(x_data) > 100:
        x_data.pop(0)
        y_data.pop(0)
    
    ax.set_xlim(x_data[0], x_data[-1])
    line.set_data(x_data, y_data)
    return line,

def obtener_valor_eje_y():
    # Acá recibís tu valor dinámico desde sensor, cálculo, etc.
    return random.randint(0, 10)  # Ejemplo con valor simulado

ani = FuncAnimation(fig, update, init_func=init, interval=1000, blit=True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()