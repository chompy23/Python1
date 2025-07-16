import time as basedetiempo

class EntradasPlc():
    def __init__(self):
        # entradas
            
        self.entradas = {
        "pE_SControl" : True,  
        "pE_Remota" : True,
        "p_valPpalAbi" : False,
        "p_marchaTur"  : False ,
        "p_paradaTur"  : True,
        "sel_loc_rem"  : False,
        "sensor_freno"  : True,
        "sensor_Q1"  : False,
        "sensor_Q2"   : False,
        "sensr_QEmer"  : False,
        "sp_VComb"  : 0.0,
        "sp_Vel_Tur"  : 0.0,
        "sensor_valvppal"  : False,
        "sensor_Tq"  : 0.0,
        "sensor_preCom"  : 0.0,
        "sensor_velTur" : 0.0
        }
        
            
        
    def modificar(self):
        try:
                     
            self.__str__()
                
            entrada = input("Seleccione la entrada a modificar: ") 
            print("***************************************")
            print(f"Entrada a Modificar  :  {entrada}")
            print("***************************************")
            
            if type(self.entradas[entrada]) == float:
                nuevo_valor = float(input(f" Nuevo valor de {entrada}: ") )
                self.entradas[entrada] = nuevo_valor
            else:
                if self.entradas[entrada] == True:
                    self.entradas[entrada] = False
                    
                else:
                    self.entradas[entrada] = True
                
                
            print("********************************")
            print("Entrada modificada con exito")
            print("********************************")
            
        except Exception as e :
            print("Vuelva a introducir la entrada")
            self.modificar()

              
        
    def __str__(self):
        for llave, valor in self.entradas.items():
            print(f" *Entrada : {llave}          *Estado :   {valor}")
      
    
class SalidasPlc():
        # SALIDAS
    
    def __init__(self):
        
        self.salidas = {
            "frenos"  :  False ,
            "motorAux" : False,
            "juntaNeumat"  : False,
            "ignitor1"  :   False,
            "ignitor2"  :  False,
            "ignitorEmerg"  :  False,
            "valvulaEscape"  :  False,
            "valvulaPpal"  :  False,
            "valvula_comb" : 0.0
            }
            
        
        
    def __str__(self):
        for llave, valor in self.salidas.items():
            print(f" *Salida : {llave}          *Estado :   {valor}")
