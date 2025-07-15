import time
import math

class Tanque :
    nivelActual = 0.0
    caudal = 0.0
    volumenActual = 0.0
    volumenMaximo = 0.0
    
    
    def __init__(self, diametro = 1.0, altura = 1.0, valvulas = [], tiempoUpdate=10): #diametro y altura en metros
        self.diametro = diametro
        self.altura = altura
        self.valvulas = valvulas
        self.tiempoUpdate = tiempoUpdate
    
    def calcularNivel(self):
        self.volumenMaximo = round((self.altura * ((self.diametro/2)**2) * math.pi) * 1000 , 2) # volumen máximo en litros
        print("El volumen maximo es : ", self.volumenMaximo, " Litros")
        self.nivelActual = round((self.volumenActual / self.volumenMaximo) * 100 , 2) # nivel actual en %
        
         
    acumuladorDeTiempo = 0
    def update(self, tiempo): #El parámetro "tiempo" en segundos sirve para ver cada cuánto se actualiza el nivel del tanque.
        self.acumuladorDeTiempo += tiempo 
        print(" El acumuladorDeTiempo es = ", self.acumuladorDeTiempo , " seg.")
        
        # Calculo el volumen durante el llenado del Tanque
        if self.caudal > 0 :
                self.volumenActual = self.caudal * self.acumuladorDeTiempo
                print(" El volumenActual es = ", self.volumenActual, " litros ")
                self.calcularNivel() 
        
        # Calculo el volumen durante el vaciado del tanque
        elif self.caudal < 0 :
                self.volumenActual += self.caudal * tiempo
                print(" El volumenActual es = ", self.volumenActual, " litros ")
                self.calcularNivel() 
                       
    
    def cargarTanque(self):
        self.tiempoUpdate = 10
        print(" El nivel actual es  : ", self.nivelActual)
        if self.nivelActual < 100.00:
            try:
                for valvesIngreso in self.valvulas:
                    if valvesIngreso.tipo != "E" and valvesIngreso.tipo != "S":
                        raise ErrorDeTipo(valvesIngreso.tipo)
                    
                    if valvesIngreso.tipo == "E":
                       valvesIngreso.abrirValvula()
                       self.caudal += valvesIngreso.caudalActual 
                       print(self.caudal)
                    elif valvesIngreso.tipo == "S":
                         valvesIngreso.cerrarValvula
           
                       
                tiempoEspera = 0 
                a = 0 
                while tiempoEspera < self.tiempoUpdate :
        # A partir del 84% del nivel calculo el tiempo para completar el nivel del tanque con un error de +-1% 
             
                  if (self.nivelActual >= 84.00) and (self.nivelActual <= 100.0) and (self.tiempoUpdate != math.ceil(a)):
                     a = (self.volumenMaximo - self.volumenActual) / self.caudal
                     self.tiempoUpdate = math.ceil(a)
                
                  time.sleep(1)
                  tiempoEspera +=1
            
                  while (self.nivelActual < 100.00) and (tiempoEspera == self.tiempoUpdate) :
                    self.update(tiempoEspera)
                    tiempoEspera = 0 
                    print(f"El nivel es  :  {self.nivelActual} %")
                 
                    if self.nivelActual > 99.99:
                       for valvesIngreso in self.valvulas:
                          if valvesIngreso.tipo == "E":
                             valvesIngreso.cerrarValvula()
                  #tiempoEspera = self.tiempoUpdate               
                self.acumuladorDeTiempo = 0
                self.caudal = 0
                
            except ErrorDeTipo as e :
                print (e)       
        else:
            print("Tanque lleno")        
    
    def vaciarTanque(self):
        self.tiempoUpdate = 10
        if self.nivelActual > 0:
            try:
                for valvesIngreso in self.valvulas:
                    if valvesIngreso.tipo != "E" and valvesIngreso.tipo != "S":
                        raise ErrorDeTipo( valvesIngreso.tipo)
                    if valvesIngreso.tipo == "S":
                       valvesIngreso.abrirValvula()
                       self.caudal += valvesIngreso.caudalActual 
                       print(self.caudal)
                    elif valvesIngreso.tipo == "E":
                       valvesIngreso.cerrarValvula
            
           
        
                tiempoEspera = 0 
                b = 0 
                while tiempoEspera < self.tiempoUpdate :
            # A partir del 10% del nivel calculo el tiempo para vaciar el tanque con un error de +-1% 
             
                     if (self.nivelActual <= 24.00) and (self.nivelActual > 0.0) and (self.tiempoUpdate != math.ceil(b)):
                        b = (self.volumenActual) / int(abs(self.caudal))
                        self.tiempoUpdate = math.ceil(b)
                
                     time.sleep(1)
                     tiempoEspera += 1
                     while (self.nivelActual > 0) and (tiempoEspera == self.tiempoUpdate) :
                           self.update(tiempoEspera)
                           tiempoEspera = 0 
                           print(f"El nivel es  :  {self.nivelActual} %")
                           if self.nivelActual <= 0:
               
                              for valvesIngreso in self.valvulas:
                                 if valvesIngreso.tipo == "S":
                                    valvesIngreso.cerrarValvula()
                    # tiempoEspera = self.tiempoUpdate               
                self.acumuladorDeTiempo = 0
                self.caudal = 0
            except ErrorDeTipo as e  :
                print (e)       
        else:
            print("Tanque vacio")
    
class Valvula:
    caudalActual = 0.0
    def __init__(self, tipo = "E", caudal = 1.0, ): # los valores posibles de la variable "tipo" son , "E"(de Entrada) o "S"(de Salida)
        self.tipo = tipo
        self.caudal = caudal
        
    def abrirValvula(self):
        try:
            if self.tipo == ("E"):
              self.caudalActual = self.caudal
            elif self.tipo == ("S"):
              self.caudalActual = -(self.caudal)
            else:
              raise ErrorDeTipo(self.tipo)   
        except ErrorDeTipo as e :
            print (e)         
        
        
    def cerrarValvula(self):
        self.caudalActual = 0.0
         
        
class ErrorDeTipo(Exception):
    
    def __init__(self, valor):
       self.valor = valor             
    
    def __str__(self):
       return (f"El Tipo {self.valor} es una selección erronea") 
        
V1 = Valvula("E", 20.0) # caudal en litros/seg
V2 = Valvula("E", 30.0)
V3 = Valvula("S", 60.0)

listadoDeValvulas = [V1, V2, V3]
Tk1 = Tanque(1.25, 5.2, listadoDeValvulas, 10)

Tk1.cargarTanque()
print("El caudal es : " , Tk1.caudal)
print("El volumen actual es : ", Tk1.volumenActual)
print(V1.caudalActual)
print(V2.caudalActual)
print(Tk1.nivelActual)

Tk1.vaciarTanque()
print(V1.caudalActual)
print(V2.caudalActual)
print(Tk1.nivelActual)
