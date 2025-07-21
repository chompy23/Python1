from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import random
import time as basedetiempo

class Fin_De_Graficado(Exception):
        
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
        
        
    def __str__(self):
        
        return (f"Fin de la animación: {self.mensaje}")



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


try:
    
    
    #plt.pause(0.1)
    #basedetiempo.sleep(10)  # Simula un retardo de 1 segundo entre actualizaciones
    # Crear una figura y un eje
    # Datos
    """x_data = []
    y_data = []
    
    x_data.append(0) 
    y_data.append(0)
    while scaneo  <= 60:
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        line, = ax.plot(x_data, y_data, 'r-')
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

        # Personalizar la apariencia de las marcas (opcional)
        ax.tick_params(axis='both', which='major', length=10, width=2, labelsize=12)
        ax.tick_params(axis='both', which='minor', length=5, width=1, labelsize=10)

        ax.set_xlabel('Tiempo (seg)')
        ax.set_ylabel('Velocidad de la Turbina (rpm)')
        ax.set_title('Curva Velocidad/Tiempo de la Turbina en tiempo real')
        # Formato para eje X de tiempo
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        def init():
            ax.set_ylim(0, 6000)  # Ajustá según el rango esperado de Y
            ax.set_xlim(0, 120)  # Ajustá según el rango esperado de X
            return line,
                
        def update(frame):
            basedetiempo.sleep(1)  #retardo de 1 segundo entre actualizaciones
            x_data.append(tiempo_actual) 
            y_data.append(valor_y)
            # Mantenemos solo los últimos 100 puntos
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)
            # Actualizar los datos de la línea
            line.set_data(x_data, y_data)
            return line,
        if scaneo >= 60:
            tiempo_actual += 1
            b += 160
            valor_y = b
            scaneo = 0
            break 
        
        ani = FuncAnimation(fig, update, init_func=init, interval=1000, blit=False)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        scaneo += 1
    print(f"scaneo: {scaneo} - tiempo_actual: {tiempo_actual} - valor_y: {valor_y}")    
    def obtener_valor_eje_y():
        global b  
        if b == 0:
            b = 160
        else:
            b += 160
        
        return b #Ejemplo con valor simulado
        # Variable global para el valor dinámico
    # Crear la animación
    ani = FuncAnimation(fig, update, init_func=init, interval=100, blit=False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    """
    
    """scaneo = 0
    b = 0   
    valor_y = 0 """
    tiempo_actual = 0
    vel = 0.0
    acel = 0.0
    fric = 0.0
    compr = 0.0
    frenado = 0.0
    vel_fin = 0.0
        
    def grafico(vel_tur, aceleracion_tur,  friccion_tur, carga_compresor, pot_frenado, vel_fin_ciclo): 
        global vel, acel,  fric, compr, frenado, vel_fin
        vel = vel_tur
        acel = aceleracion_tur
        fric = friccion_tur
        compr = carga_compresor
        frenado = pot_frenado
        vel_fin = vel_fin_ciclo
        print(f"Velocidad de la turbina: {vel} rpm, Aceleración: {acel}, Fricción: {fric}, Carga Compresor: {compr}, Potencia de Frenado: {frenado}, Velocidad Final Ciclo: {vel_fin}   rpm ")
        def leer_entrada():
            try:
                
                # Aquí deberías leer el valor real de tu entrada PLC
                # Por ejemplo: return mi_objeto_plc.entradas["sensor_velTur"]
                #basedetiempo.time() % 10 * 600
                global vel, acel,  fric, compr, frenado, vel_fin
                vel = vel + (vel_fin / (acel*60)) - (fric / 60) - (compr / 60) - (frenado / 60)
                if vel >= vel_fin:
                    print("\n")
                    event_source.stop()  # Detiene la animación
                    print(f"Velocidad de la turbina alcanzó la velocidad de {vel_fin}.")
                return vel           
            except Exception as e:
                print(f"Fin de la animación por pausa: {e}")
        print(vel)         
        def base_Tiempo():
            global tiempo_actual
            tiempo_actual += timedelta(seconds=1).total_seconds()  # Incrementa el tiempo en 1 segundo
            
            return tiempo_actual
        x_data = []
        y_data = []
        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        line, = ax.plot([], [], 'r-')
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

        # Personalizar la apariencia de las marcas (opcional)
        ax.tick_params(axis='both', which='major', length=10, width=2, labelsize=12)
        ax.tick_params(axis='both', which='minor', length=5, width=1, labelsize=10)

        # marcas de velocidad
        ax.axhline(y=480, color="black", linestyle="--")
        ax.text(0, 480, "Vel. de autosust.", color="blue", fontsize=10, verticalalignment='bottom', horizontalalignment='left')
        ax.text(0, 480, "480  ", color="blue", fontsize=10, verticalalignment='center', horizontalalignment='right')
        ax.axhline(y=2500, color="black", linestyle=":")
        ax.text(0, 2500, "En Parada; aplico frenos", color="gray", fontsize=10, verticalalignment='top', horizontalalignment='left')
        ax.text(0, 2500, "2500  ", color="gray", fontsize=10, verticalalignment='center', horizontalalignment='right')
        ax.axhline(y=2750, color="black", linestyle="--")
        ax.text(0, 2750, "Paso a control automático", color="black", fontsize=10, verticalalignment='bottom', horizontalalignment='left')
        ax.text(0, 2750, "2750  ", color="black", fontsize=10, verticalalignment='center', horizontalalignment='right')
        ax.axhline(y= 4600, color="red", linestyle="-.")
        ax.text(0, 4600, "SetPoint de Vel. ", color="red", fontsize=10, verticalalignment='bottom', horizontalalignment='left')
        ax.text(0, 4600, "4600  ", color="red", fontsize=10, verticalalignment='center', horizontalalignment='right')
        ax.set_xlabel('Tiempo (seg)')
        ax.set_ylabel('Valor de velocidad de la Turbina (rpm)')
        ax.set_title('Velocidad de la Turbina en tiempo real (rpm)')

        def init():
            ax.set_xlim(0, 1240)
            ax.set_ylim(0, 6000)
            line.set_data([], [])
            return line,

        def update(frame):
            #x_data.append(frame)
            x_data.append(base_Tiempo())
            y_data.append(leer_entrada())
            line.set_data(x_data, y_data)
            #ax.set_xlim(max(0, frame-60), frame+1)  # Ventana deslizante de 60s
            return line,
        
        ani = FuncAnimation(fig, update, init_func=init, interval=1000, blit=False, repeat=False)
        event_source = ani.event_source
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        return leer_entrada()    
  
    d = grafico(0.0, 3.0, 2.5, 5.0, 1.0, 480.0)
    print(f"Velocidad de la turbina: {d} rpm")
except Fin_De_Graficado as e:
    print(f"Fin de la animación: {e.mensaje}") 
           
except KeyboardInterrupt:
    print("Animación detenida por el usuario.") 
  

