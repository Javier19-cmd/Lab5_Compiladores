def aumentar_gramatica(gramatica):
    nuevo_simbolo_inicial = gramatica[0][0] + "'"
    nueva_gramatica = [[nuevo_simbolo_inicial, gramatica[0][0]]]
    
    for produccion in gramatica:
        nueva_gramatica.append(produccion)
    
    return nueva_gramatica

def simbolos_gramaticales(lista_producciones):
    simbolos = set()
    for produccion in lista_producciones:
        simbolos.add(produccion[0])
        for simbolo in produccion[1].split():
            if simbolo.isupper():
                simbolos.add(simbolo)
            elif simbolo.islower() or simbolo.isnumeric() or simbolo in ['+', '*', '(', ')']:
                simbolos.add(simbolo)
    return sorted(list(simbolos))

def construir_gramatica_y_conjunto_I(lista_producciones):
    simbolo_inicial = lista_producciones[0][0]
    gramatica = [[produccion[0], produccion[1]] for produccion in lista_producciones]
    I = {simbolo_inicial + " -> ." + simbolo_inicial}
    
    for produccion in gramatica:
        if produccion[0] == simbolo_inicial and simbolo_inicial + " -> ." + simbolo_inicial not in I:
            I.add(simbolo_inicial + " -> " + simbolo_inicial + ".")
        if produccion[0] + " -> ." + produccion[1] not in I:
            I.add(produccion[0] + " -> ." + produccion[1])
    
    return gramatica, I


def CERRADURA(I, gramatica):
    J = set(tuple(prod) for prod in I)
    agregados = True

    while agregados:
        agregados = False
        nuevos = []

        for produccion in J:
            if produccion[1] == "":
                continue

            siguiente_simbolo = produccion[1][0]
            if siguiente_simbolo.isupper():
                for nueva_produccion in gramatica:
                    if nueva_produccion[0] == siguiente_simbolo and tuple(nueva_produccion) not in J and tuple(nueva_produccion) not in nuevos:
                        nuevos.append(tuple(nueva_produccion))
                        agregados = True

        J.update(nuevos)

    # Convertir las producciones de J en strings y devolver un conjunto de strings
    return set([''.join(prod) for prod in J])


def irA(I, X, gramatica):

    # print("I: ", I)
    # print("X: ", X)
    # print("Gramática: ", gramatica)

    J = set()
    for produccion in I:
        if len(produccion[0]) == 0 or produccion[0][0] != X:
            continue
        nueva_produccion = (produccion[0], produccion[0][1:] + ".")

        #print("Nueva producción: ", nueva_produccion)
        
        J |= CERRADURA({nueva_produccion}, gramatica)

        #print("J: ", J)

    return J

#print(I)

# J = CERRADURA(I, gram)

# print(J)

#print("Gramática: ", gram)

def elementos(G):
    
    gra, Is = construir_gramatica_y_conjunto_I(G)

    # Obtener la producción que tenga el '.
    # print("Gramática: ", gra, "Conjunto I: ",  Is)

    # Quitar las producciones que sean de tipo "E' -> E'." y "E' -> .E'" del Is.
    Is = {produccion for produccion in Is if produccion[0] != produccion[1]}

    #print(Is)

    C = CERRADURA(Is, gra)
    
    simbolos_gramaticaless = simbolos_gramaticales(G)

    #print("Simbolos: ", simbolos_gramaticaless)
    
    #print("C: ", C)

    done = False
    while not done:
        done = True
        new_sets = set()  # create a new set to store the new items
        for I in C:
            for X in simbolos_gramaticaless:

                # print("I: ", I)
                # print("Símbolos: ", simbolos_gramaticaless)
                # print("X: ", X)

                ira = irA(I, X, G)
                #print("IrA", ira)

                if ira and ira not in C:

                    #print("ira: ", ira)

                    new_sets.add(frozenset(ira))  # add the new items to the new set

                    #print("New set: ", new_sets)

                    done = False
        C.update(new_sets)  # add the new items to C

        #print("C: ", C)

    return C

grammar = [
    ["E", "E + T"],
    ["E", "T"],
    ["T", "T * F"],
    ["T", "F"],
    ["F", "( E )"],
    ["F", "id"]
]

def construir_automata_LR0(grammar):
    """
    Construye el autómata de análisis sintáctico LR(0) a partir de una gramática dada.

    Args:
        grammar (List[List[str]]): La gramática en forma de lista de producciones.

    Returns:
        Tuple[Dict[Tuple[int, str], Tuple[str, int]], Dict[int, Dict[str, Tuple[str, int]]]]: Una tupla con el diccionario de transiciones y el diccionario de acciones.
    """
    # Aumentar la gramática
    grammar = aumentar_gramatica(grammar)

    # Obtener los símbolos gramaticales
    simbolos_gram = simbolos_gramaticales(grammar)

    # Construir la gramática y el conjunto I0
    gramatica, I0 = construir_gramatica_y_conjunto_I(grammar)

    # Crear la lista de conjuntos LR(0) y el diccionario de transiciones
    C = [CERRADURA(I0, gramatica)]
    transiciones = {}

    # Crear el diccionario de acciones
    acciones = {}

    FIN_CADENA = "FIN"
    SHIFT = "SHIFT"
    ACEPTAR = "ACEPTAR"
    REDUCE = "REDUCE"

    # Recorrer la lista de conjuntos LR(0)
    for i, conjunto in enumerate(C):
        # Recorrer los símbolos gramaticales y el símbolo de fin de cadena
        for simbolo in simbolos_gram + [FIN_CADENA]:
            # Calcular el conjunto siguiente
            ir_a = irA(conjunto, simbolo, gramatica)

            # Si el conjunto siguiente es vacío, pasar al siguiente símbolo
            if not ir_a:
                continue

            # Si el conjunto siguiente no está en la lista de conjuntos, agregarlo
            if ir_a not in C:
                C.append(ir_a)

            # Agregar la transición correspondiente
            j = C.index(ir_a)
            transiciones[(i, simbolo)] = (SHIFT, j)

        # Recorrer las producciones en el conjunto actual
        for produccion in conjunto:
            # Si la producción está completa, agregar la acción correspondiente
            if produccion[-1] == ".":
                # Si es la producción S' -> S., agregar la acción de aceptar
                if produccion == f"{gramatica[0][0]}' -> {gramatica[0][0]}.":
                    acciones[(i, FIN_CADENA)] = (ACEPTAR,)
                # Si no, agregar la acción de reducir
                else:
                    for simbolo in simbolos_gram + [FIN_CADENA]:
                        acciones[(i, simbolo)] = (REDUCE, produccion)

    return transiciones, acciones


transiciones, acciones = construir_automata_LR0(grammar)
print("Transiciones: ", transiciones)
print("Acciones: ", acciones)