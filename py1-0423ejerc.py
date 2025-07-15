"""
temperaturas = [26.75431352056954, 21.991086464852872, 27.209759257701366, 23.443668324912598, 28.8725217962772, 20.731695645337763, 
 22.58962536117254, 24.846285051127114, 26.074481791289337, 22.085936681499903, 23.913576519730877, 27.678759112104154, 24.381354548084965,
 23.19239923228099, 20.803472013144523, 21.30390306534694, 27.102859960400624, 23.763191774421054, 25.157825319899203, 20.2290281340311,
 26.746902019682647, 22.750408458130667, 20.26298637657635, 26.423788201931604
]

Maximo = round(max(temperaturas),3)
Minimo = round(min(temperaturas),3)
Promedio = round((sum(temperaturas) / len(temperaturas)),3)

print(len(temperaturas))
print (f"el valor maximo de la lista de Temperaturas es : {Maximo}")
print (f"el valor minimo de la lista de Temperaturas es : {Minimo}")
print (f"el valor del promedio  de la lista de Temperaturas es : {Promedio}")
"""

"""
estadoSensores = [True, True, True, False, False, False, True, False, True, False, False, True, True, 
                  False, False, True, False, False, False, True,True, False, False, False, True, True, True, 
                  False, True, True, True, False, False, True, False, False, False, True,True, False
                  ]

bueno = estadoSensores.count(False)
falla = estadoSensores.count(True)

sensores = {
    "correctos":bueno,
    "fallados":falla 
}
print(f"Hay {sensores['correctos']} Sensores OK y {sensores['fallados']} Sensores en falla")
"""



"""

Temperaturas1=[27.1, 22.3, 26.8, 23.5, 22.7, 15.3, 26.6, 16.9, 18.1, 24.7, 23.8, 18.4, 26.1, 27.5, 
               27.3, 21.9, 25.4, 25.1, 20.4, 16.2, 27.5, 22.7, 25.9, 21.2
]

Temperaturas2=[25.4, 21.5, 27.3, 25.5, 20.2, 26.6, 16.1, 27.7, 26.4, 24.0, 22.6, 19.4, 27.0, 18.3,
               25.0, 24.3, 25.6, 27.1, 15.6, 27.1, 26.6, 22.7, 20.4, 23.3
]

Temperaturas3=[16.4, 20.5, 23.5, 17.3, 26.2, 26.2, 22.9, 21.2, 24.2, 26.0, 18.7, 27.5, 25.0, 22.7, 
               21.7, 22.7, 23.3, 25.0, 26.7, 18.7, 19.6, 23.9, 20.0, 17.2
]

valores_calculados = ()
def analisis_de_valores (nombre_lista) :
    num = 0
    a = round(sum(nombre_lista)/len(nombre_lista),2)
    b = min(nombre_lista)
    c= max(nombre_lista)
    for valor in nombre_lista :
        if valor < 22.0 :
           num = num + 1
    d = num
    valores_calculados = (a,b,c,d)
    return valores_calculados
    

def  mostrar(datos) :
    print(f"El promedio es : {datos[0]} , el valor mínimo de temperatura es : {datos[1]}, el valor máximo de temperatura es {datos[2]} y la cantidad de temperaturas por debajo de 22.0 es : {datos[3]}") 
    num = 0

impresion = analisis_de_valores(Temperaturas3)
mostrar(impresion)

"""

"""
maximo_ing = 32767
minimo_ing = 0
maximo_salida = 100
minimo_salida = 0

valor_analogico= int(input("ingrese el valor analogico : "))

def EscalarValores(valor , maximo_ing = 32767 , minimo_ing = 0, maximo_salida = 100.0, minimo_salida = 0.0) :
    return (valor * maximo_salida)/maximo_ing

valor_escalado = EscalarValores(valor_analogico,maximo_ing, minimo_ing, maximo_salida, minimo_salida)

print(f"El valor escalado es  :  {valor_escalado} %")
"""

"""
productos_stock = {'producto1': 15, 'producto2': 7, 
                 'producto3': 11, 'producto4': 5
}


Punto_de_reposicion = 10

for clave, valor in productos_stock.items() :
    if valor < 10 :
        print(f"{clave} : {valor}")
"""

"""
Temperaturas = [28, 29, 31, 27, 33, 29, 30, 31, 32, 28]
umbral = 30 

Temperaturas_anormales = [valores for valores in Temperaturas if valores > umbral]

print(Temperaturas_anormales )
"""