import time as baseDeTiempo
from IOdelPLC import EntradasPlc, SalidasPlc
from ExcepcionesTurbina import ParadaDeTurbina1

    
    
class Turbina():
    # Rango de Velocidad de la Turbima en [rpm]
    velTurbRpmMin = 0
    velTurbRpmMax = 6000 
   
    vel_turb_rpm = 0.0
        
    
    def __init__(self):
        #self.paso1 = self.paso2 = self.paso3 = self.paso4 = False                                           
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
            # Seguridades
            
            """ self.inputs_criticas1 = self.inputs_criticas and self.ent.entradas.get("p_paradaTur")
            self.inputs_criticas2 = self.inputs_criticas1 and  self.sal.salidas.get("frenos") and self.ent.entradas.get("sensor_freno") 
            self.inputs_criticas3 = self.inputs_criticas2 and self.ent.entradas.get("sensor_Q1")and self.ent.entradas.get("sensor_Q2")"""
            
            if self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota") and self.ent.entradas.get("p_valPpalAbi") and self.ent.entradas.get("p_paradaTur"):
            
                print("Valvula Ppal. abierta \n")
                self.ent.entradas["sensor_valvppal"] = True
            else:    
            
                while self.ent.entradas.get("p_valPpalAbi") == False and self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota") and self.ent.entradas.get("p_paradaTur"):   #  valvula ppal. cerrada
                    
                    print ("valvula Ppal. cerrada \n")
                    print (" pulsar p_valPpalAbi Para abrir la valvula \n")
                    baseDeTiempo.sleep(1)
                    
                    self.modificar_ent()
                    
                    #print(self.ent.entradas["p_valPpalAbi"]) 
                    
                    self.ent.entradas["sensor_valvppal"] = True
                    baseDeTiempo.sleep(1)
                    if self.ent.entradas.get("sensor_valvppal") == True:
                        break
                    
                
            
            """
                PASO 1:
                Para el arranque con la turbina completamente detenida, se utiliza un motor auxiliar, que se acopla 
                mediante una junta neumática comandada desde el PLC y mueve el eje completo de la turbina hasta 
                llegar a la velocidad de auto sustentación (478 rpm). Si la válvula principal manual no está abierta, no 
                se puede ejecutar el arranque.   
                
            """
            self.inputs_criticas = self.ent.entradas.get("pE_SControl") and self.ent.entradas.get("pE_Remota") and self.ent.entradas.get("sensor_valvppal")
            
            if self.inputs_criticas:
                vel_turb_rpm = self.ent.entradas.get("sensor_velTur")
                if  self.ent.entradas.get("p_paradaTur") == False:
                        self.parada_controlada()
                if vel_turb_rpm <= 0.0 and self.inputs_criticas :
                    
                    
                    print("Comienza el ciclo de encendido de la Turbina : self.paso1 \n")
                    
                    while self.ent.entradas.get("p_marchaTur") == False:
                        print("Pulsar p_marchaTur para iniciar el arranque de la Turbina \n")
                        self.modificar_ent()
                        if self.ent.entradas.get("p_marchaTur") or self.ent.entradas.get("p_paradaTur") == True:
                            break
                        
                        baseDeTiempo.sleep(1)
                    if self.ent.entradas.get("p_marchaTur"):     # inicia la secuencia de arranque de la turbina
                        
                        print("Ponemos en modo manual el control de velocidad")
                        
                        self.Man_Auto  = False                      # control de la valvula de combustible en manual
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
                                self.inputs_criticas2 = self.inputs_criticas1 and  self.sal.salidas.get("frenos") and self.ent.entradas.get("sensor_freno") 
                                if self.inputs_criticas2: 
                                    
                                    print("Acoplamos el motor auxiliar al eje y lo activamos")
                                    
                                    self.sal.salidas["juntaNeumat"] = True                           
                                    self.sal.salidas["motorAux"] = True
                                    vel_turb_rpm = 0.0
                                    
                                    print("Se lleva  la turbina a velocidad de autosustentacion")
                                    
                                    while vel_turb_rpm < 478 and self.inputs_criticas2:
                                        baseDeTiempo.sleep(1)
                                        vel_turb_rpm = vel_turb_rpm + 25.0 - self.friccion  # rpm
                                        self.ent.entradas["sensor_velTur"] = vel_turb_rpm
                                        
                                        print (self.ent.entradas["sensor_velTur"])
                                        
                                    
                                else:
                                                                       
                                    self.sal.salidas["juntaNeumat"] = False
                                    self.sal.salidas["motorAux"] = False
                                    self.sal.salidas["frenos"] = False
                                    baseDeTiempo.sleep(1)
                                    self.ent.entradas["sensor_freno"] = False
                                    
                                    raise ParadaDeTurbina1("Parada del Arranque de la Turbina , por Falla de ent.entradas criticas 2")
                    
                    
                        else:
                                                       
                            self.sal.salidas["juntaNeumat"] = False
                            self.sal.salidas["motorAux"] = False
                            self.sal.salidas["frenos"] = False
                            baseDeTiempo.sleep(1)
                            self.ent.entradas["sensor_freno"] = False
                            
                            raise ParadaDeTurbina1("Parada de la Turbina , por Turbina Frenada o Falla de entrada critica1")
                    
                    elif  self.ent.entradas.get("p_paradaTur") == True:
                        self.parada_controlada()
            
                
                if vel_turb_rpm >= 478.0 and vel_turb_rpm < 2750.0 and self.inputs_criticas2 and not self.ent.entradas.get("sensor_Q1")and not self.ent.entradas.get("sensor_Q2"):
                    """PASO 2:   
                        Una vez alcanzada la auto sustentación, se habilitan los chisperos y luego de 2 segundos se comanda el 
                        control de velocidad en MANUAL, abriendo la válvula de control de combustible un 10%, el cual 
                        comenzará a ingresar a través de 2 quemadores tangenciales.   
                        Con dos sensores de llama, se verifica que ambos quemadores estén encendidos para ir al siguiente 
                        paso """
                    
                    
                    print("Con la Turbina en vel. de autosustentacion encendemos los quemadores  :  paso2")
                    
                    print("Accionamos los Chisperos")
                    
                    self.sal.salidas["ignitor1"] = True
                    self.sal.salidas["ignitor2"] = True
                    baseDeTiempo.sleep(2)
                    
                    print("Abrimos 10% la valvula de combustible")
                    
                    self.ent.entradas["sp_VComb"] = 10.0
                    self.sal.salidas["valvula_combustible"] = self.ent.entradas["sp_VComb"]
                    
                    print("Se detecta llama ==> Quemadores encendidos")
                    
                    self.ent.entradas["sensor_Q1"] = True
                    self.ent.entradas["sensor_Q2"] = True
                    
                    self.inputs_criticas3 = self.inputs_criticas2 and self.ent.entradas.get("sensor_Q1")and self.ent.entradas.get("sensor_Q2")
                    
                if vel_turb_rpm >= 478.0 and vel_turb_rpm < 2750.0 and self.inputs_criticas3:
                    
                    """PASO 3:   
                    Se acelera constantemente la máquina con las válvulas de combustible FIJAS al 25%, hasta llegar a 
                    2750 rpm. En este punto, se desacopla el motor auxiliar y 5 segundos después se apaga"""
                    print("Una vez que se verifca el encendido de los quemadores apagamos los chisperos")
                    
                    self.sal.salidas["ignitor1"] = False
                    self.sal.salidas["ignitor2"] = False 
                    
                    print("Con la Valvula de combustible al 25% aceleramos hasta 2750 rpm  :  self.paso3")
                    
                    print("Abrimos la valvula de combustible al 25 %")
                    
                    self.ent.entradas["sp_VComb"] = 25.0
                    self.sal.salidas["valvula_combustible"] = self.ent.entradas["sp_VComb"]
                    
                    print("Se acelera la turbina por medio del combustible")
                    
                    while vel_turb_rpm < 2750 and self.inputs_criticas3 :
                        baseDeTiempo.sleep(1)
                        
                        if self.ent.entradas["sp_VComb"] == 25.0:
                            if vel_turb_rpm < 2750 :
                                vel_turb_rpm = vel_turb_rpm + 38.0 - self.friccion - self.carga_compresor
                                self.ent.entradas["sensor_velTur"] = vel_turb_rpm
                                print(round(self.ent.entradas["sensor_velTur"] , 2))

                        
                if vel_turb_rpm >= 2750 and self.inputs_criticas3 :
                    """PASO 4:   
                        Al superar las 2750 rpm, se habilita el control externo en modo automático, con una consigna de 4600 
                        rpm."""
                        
                    print("Se alcanzan las 2750 rpm , se desacopla el motor auxiliar")
                    
                    
                    self.sal.salidas["juntaNeumat"] = False
                    baseDeTiempo.sleep(5)
                    self.sal.salidas["motorAux"] = False
                    self.Man_Auto = True
                    self.ent.entradas["sp_Vel_Tur"] = 4600
                    
                    """elif not self.inputs_criticas3 :
                        self.parada()                            
                        raise ParadaDeTurbina1("Parada de la Turbina , por Falla de ent.entradas criticas 3")"""
                            
                        

                else:
                    
                    if vel_turb_rpm <= 478.0:
                        self.sal.entradas["sensor_velTur"] = False
                        self.sal.salidas["motorAux"] = False
                        self.sal.salidas["frenos"] = True
                        baseDeTiempo.sleep(5)
                        self.sal.salidas["frenos"] = False
                        
                        
                    elif vel_turb_rpm > 478.0:
                        self.parada()
                        
                    raise ParadaDeTurbina1("Parada de la Turbina , por falla de ent.entradas criticas 2 ")  
            
            else:
                
                raise ParadaDeTurbina1("Parada de la Turbina , por falla de ent.entradas criticas====))")
        
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
        self.Man_Auto  = False
        self.ent.entradas["sp_VComb"] = 10.0
        baseDeTiempo.sleep(10)
        self.ent.entradas["sp_VComb"] = 0.0
        self.ent.entradas["sensr_Q1"] = False
        self.ent.entradas["sensr_Q2"] = False
        self.sal.salidas["valvula_combustible"] = self.ent.entradas["sp_VComb"]
        self.sal.salidas["valvulaEscape"] = True
        baseDeTiempo.sleep(5)
        self.sal.salidas["valvulaPpal"] = False
        while True:
            baseDeTiempo.sleep(1)   
            vel_turb_rpm = vel_turb_rpm - self.friccion - self.carga_compresor
            if vel_turb_rpm < 2500:
                break 
        self.sal.salidas["frenos"] = True
        while True:
            baseDeTiempo.sleep(1)   
            vel_turb_rpm = vel_turb_rpm - self.friccion
            if vel_turb_rpm <= 0.0:
                break
        
        print ("Turbina detenida por Parada Controlada")
                      
    def parada(self):
        self.Man_Auto  = False
        self.ent.entradas["sp_VComb"] = 0.0
        self.sal.salidas["valvulaEscape"] = True
        self.sal.salidas["ignitorEmerg"] = True
        baseDeTiempo.sleep(5)
        self.ent.entradas["sensr_QEmer"] = True
        if self.ent.entradas["sensr_QEmer"] :
            self.sal.salidas["ignitorEmerg"] = False
            self.sal.salidas["frenos"] = True  
            baseDeTiempo.sleep(30)
            self.sal.salidas["valvulaEscape"] = False
            self.ent.entradas["sensr_QEmer"] = False
        
            
            
        print ("Turbina Parada")

    def PID(self,input, Man_Auto  = False, SetpointMan = 0.0, SetpointAuto = 0.0):
            """
                Calcula la salida de un controlador PID (Proporcional, Integral, Derivativo).

                Args:
                    Man_Auto (bool): Modo manual (True) o automático (False).
                    SetpointMan (bool): Ignorado si Man_Auto es True. Modo manual de setpoint (True) o automático (False).
                    SetpointAuto (float): El valor del setpoint en modo automático.

                Returns:
                    None

                El método calcula la salida del controlador PID utilizando el valor actual (input) y el setpoint (SetpointAuto).
                Se almacena el histórico de velocidades en self.anteriores y se limita a 100 elementos.
                Se calculan los componentes P, I y D del controlador y se suman para obtener la salida.
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
                
                #error es la diferencia entre lo que tengo, y mi setpoint actual. Usamos la lista para ello. 
                E_accu = [(SP - elem) for elem in self.anteriores[-20:]]
                self.error_accu = E_accu
                
                kP = 10.0
                kI = 0.0001
                kD = 0.01

                #La acción proporcional es el error multiplicado por una constante
                aP = self.error * kP
                
                #La acción integral es el área de los valores, dividido por la constante
                aI = (kP * (sum(self.error_accu) / (len(self.error_accu)*0.002) * kI))

                #La acción derivativa es la proyección a futuro (pendiente) del error, multiplicado por una constante
                if len(self.anteriores)>2:
                    aD = (self.error_accu[-1]-self.error_accu[-2])*kD*kP
                else:
                    aD = 0.0
                
                #sumamos las componentes de las acciones Proporcional, Integral y Derivativa
                Salida = self.Valvula + aP + aI + aD

                #Limitamos la válvula de salida
                if Salida < 0:
                    self.Valvula = 0
                elif Salida > 100:
                    self.Valvula = 100         
                else:
                    self.Valvula = Salida

            else:
                # Si estamos en modo "Manual", la válvula se pone en la posición que definimos en el setpoint.
                self.Valvula = SetpointMan
    
    def __str__(self):
        for llave, valor in self.ent.entradas.items():
            print(f" *Entrada : {llave}          *Estado :   {valor}")



