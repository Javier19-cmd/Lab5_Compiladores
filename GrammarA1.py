from prettytable import PrettyTable
from Grammar import *
from EstadosLR import *

tabla = []


def aumentar_gramatica(gramatica): # Aumento de la gramática.
    nuevo_simbolo_inicial = grammar.productions[0][0] + "'"
    nueva_gramatica = [[nuevo_simbolo_inicial, grammar.productions[0][0]]]
    
    for produccion in gramatica.productions:
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

def construir_gramatica_y_conjunto_I(lista_producciones):
    # Obtener todos los no terminales de la gramática
    no_terminales = set([produccion[0] for produccion in lista_producciones])
    for produccion in lista_producciones:
        for simbolo in produccion[1]:
            if simbolo.isupper():
                no_terminales.add(simbolo)

    # Agregar producciones vacías para no terminales sin producción
    for no_terminal in no_terminales:
        if no_terminal not in [produccion[0] for produccion in lista_producciones]:
            lista_producciones.append([no_terminal, ''])

    # Construir gramática y conjunto I0
    gramatica = [[produccion[0], produccion[1]] for produccion in lista_producciones]
    I0 = []
    for produccion in gramatica:
        I0.append([produccion[0], "." + produccion[1]])

    return gramatica, I0


def CERRADURA(I, grammar):
    J = I.copy()

    estados = {}

    added = True
    while added:
        added = False
        for item in J:
            simbolo = item[0] # Símbolo
            prod = item[1] # Producción

            # Si el símbolo es E' y la producción es E, entonces es un corazón.
            if simbolo == "E'": 
                if prod == ".E":
                    corazon = Corazon(simbolo, prod)
                    estados[corazon] = set() # Usamos un conjunto para evitar duplicados

            dot_pos = prod.index('.')

            # Verificando si el corazón no está a la izquierda, dado que eso será corazón también.
            if dot_pos > 0:
                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos+1:])
                estados[corazon] = set()

            # Si el punto no está a la izquierda, entonces es un resto.
            if dot_pos == 0:
                if simbolo != "E'" and prod != ".E":
                    resto = Resto(simbolo, prod)


                    # print("Corazón: ", corazon)
                    # print("Resto: ", resto)

                    # corazon = Corazon(simbolo, prod)

                    # print("Corazón: ", corazon)

                    if corazon not in estados:
                        estados[corazon] = set()
                    estados[corazon].add(resto)

            if dot_pos < len(prod)-1:
                next_sym = prod[dot_pos+1]
                for rule in grammar.productions:
                    if rule[0] == next_sym:
                        new_item = (next_sym, '.' + rule[1])
                        if new_item not in J:
                            J.append(new_item)
                            added = True


    # Eliminando el último estado que se generó, porque se duplica.
    del estados[corazon]

    return estados



def ir_A(I, X, gramatica):
    """
    I: Conjunto de producciones
    X: Símbolo de gramática
    gramatica: Gramática
    
    Retorna el conjunto de producciones que resulta de avanzar el punto de
    todas las producciones en I que tienen a X después del punto.
    """
    J = []
    for elemento in I:
        produccion = elemento[1]
        punto_pos = produccion.index('.')
        if punto_pos != len(produccion) - 1 and produccion[punto_pos + 1] == X:

            #print("Hola")

            nueva_produccion = (elemento[0], produccion[:punto_pos] + X + '.' + produccion[punto_pos + 2:])

            #print(nueva_produccion)

            J.append(nueva_produccion)


            # Guardando en la tabla la transición.
            tabla.append([I, X, J])


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

    gramatica = Grammar(gramatica)

    # print(type(gramatica))

    #print("Grammar: ", gramatica)

    #print(I0)

    # print("Gramática: ", gramatica)
    # print("Gramática aumentada: ", grammara)
    # print("I0: ", I0)

    # # Imprimiendo hacia abajo el I0.
    # for i in I0:
    #     print(i)

    # # Crear la lista de conjuntos LR(0), el diccionario de transiciones y el diccionario de acciones
    C = [CERRADURA(I0, gramatica)]

    a = C.pop()

    #print(a)

    for corazon, restos in a.items():
        
        print()
        print("Corazón: ",corazon)

        print()
        
        for resto in restos: 
            print("Resto: ", resto)
    

    # for corazon, restos in a.items():
    #     print(corazon)
    #     for resto in restos:
    #         print(resto)

    #print("Quiebre")


    #print("C: ", C)
    #print(grammara)

    #print("Símbolos de la gramática: ", simbolos_gram)

    # agregado = True
    
    # while agregado:
    #     agregado = False

    #     for i in range(len(C)):
    #         I = C[i]

    #         for X in simbolos_gram:
    #             #print(X)

    #             goTo = ir_A(I, X, gramatica)

    #             #print("GoTo: ", goTo)


    #             # if goTo: 
    #             #     print("Resultado: ", goTo)

    #             if goTo and goTo not in C:
                    
    #                 #print("GoTo: ", goTo)

    #                 C.append(goTo)

    #                 #print("Hola")

    #                 agregado = True

    #print("C: ", C)

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

    # for s in tabla:
    #     print("S: ", s)

    # # Imprimiendo hacia abajo la tabla.
    # for i in lista_nueva:
    #     print(i)
    

    #return C, transiciones, acciones

    return tabla


grammar = Grammar([
    ["E", "E + T"],
    ["E", "T"],
    ["T", "T * F"],
    ["T", "F"],
    ["F", "( E )"],
    ["F", "id"]
]) # Gramática a utilizar.

tabla = construir_automata_LR0(grammar)
