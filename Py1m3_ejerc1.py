# Introducimos  los valores de los catetos
cat_adyacente = float(input("Valor del cateto adyacente : "))
cat_opuesto = float(input("Valor cel cateto opuesto : "))

hipotenusa = ((cat_adyacente ** 2) + (cat_opuesto ** 2)) ** (1/2) 
#print(f"El valor de la Hipotenusa es : {hipotenusa}")
print ("La Hipotenusa del triangulo es : ", hipotenusa)
