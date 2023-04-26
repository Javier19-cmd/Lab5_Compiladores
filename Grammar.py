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

class Produccion:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha