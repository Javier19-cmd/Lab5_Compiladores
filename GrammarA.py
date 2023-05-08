from prettytable import PrettyTable

tabla = []

def aumentar_gramatica(gramatica): # Aumento de la gramática.
    nuevo_simbolo_inicial = gramatica[0][0] + "'"
    nueva_gramatica = [[nuevo_simbolo_inicial, gramatica[0][0]]]
    
    for produccion in gramatica:
        nueva_gramatica.append(produccion)
    
    return nueva_gramatica

def simbolos_gramaticales(lista_producciones): # Obteniendo los símbolos gramaticales.
    simbolos = set()
    for produccion in lista_producciones:
        simbolos.add(produccion[0])
        for simbolo in produccion[1].split():
            if simbolo.isupper():
                simbolos.add(simbolo)
            elif simbolo.islower() or simbolo.isnumeric() or simbolo in ['+', '*', '(', ')', '-', '/']:
                simbolos.add(simbolo)
    return sorted(list(simbolos))

def construir_gramatica_y_conjunto_I(lista_producciones): # Construyendo la gramática y el conjunto inicial.

    """
    
    Método que ayuda a construir la gramática y el conjunto I0.

    """

    #simbolo_inicial = lista_producciones[0][0] # Agarrando el símbolo inicial de la gramática.
    gramatica = [[produccion[0], produccion[1]] for produccion in lista_producciones] # Haciendo listas de listas para la gramática.

    I0 = [] # Este es el conjunto I0.
    
    for produccion in gramatica:
        if [produccion[0], produccion[1]] not in I0:

            #print([produccion[0], produccion[1]])

            I0.append([produccion[0], "." + produccion[1]])

    #gramatica = I0.copy()

    # Devolviendo la gramática aumentada y el estado I0.
    return gramatica, I0

def CERRADURA(I, gramatica): # Cálculo de la cerradura de un conjunto I dada una gramática.
    # print(gramatica)
    # print(I)

    cerradura = list(I) # Copiando el conjunto I.
    agregado = True


    while agregado:
        agregado = False

        for elemento in cerradura:
            #print(elemento)
            produccion = elemento[1]
            #print(produccion)
            punto_pos = produccion.index('.')
            #print(punto_pos)
            if punto_pos != len(produccion) - 1:
                # Encontrar el siguiente espacio en blanco después del punto.
                espacio_pos = produccion.find(' ', punto_pos)
                
                if espacio_pos == -1: # Agarrando palabras en caso de que haya.
                    espacio_pos = len(produccion)
                simbolo = produccion[punto_pos + 1:espacio_pos]
                # print(simbolo)
                # print(gramatica)


                # Revisar en cada lista de listas.
                for produccion in gramatica:
                    if produccion[0] == simbolo:
                        
                        #print(produccion[0])

                        nueva_produccion = [produccion[0], '.' + produccion[1]]

                        #print("Nueva producción: ", nueva_produccion)

                        if nueva_produccion not in cerradura:
                            cerradura.append(nueva_produccion)
                            agregado = True

    return cerradura


def ir_A(I, X, gramatica): # Función para generar transiciones.

    # print("I: ", I)
    # print(X)

    J = []
    for elemento in I:
        produccion = elemento[1]
        punto_pos = produccion.index('.')
        if punto_pos != len(produccion) - 1 and produccion[punto_pos + 1] == X:
            nuevo_elemento = (elemento[0], produccion[:punto_pos] + X + '.' + produccion[punto_pos+2:])

            #print("Nuevo elemento: ", nuevo_elemento)

            # Si el elemento ya está en el conjunto J, entonces seguir moviendo el punto a la derecha.
            if nuevo_elemento not in J:
                #print("Nuevo elemento: ", nuevo_elemento)
                J.append(nuevo_elemento)

                a = CERRADURA([nuevo_elemento], gramatica)
                
                if [I, X, a] not in tabla:

                    tabla.append([I, X, a])

            # Obtener la posición del punto en el elemento.
            punto_pos = nuevo_elemento[1].index('.')
            
            # Verificar si se puede mover el punto a la derecha.
            if punto_pos < len(nuevo_elemento[1])-1:
                
                #print("Punto pos: ", punto_pos)
                #print("Elemento: ", nuevo_elemento[1])

                # Moviendo el punto del nuevo_elemento[1]

                # Detectando el caracter después del punto.
                caracter_despues_punto = nuevo_elemento[1][punto_pos+2]

                #print(caracter_despues_punto)

                # Mantener el espacio antes del caracter.
                if caracter_despues_punto == ' ':
                    caracter_despues_punto = ''

                # Colocando el punto después de ese caracter.
                nuevo_elemento = (nuevo_elemento[0], nuevo_elemento[1][:punto_pos] + caracter_despues_punto + '.' + nuevo_elemento[1][punto_pos+3:])

                #print("Nuevo elemento: ", nuevo_elemento)

                # Revisar si se puede seguir moviendo el punto a la derecha.
                if nuevo_elemento not in J:
                                    

                    J.append(nuevo_elemento)

                    a = CERRADURA(J, gramatica)

                    #print("A: ", a, caracter_despues_punto)

                    if [nuevo_elemento, caracter_despues_punto, a] not in tabla:

                        #print(I)

                        # Guardando las transiciones en una lista.
                        tabla.append([nuevo_elemento, caracter_despues_punto, a])

                    #print(tabla)

                    #return CERRADURA(J, gramatica)


                    #J += ir_A([nuevo_elemento], X, gramatica)

                    # Obtener nuevamente la posición del punto.
                    punto_pos = nuevo_elemento[1].index('.')

                    #print("Punto pos: ", punto_pos)

                    # Haciendo verificaciones otra vez.
                    if punto_pos < len(nuevo_elemento[1])-1:

                        # Detectando el caracter después del punto.
                        caracter_despues_punto = nuevo_elemento[1][punto_pos+2]

                        #print("Caracter: ", caracter_despues_punto)

                        # Si no hay nada, entonces se hace break.
                        if caracter_despues_punto == ' ':
                            break

                        # Colocando el punto después de ese caracter.
                        nuevo_elemento = (nuevo_elemento[0], nuevo_elemento[1][:punto_pos] + caracter_despues_punto + '.' + nuevo_elemento[1][punto_pos+3:])

                        #print("Nuevo elemento: ", nuevo_elemento)

                        if nuevo_elemento not in J: 
                            J.append(nuevo_elemento)

                            a = CERRADURA(J, gramatica)

                            #if [nuevo_elemento, caracter_despues_punto, a] not in tabla:

                            tabla.append([nuevo_elemento, caracter_despues_punto, a])

                            #print("A: ", a, " caracter después del punto: ", caracter_despues_punto)

                            #print(tabla)

                            #return CERRADURA(J, gramatica)

    return CERRADURA(J, gramatica)


