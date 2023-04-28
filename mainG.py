from Grammar import *
from GramarF import primero, siguiente

producciones = [    
    Produccion('E', ['T', "E'"]),
    Produccion("E'", ['+', 'T', "E'"]),
    Produccion("E'", ['']),
    Produccion('T', ['F', "T'"]),
    Produccion("T'", ['*', 'F', "T'"]),
    Produccion("T'", ['']),
    Produccion('F', ['(', 'E', ')']),
    Produccion('F', ['id'])
]

gramatica = Grammar(producciones, 'E')

# Obtenemos los conjuntos primero
primeros = primero(gramatica)
print("Conjuntos primero:")
for no_terminal, conjunto in primeros.items():
    print(f"{no_terminal}: {{{', '.join(conjunto)}}}")

# Obtenemos los conjuntos siguiente
# Obtenemos los conjuntos siguiente
siguientes = siguiente(gramatica, primeros)
print("Conjuntos siguiente:")
for no_terminal, conjunto in siguientes.items():
    conjunto_str = ", ".join([p.__str__() if isinstance(p, Produccion) else p for p in conjunto])
    print(f"{no_terminal}: {{{conjunto_str}}}")

