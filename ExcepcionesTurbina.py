
class ParadaDeTurbina1(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
        
    def __str__(self):
        return (f"Causa de Parada de la Turbina: {self.mensaje}")
        
    

