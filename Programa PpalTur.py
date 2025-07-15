from IOdelPLC import (EntradasPlc, SalidasPlc)
import threading as hilo
import time as baseDeTiempo
from SimulTurbinaGas import Turbina


print ("comienzo de programa")

 
entradas = EntradasPlc()
salidas = SalidasPlc()
tur = Turbina()

try:
    print ("programa on")
    while True:
        print(entradas.__str__())
        
        tur.update()
        
        baseDeTiempo.sleep(1)
        """a = 0
        while a < 1 :
            tur.modificar_ent()
            a += 1"""
        
        
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
    
