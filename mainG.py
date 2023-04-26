from Grammar import *
from GramarF import primero, siguiente

producciones = [    
    Produccion('S', ['a', 'S', 'b']),
    Produccion('S', ['a', 'b'])
]

gramatica = Grammar(producciones, 'S')

# Obtenemos los conjuntos primero
primeros = primero(gramatica)
print("Conjuntos primero:")
for no_terminal, conjunto in primeros.items():
    print(f"{no_terminal}: {conjunto}")

# Obtenemos los conjuntos siguiente
siguientes = siguiente(gramatica, primeros)
print("Conjuntos siguiente:")
for no_terminal, conjunto in siguientes.items():
    print(f"{no_terminal}: {conjunto}")