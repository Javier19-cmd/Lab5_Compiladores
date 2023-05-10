class Corazon:

    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
    
    def __str__(self):
        return f"{self.izquierda} -> {self.derecha}"

class Resto:

    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def __str__(self):
        return f"{self.izquierda} -> {self.derecha}"