# Programa principal para la simulación de una turbina de gas
# Este programa interactúa con IOdelPLC.py para modificar entradas y salidas de la turbina
# y maneja excepciones definidas en ExcepcionesTurbina.py.  
# Importación de módulos necesarios
import time as baseDeTiempo
from SimulTurbinaGas import Turbina


print ("comienzo de programa")

 

tur = Turbina()

try:
        
    print("***************************************")
    print("Simulación de Turbina de Gas")
    print ("programa on")
    print("***************************************\n")
    while True:
        
        a = 0
        while a < 1 :
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
        print ("Tiempo de espera entre actualizaciones")
        print("***************************************")
        print("\n")
        baseDeTiempo.sleep(1)
        
        
        
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
    
