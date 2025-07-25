import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import time as baseDeTiempo    

b = 0 
x_data = []
y_data = []
x_data.append(0) 
y_data.append(0)
tiempo_actual = 0
rampa_aceleracion = 0.0
   

class Turbina():
    
    # Rango de Velocidad de la Turbima en [rpm]
    velTurbRpmMin = 0
    velTurbRpmMax = 6000 
    vel_turb_rpm = 0.0
       
    def __init__(self):
                                               
        self.ent = EntradasPlc()
        self.sal = SalidasPlc()
        self.Man_Auto = False
        self.friccion = 2.5               # Frenado por inercia en la turbina 2.5 rpm
        self.inputs_criticas = False
        self.inputs_criticas1 = False
        self.inputs_criticas2 = False
        self.inputs_criticas3 = False
        self.carga_compresor = 10.2          # Carga del compresor en la turbina
    
    def update(self):
       
        try:
            if (self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota")
                and self.ent.entradas.get("p_valPpalAbi") and self.ent.entradas.get("p_paradaTur") 
                and self.ent.entradas.get("sensor_velTur") <= 0.0):  # valvula ppal. abierta
                print("Valvula Ppal. abierta \n")
                self.ent.entradas["sensor_valvppal"] = True
                print("Se procede a la puesta en marcha de la Turbina")
            elif (self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota") 
                  and self.ent.entradas.get("p_valPpalAbi")== False and self.ent.entradas.get("p_paradaTur") 
                  and self.ent.entradas.get("sensor_velTur") >= 480.0):
                print("Intento de cierre de la valvula Ppal. con la Turbina en marcha \n")
                print("Se procede a la parada de Emergencia de la Turbina")
                self.parada()
                self.ent.entradas["sensor_valvppal"] = False
                raise ParadaDeTurbina1("Parada de la Turbina , por valvula Ppal. cerrada") 
            elif (self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota") 
                  and self.ent.entradas.get("p_valPpalAbi") == False and self.ent.entradas.get("p_paradaTur") 
                  and self.ent.entradas.get("sensor_velTur") <= 480.0):
                print("Intento de cierre de la valvula Ppal. con la Turbina en marcha \n")
                print("Se procede a la parada de la Turbina")
                self.parada_controlada()
                self.ent.entradas["sensor_valvppal"] = False
                raise ParadaDeTurbina1("Parada de la Turbina , por valvula Ppal. cerrada")  
            else:    
                while (self.ent.entradas.get("p_valPpalAbi") == False and self.ent.entradas.get("pE_SControl") 
                       and self.ent.entradas.get("pE_Remota") and self.ent.entradas.get("p_paradaTur") 
                       and self.ent.entradas.get("sensor_velTur") <= 0.0):   #  valvula ppal. cerrada
                    print ("valvula Ppal. cerrada \n")
                    print (" pulsar p_valPpalAbi Para abrir la valvula \n")
                    baseDeTiempo.sleep(1)
                    self.modificar_ent()
                    self.ent.entradas["sensor_valvppal"] = True
                    baseDeTiempo.sleep(1)
                    if self.ent.entradas.get("sensor_valvppal") == True:
                        break
            print("""
                PASO 1:
                Para el arranque con la turbina completamente detenida, se utiliza un motor auxiliar, que se acopla 
                mediante una junta neumática comandada desde el PLC y mueve el eje completo de la turbina hasta 
                llegar a la velocidad de auto sustentación (478 rpm). Si la válvula principal manual no está abierta, no 
                se puede ejecutar el arranque.\n""")
            self.inputs_criticas = (self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota") 
                                    and self.ent.entradas.get("sensor_valvppal"))
            
            if self.inputs_criticas:
                if  self.ent.entradas.get("p_paradaTur") == False:
                    self.parada_controlada()
                if self.ent.entradas.get("sensor_velTur") <= 0.0 and self.inputs_criticas :
                    print("Comienza el ciclo de encendido de la Turbina : self.paso1 \n")
                    while self.ent.entradas.get("p_marchaTur") == False:
                        print("Pulsar p_marchaTur para iniciar el arranque de la Turbina \n")
                        self.modificar_ent()
                        if self.ent.entradas.get("p_marchaTur") or self.ent.entradas.get("p_paradaTur") == True:
                            break
                        baseDeTiempo.sleep(1)
                    if self.ent.entradas.get("p_marchaTur"): # inicia la secuencia de arranque de la turbina
                        print("Ponemos en modo manual el control de velocidad\n")
                        self.Man_Auto  = False  # control de la valvula de combustible en manual
                        self.inputs_criticas1 = self.inputs_criticas and self.ent.entradas.get("p_paradaTur") 
                        if self.inputs_criticas1:
                            print("Liberamos el freno de la Turbina")
                            self.sal.salidas["frenos"] = True
                            baseDeTiempo.sleep(1)
                            self.ent.entradas["sensor_freno"] = True
                        else:
                            self.sal.salidas["frenos"] = False
                            baseDeTiempo.sleep(1)   
                            self.ent.entradas["sensor_freno"] = False
                            raise ParadaDeTurbina1("Parada de la Turbina , por Falla de ent.entradas criticas 1")
                        if self.ent.entradas.get("sensor_freno")  and self.inputs_criticas1:
                                baseDeTiempo.sleep(1)                               # aseguramos que la turbina no esté frenada  
                                self.inputs_criticas2 = (self.inputs_criticas1 and  self.sal.salidas.get("frenos") and
                                                         self.ent.entradas.get("sensor_freno")) 
                                if self.inputs_criticas2: 
                                    print("Acoplamos el motor auxiliar al eje y lo activamos")
                                    self.sal.salidas["juntaNeumat"] = True                           
                                    self.sal.salidas["motorAux"] = True
                                    self.ent.entradas["sensor_velTur"] = 0.0
                                    print("Se lleva  la turbina a velocidad de autosustentacion\n")
                                    while self.ent.entradas.get("sensor_velTur") < 478 and self.inputs_criticas2:
                                        baseDeTiempo.sleep(1)
                                        self.ent.entradas["sensor_velTur"] = (self.ent.entradas.get("sensor_velTur") 
                                        + 25.0 - self.friccion)  # rpm
                                        print(round(self.ent.entradas.get("sensor_velTur") , 2))
                                else:
                                    self.sal.salidas["juntaNeumat"] = False
                                    self.sal.salidas["motorAux"] = False
                                    self.sal.salidas["frenos"] = False
                                    baseDeTiempo.sleep(1)
                                    self.ent.entradas["sensor_freno"] = False
                                    raise ParadaDeTurbina1("Parada del Arranque de la Turbina , por Falla de entradas criticas 2")
                        else:
                            self.sal.salidas["juntaNeumat"] = False
                            self.sal.salidas["motorAux"] = False
                            self.sal.salidas["frenos"] = False
                            baseDeTiempo.sleep(1)
                            self.ent.entradas["sensor_freno"] = False
                            raise ParadaDeTurbina1("""Parada de la Turbina , por Turbina Frenada o Falla de 
                                                   entrada critica1""")
                    elif  self.ent.entradas.get("p_paradaTur") == False:
                        print("Parada de la Turbina , por pulsar p_paradaTur")
                        self.ent.entradas["p_paradaTur"] = True
                        self.ent.entradas["p_marchaTur"] = False
                        self.parada_controlada()
                if (self.ent.entradas.get("sensor_velTur") >= 478.0 and self.ent.entradas.get("sensor_velTur") < 
                    2750.0 and self.inputs_criticas2 and not self.ent.entradas.get("sensor_Q1")and not 
                    self.ent.entradas.get("sensor_Q2")):
                    print("""PASO 2:   
                        Una vez alcanzada la auto sustentación, se habilitan los chisperos y luego de 2 segundos se comanda el 
                        control de velocidad en MANUAL, abriendo la válvula de control de combustible un 10%, el cual 
                        comenzará a ingresar a través de 2 quemadores tangenciales.   
                        Con dos sensores de llama, se verifica que ambos quemadores estén encendidos para ir al siguiente 
                        paso\n """)
                    print("Con la Turbina en vel. de autosustentacion encendemos los quemadores  :  paso2\n")
                    print("Accionamos los Chisperos\n")
                    self.sal.salidas["ignitor1"] = True
                    self.sal.salidas["ignitor2"] = True
                    baseDeTiempo.sleep(2)
                    print("Abrimos 10% la valvula de combustible")
                    self.ent.entradas["sp_VComb"] = 10.0
                    self.sal.salidas["valvula_combustible"] = self.ent.entradas["sp_VComb"]
                    print("Se detecta llama ==> Quemadores encendidos")
                    self.ent.entradas["sensor_Q1"] = True
                    self.ent.entradas["sensor_Q2"] = True
                    self.inputs_criticas3 = (self.inputs_criticas2 and self.ent.entradas.get("sensor_Q1") and 
                                             self.ent.entradas.get("sensor_Q2"))
                print("""PASO 3:   
                    Se acelera constantemente la máquina con las válvulas de combustible FIJAS al 25%, hasta 
                    llegar a 2750 rpm. En este punto, se desacopla el motor auxiliar y 5 segundos después se apaga""")
                if (self.ent.entradas.get("sensor_velTur") >= 478.0 and self.ent.entradas.get("sensor_velTur")
                    < 2750.0 and self.inputs_criticas3):
                    print("Una vez que se verifca el encendido de los quemadores apagamos los chisperos")
                    self.sal.salidas["ignitor1"] = False
                    self.sal.salidas["ignitor2"] = False 
                    print("Con la Valvula de combustible al 25% aceleramos hasta 2750 rpm  :  self.paso3\n")
                    print("Abrimos la valvula de combustible al 25 %\n")
                    self.ent.entradas["sp_VComb"] = 25.0
                    self.sal.salidas["valvula_combustible"] = self.ent.entradas["sp_VComb"]
                    print("Se acelera la turbina por medio del combustible")
                    while self.ent.entradas.get("sensor_velTur")< 2750 and self.inputs_criticas3 :
                        baseDeTiempo.sleep(1)
                        if self.ent.entradas["sp_VComb"] == 25.0:
                            if self.ent.entradas.get("sensor_velTur") < 2750 :
                                self.ent.entradas["sensor_velTur"] = (self.ent.entradas.get("sensor_velTur") + 38.0 
                                - self.friccion - self.carga_compresor)
                                print(round(self.ent.entradas.get("sensor_velTur") , 2))
                print("""PASO 4:   
                        Al superar las 2750 rpm, se habilita el control externo en modo 
                        automático, con una consigna de 4600 rpm.""")
                if (self.ent.entradas.get("sensor_velTur") >= 2750 and self.inputs_criticas3 == True and 
                    self.ent.entradas.get("sensor_Q1") == True and self.ent.entradas.get("sensor_Q2") == True and 
                    self.ent.entradas.get("p_paradaTur") == True):
                    print("Se alcanzan las 2750 rpm , se desacopla el motor auxiliar")
                    self.sal.salidas["juntaNeumat"] = False
                    baseDeTiempo.sleep(5)
                    self.sal.salidas["motorAux"] = False
                    print("Motor auxiliar desacoplado")
                    print("Se habilita el control externo en modo automatico")
                    self.Man_Auto = True
                    print("Se establece la consigna de 4600 rpm")
                    self.ent.entradas["sp_Vel_Tur"] = 4600
                elif self.ent.entradas.get("sensor_velTur") >= 2750.0 :
                    self.parada()        
                else:
                    if self.ent.entradas.get("sensor_velTur") <= 478.0:
                        self.ent.entradas["sensor_velTur"] = False
                        self.sal.salidas["motorAux"] = False
                        self.sal.salidas["frenos"] = True
                        baseDeTiempo.sleep(5)
                        self.sal.salidas["frenos"] = False
                        self.parada()                    
                    elif self.ent.entradas.get("sensor_velTur") > 478.0:
                        self.parada()
                    raise ParadaDeTurbina1("Parada de la Turbina , por falla de ent.entradas criticas 2 ")  
            else:
                self.parada()
                raise ParadaDeTurbina1("Parada de la Turbina , por falla de ent.entradas criticas)")
        except ParadaDeTurbina1 as e:
            print(e)
        
    def modificar_ent(self):
        
        try:
            for llave, valor in self.ent.entradas.items():
                print(f" *Entrada : {llave}          *Estado :   {valor}")  
            entrada = input("Seleccione la entrada a modificar: ") 
            print("***************************************")
            print(f"Entrada a Modificar  :  {entrada}")
            print("***************************************")
            print("")
            print("")
            if type(self.ent.entradas.get(entrada)) == float:
                nuevo_valor = float(input(f" Nuevo valor de {entrada}: ") )
                self.ent.entradas.update({entrada : nuevo_valor}) 
                print("********************************")
                print("Entrada modificada con exito")
                print("********************************")
            elif type(self.ent.entradas.get(entrada)) == bool:
                if self.ent.entradas.get(entrada) == True:
                    self.ent.entradas.update({entrada : False})
                    print("********************************")
                    print("Entrada modificada con exito")
                    print("********************************")
                else:
                    self.ent.entradas.update({entrada : True})  
                    print("********************************")
                    print("Entrada modificada con exito")
                    print("********************************")
        except Exception as e :
            print("Vuelva a introducir la entrada")
            self.modificar_ent()
        
    def parada_controlada(self):
        
        print("************************************************")
        print("Inicio de Parada controlada de la Turbina")
        print("************************************************")
        self.ent.entradas["p_paradaTur"] = True
        self.ent.entradas["p_marchaTur"] = False  
        self.Man_Auto  = False
        print("\n")
        print("verificamos si la parada es a menos de 480 rpm")
        print("\n")
        if self.ent.entradas.get("sensor_velTur") >= 480.0:
            print("Parada controlada a mas de 480 rpm")
            print("Cerramos la valvula de combustible al 10%")
            self.ent.entradas["sp_VComb"] = 10.0
            baseDeTiempo.sleep(10)
            print("Cerramos la valvula de combustible")
            self.ent.entradas["sp_VComb"] = 0.0
            self.sal.salidas["valvula_combustible"] = self.ent.entradas.get("sp_VComb")
            self.ent.entradas["sensr_Q1"] = False
            self.ent.entradas["sensr_Q2"] = False
            baseDeTiempo.sleep(5)
            self.sal.salidas["valvulaPpal"] = False
            print("Desaceleramos la Turbina")
            while True:
                baseDeTiempo.sleep(1)
                if self.ent.entradas.get("sensor_velTur") < 2500:
                    break    
                self.ent.entradas["sensor_velTur"] = (self.ent.entradas.get("sensor_velTur") 
                                                      - self.friccion - self.carga_compresor) 
                print(round(self.ent.entradas.get("sensor_velTur") , 2))
        print("Frenamos la Turbina")
        self.sal.salidas["frenos"] = True
        while True:
            baseDeTiempo.sleep(1)   
            self.ent.entradas["sensor_velTur"] = (self.ent.entradas.get("sensor_velTur") 
                                                  - self.friccion - self.carga_compresor - 50.0)
            if self.ent.entradas.get("sensor_velTur") <= 0.0:
                self.ent.entradas["sensor_velTur"] = 0.0
                self.sal.salidas["frenos"] = False
                break
            print(round(self.ent.entradas.get("sensor_velTur") , 2))
        print ("Turbina detenida por Parada Controlada")
                      
    def parada(self):
        print("************************************************")
        print("Inicio de Parada de Emergencia de la Turbina")
        print("************************************************")
        self.ent.entradas["p_paradaTur"] = True
        self.ent.entradas["p_marchaTur"] = False    
        self.Man_Auto  = False
        print("Cerramos la valvula de combustible")
        self.ent.entradas["sp_VComb"] = 0.0
        self.sal.salidas["valvula_combustible"] = self.ent.entradas.get("sp_VComb")
        print("Quemadores apagados")
        self.ent.entradas["sensr_Q1"] = False
        self.ent.entradas["sensr_Q2"] = False
        print("Ciclo de quema de gases reciduales en la Turbina")
        self.sal.salidas["valvulaEscape"] = True
        self.sal.salidas["ignitorEmerg"] = True
        baseDeTiempo.sleep(5)
        self.ent.entradas["sensr_QEmer"] = True
        if self.ent.entradas.get("sensr_QEmer") == True:
            self.sal.salidas["ignitorEmerg"] = False
            baseDeTiempo.sleep(30)
            self.sal.salidas["valvulaEscape"] = False
            self.ent.entradas["sensr_QEmer"] = False
        print("Frenamos la Turbina")
        self.sal.salidas["frenos"] = True    
        while True:
            baseDeTiempo.sleep(1)   
            self.ent.entradas["sensor_velTur"] = (self.ent.entradas.get("sensor_velTur") 
                                                  - self.friccion - self.carga_compresor - 150.0)
            if self.ent.entradas.get("sensor_velTur") <= 0.0:
                self.ent.entradas["sensor_velTur"] = 0.0
                self.sal.salidas["frenos"] = False
                baseDeTiempo.sleep(5)
                break
            print(round(self.ent.entradas.get("sensor_velTur") , 2))
            
        print("Turbina Parada de Emergencia")

    def PID(self, input, Man_Auto = False, SetpointMan = 0.0, SetpointAuto = 0.0):
            
            """
                Calcula la salida de un controlador PID (Proporcional, Integral, Derivativo).
                Args:
                Man_Auto (bool): Modo manual (True) o automático (False).
                    SetpointMan (bool): Ignorado si Man_Auto es True. Modo manual de 
                    setpoint (True) o automático (False).
                    SetpointAuto (float): El valor del setpoint en modo automático.
                Returns:
                    None
                El método calcula la salida del controlador PID utilizando el valor actual
                (input) y el setpoint (SetpointAuto).
                Se almacena el histórico de velocidades en self.anteriores y se limita a 
                100 elementos.
                Se calculan los componentes P, I y D del controlador y se suman para 
                obtener la salida.
                La salida se limita al rango de 0 a 100.
            """
            if Man_Auto == False:     
                # Si el PID está en modo automático...
                # Almaceno el vector velocidad en una lista de 100 elementos.
                self.anteriores.append(input)
                if len(self.anteriores) > 100:
                    self.anteriores = self.anteriores[-100:]
                SP = SetpointAuto        
                E = SP - input
                self.error = E 
                #error es la diferencia entre lo que tengo, y mi setpoint actual. Usamos la
                #lista para ello. 
                E_accu = [(SP - elem) for elem in self.anteriores[-20:]]
                self.error_accu = E_accu
                kP = 10.0
                kI = 0.0001
                kD = 0.01
                #La acción proporcional es el error multiplicado por una constante
                aP = self.error * kP
                #La acción integral es el área de los valores, dividido por la constante
                aI = (kP * (sum(self.error_accu) / (len(self.error_accu)*0.002) * kI))
                #La acción derivativa es la proyección a futuro (pendiente) del error, multiplicado por una 
                # constante
                if len(self.anteriores)>2:
                    aD = (self.error_accu[-1]-self.error_accu[-2])*kD*kP
                else:
                    aD = 0.0
                #sumamos las componentes de las acciones Proporcional, Integral y Derivativa
                Salida = self.Valvula + aP + aI + aD
                # Limitamos la salida al rango de 0 a 100
                if Salida < 0:
                    self.Valvula = 0
                elif Salida > 100:
                    self.Valvula = 100         
                else:
                    self.Valvula = Salida
            else:
                # Si estamos en modo "Manual", la válvula se pone en la posición que definimos 
                # en el setpoint.
                self.Valvula = SetpointMan
    
    def grafico_Velocidad(self, velocidad_turbina ,tiempo_actual):  
        
        """
            Grafica la velocidad de la turbina en un gráfico de líneas.
            Utiliza matplotlib para crear el gráfico.
        """
        plt.style.use('_mpl-gallery')               
        # Crear una figura y un eje
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
        
        def init():
            ax.set_ylim(0, 6000)  # Ajustá según el rango esperado de Y
            ax.set_xlim(0, 120)  # Ajustá según el rango esperado de X
            return line,
        
        def update(frame):
            x_data.append(tiempo_actual)    
            valor_y = velocidad_turbina
            y_data.append(valor_y)
            # Mantenemos solo los últimos 100 puntos
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)
            # Actualizamos los datos de la línea   
            line.set_data(x_data, y_data)
            return line,
               
        ani = FuncAnimation(fig, update, init_func=init, interval=100, blit=False)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    
    
    def __str__(self):
        for llave, valor in self.ent.entradas.items():
            print(f" *Entrada : {llave}          *Estado :   {valor}")
            

