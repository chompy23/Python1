# Programa principal para la simulación de una turbina de gas
# Este programa interactúa con IOdelPLC.py para modificar entradas y salidas de la turbina
# y maneja excepciones definidas en ExcepcionesTurbina.py.  
# Importación de módulos necesarios
import time as baseDeTiempo
from SimulTurbinaGas import Turbina


print ("comienzo de programa")

 

tur = Turbina()

try:
    print ("programa on")
    while True:
        
        a = 0
        while a < 1 :
            tur.modificar_ent()
            a += 1
                
        tur.update()
        
        baseDeTiempo.sleep(15)
        
        
        
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
    