def construir_automata_LR0(grammar): # Construcción de la gramática.
    """
    Construye el autómata de análisis sintáctico LR(0) a partir de una gramática dada.

    Args:
        grammar (List[List[str]]): La gramática en forma de lista de producciones.

    Returns:
        Tuple[List[Set[Tuple[str, int]]], Dict[Tuple[int, str], Tuple[int, str, int, Set[str]]], Dict[Tuple[int, str], Tuple[str, int]]]: 
        Una tupla con la lista de conjuntos, el diccionario de transiciones y el diccionario de acciones.
    """
    # Aumentar la gramática
    grammara = aumentar_gramatica(grammar)

    # Obtener los símbolos gramaticales
    simbolos_gram = simbolos_gramaticales(grammara)

    # Construir la gramática y el conjunto I0
    gramatica, I0 = construir_gramatica_y_conjunto_I(grammara)

    # print("Gramática: ", gramatica)
    # print("Gramática aumentada: ", grammara)
    # print("I0: ", I0)

    # # Imprimiendo hacia abajo el I0.
    # for i in I0:
    #     print(i)

    # # Crear la lista de conjuntos LR(0), el diccionario de transiciones y el diccionario de acciones
    C = [CERRADURA(I0, gramatica)]
    transiciones = {}
    acciones = {}

    #print("C: ", C)
    #print(grammara)

    agregado = True
    
    while agregado:
        agregado = False

        for i in range(len(C)):
            I = C[i]

            for X in simbolos_gram:
                #print(X)

                goTo = ir_A(I, X, gramatica)

                #print("GoTo: ", goTo)


                # if goTo: 
                #     print("Resultado: ", goTo)

                if goTo and goTo not in C:
                    
                    #print("GoTo: ", goTo)

                    C.append(goTo)
                    agregado = True



    # # Imprimir hacia abajo la lista C.
    # for i in C:
    #     print(i)

    # Imprimiendo hacia abajo la tabla.
    # for i in tabla:
    #     print(i)

    lista_nueva = []
    for elemento in tabla:
        if elemento not in lista_nueva:
            lista_nueva.append(elemento)

    #print("Tabla en GrammarA: ", tabla)
    

    #return C, transiciones, acciones

    return tabla


# grammar = [
#     ["E", "E + T"],
#     ["E", "T"],
#     ["T", "T * F"],
#     ["T", "F"],
#     ["F", "( E )"],
#     ["F", "id"]
# ] # Gramática a utilizar.

# C, transiciones, acciones = construir_automata_LR0(grammar)
#print("Transiciones: ", transiciones)
#print("Acciones: ", acciones)
#print("C: ", C)

# for i in lista_nueva:
#     print(i)


# # Colocar las transiciones en una tabla.
# # Definir las columnas de la tabla
# table = PrettyTable()
# table.field_names = [" Símbolo ", " Conjunto de partida ", "Conjunto de llegada "]

# # # Agregando los resultados de la tabla a la table.
# # for i in tabla:
# #     table.add_row([tabla[1], tabla[0], tabla[2]])

# # for estado, simbolo in acciones:
# #     accion_transicion = acciones[(estado, simbolo)]
# #     table.add_row([simbolo, accion_transicion[0], accion_transicion[2], accion_transicion[3]])

# # Imprimir la tabla
# print(table)