class EntradasPlc():
    
    def __init__(self):
        # entradas
        self.entradas = {
        "pE_SControl": True,  
        "pE_Remota": True,
        "p_valPpalAbi": False,
        "p_marchaTur": False ,
        "p_paradaTur": True,
        "sel_loc_rem": False,
        "sensor_freno": True,
        "sensor_Q1": False,
        "sensor_Q2": False,
        "sensr_QEmer": False,
        "sp_VComb": 0.0,
        "sp_Vel_Tur": 0.0,
        "sensor_valvppal": False,
        "sensor_Tq": 0.0,
        "sensor_preCom": 0.0,
        "sensor_velTur": 0.0
        }
        
    def __str__(self):
        for llave, valor in self.entradas.items():
            print(f" *Entrada : {llave}          *Estado : {valor}")
      
    
class SalidasPlc():
        # SALIDAS
    
    def __init__(self):
        self.salidas = {
            "frenos":  False ,
            "motorAux": False,
            "juntaNeumat": False,
            "ignitor1":   False,
            "ignitor2":  False,
            "ignitorEmerg":  False,
            "valvulaEscape":  False,
            "valvulaPpal":  False,
            "valvula_comb": 0.0
            }
            
    def __str__(self):
        for llave, valor in self.salidas.items():
            print(f" *Salida : {llave}          *Estado :   {valor}")


class ParadaDeTurbina1(Exception):
        
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return (f"Causa de Parada de la Turbina: {self.mensaje}")
    
    
print("comienzo de programa")


tur = Turbina()

try:

    print("***************************************")
    print("Simulación de Turbina de Gas")
    print("programa on")
    print("***************************************\n")
    while True:

        a = 0
        while a < 1:
            print("***************************************")
            print("Modificación de Entradas de la Turbina")
            print("***************************************")
            print("\n")
            print("En el arranque abrir primero la valvula Ppal.")
            print("\n")
            print("Luego se puede seleccionar la entrada a modificar por ej. parar la Turbina o entrar en emergencia etc.etc..")
            print("\n")
            print("***************************************")
            print("\n")
            tur.modificar_ent()
            a += 1

        tur.update()
        print("\n")
        print("***************************************")
        print("Tiempo de espera entre actualizaciones")
        print("***************************************")
        print("\n")
        baseDeTiempo.sleep(1)


except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")



