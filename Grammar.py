from collections import defaultdict

class Grammar:
    def __init__(self, producciones, inicial):
        self.producciones = producciones
        self.inicial = inicial
        self.no_terminales = set()
        self.terminales = set()
        for produccion in producciones:
            self.no_terminales.add(produccion.izquierda)
            for simbolo in produccion.derecha:
                if simbolo not in self.no_terminales:
                    self.terminales.add(simbolo)

    def __str__(self):
        return '\n'.join([str(p) for p in self.producciones])

class Produccion:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
    
    def __str__(self):
        return f"{self.izquierda} -> {' '.join(self.derecha)}"
