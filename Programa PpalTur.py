from IOdelPLC import (EntradasPlc, SalidasPlc)
import threading as hilo
import time as baseDeTiempo
from SimulTurbinaGas import Turbina


print ("comienzo de programa")

 
#entradas = EntradasPlc()
#salidas = SalidasPlc()
tur = Turbina()

try:
    print ("programa on")
    while True:
        
        """print(tur.__str__())
        
        while baseDeTiempo.sleep(10) == False:
            tur.modificar_ent()
            baseDeTiempo.sleep(1)"""    
        
        print("***************************************")
        print("Modificacion de entradas")
        a = 0
        while a < 1 :
            tur.modificar_ent()
            a += 1
        
        
        print("***************************************")
        
        tur.update()
        
        baseDeTiempo.sleep(15)
        
        
        
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
    
