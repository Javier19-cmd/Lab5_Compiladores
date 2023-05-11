from prettytable import PrettyTable
from Grammar import *
from EstadosLR import *
import copy

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

    # for eleme in J:
    #     print("Elementos in cerradura: ", eleme)

    estados = {}

    corazones = []

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
                    #print("Corazón a agregar: ", corazon)
                    
                    estados[corazon] = set() # Usamos un conjunto para evitar duplicados

                    #print(estados[corazon])

            dot_pos = prod.index('.')


            # Verificando si el punto no está a la izquierda, dado que eso será corazón también.
            if dot_pos > 0:

                # Obteniendo el símbolo que está a la izquierda del punto.
                #nsimbolo = prod[dot_pos-1]
                #print("nsimbolo: ", nsimbolo, " símbolo: ", simbolo)

                # if nsimbolo == simbolo:
                #     print("Símbolo: ", nsimbolo)

                # print(simbolo)
                # print(prod)
                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                #print("Otro corazón a agregar: ", corazon)

                #print("Corazón a agregar: ", corazon)
                
                # Verificando si ya hay corazones en el estado, en caso de que ya haya, entonces seguir agregando el corazón.
                #print("Estados: ", estados)

                estados[corazon] = set()

            # Si el punto no está a la izquierda, entonces es un resto.
            if dot_pos == 0:
                if simbolo != "E'" and prod != ".E":
                    resto = Resto(simbolo, prod)

                    #print("Producción: ", prod)


                    #print("Corazón: ", corazon)
                    # print("Resto: ", resto)

                    # corazon = Corazon(simbolo, prod)

                    # print("Corazón: ", corazon)

                    # # Revisar este if más adelante.
                    # if corazon not in estados:
                        
                    #     print("Corazón no en estados: ", corazon)

                    #     estados[corazon] = set()

                    #print("Corazón: ", corazon)

                    # Buscar todas las producciones que empiecen con el elemento que está a la derecha del punto.
                    for rule in grammar.productions:

                        for e in resto.izquierda:
                            #print("E: ", e, " rule: ", rule[1])

                            #print("e: ", e)

                            #print("Resto: ", resto)

                            if e == rule[1][0]:
                                #print("Agregado: ", e)
                                #print("Corazón: ", corazon)
                                estados[corazon].add(resto)

                                #added = True

            # if dot_pos < len(prod)-1:
            #     next_sym = prod[dot_pos+1]
            #     for rule in grammar.productions:
            #         if rule[0] == next_sym:
            #             new_item = (next_sym, '.' + rule[1])
            #             if new_item not in J:
            #                 J.append(new_item)
            #                 #print("New item: ", new_item)
            #                 added = True
    # Eliminando el último estado que se generó, porque se duplica.
    #del estados[corazon]

    #print(estados)

    # for s, v in estados.items(): 
    #     print("s: ",s)

    #     for a in v:
    #         print("a: ", a)
    
    # print("")

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

    # print("Conjunto: ", I)
    # print("Símbolo: ", X)
    # print("Gramatica: ", gramatica)

    for corazon, resto in I.items():
        
        #print("Corazón: ", corazon)
        # print("Resto: ", resto)
        # print("Corazón derecha: ", corazon.derecha)
        # print("Corazón izquierda: ", corazon.izquierda)
        
        #print(corazon.derecha)

        #print("Corazón: ", corazon)

        # Buscar el índice del punto.
        dot_pos = corazon.derecha.index('.')

        if dot_pos < len(corazon.derecha) - 1:

            # Obteniendo lo que estaba a la derecha de ese punto.
            next_sym = corazon.derecha[dot_pos+1]

            #print(next_sym)

            #print("Next sym: ", next_sym)

            # Revisar que elementos hay a la derecha del punto que sean iguales al símbolo que se está usando.
            if next_sym == X:
                
                #print("next_sym: ", next_sym)

                # Moviendo el punto a la derecha del símbolo.
                corazon.derecha = corazon.derecha[:dot_pos] + next_sym + '.' + corazon.derecha[dot_pos+2:]

                #print("Corazón: ", corazon)
                
                #print("Agregado: ", corazon)

                if corazon not in J:
                    # Cambiando el tipo del corazón a lista.
                    corazon = list(corazon)
                    J.append(corazon)

            for res in resto:

                # Buscar el índice del punto.
                dot_pos = res.derecha.index('.')

                if dot_pos < len(res.derecha) - 1:
                    # Crear una lista de producciones que tengan el símbolo X en el lado izquierdo.
                    X_productions = [p for p in resto if p.izquierda == X]

                    # for s in X_productions:
                    #     print(s)

                    for p in X_productions:
                        if p.derecha[dot_pos] == '.' and p.derecha[dot_pos+1] == X:

                            #print(p.derecha[dot_pos], p.derecha[dot_pos+1])

                            # Guardando la parte izquierda de la producción.
                            #print(type(p))
                            iz = p.izquierda

                            # Mover el punto a la derecha del símbolo X en el lado derecho de la producción.
                            new_lado_derecho = p.derecha[:dot_pos] + X + '.' + p.derecha[dot_pos+2:]

                            #print(iz, new_lado_derecho)
                            
                            #res.derecha = new_lado_derecho

                            # Imprimiendo el símbolo de la producción original de donde se sacó la producción.
                            
                            # print("Izquierda de la producción: ", iz)
                            # print(res)


                            # print("Res izquierda: ", res.izquierda)
                            # print("Res: derecha ", new_lado_derecho)

                            # Guardando la nueva producción.
                            if p.izquierda == iz: 

                                #print("X en la creación de la nueva producción: ", X)
                                p.derecha = new_lado_derecho
                                #print("Nueva prod: ", p)

                                #print(type(p))

                                # Cambiar el tipo de p a lista.
                                p = list(p)

                                if p not in J:
                                    # print(res)
                                    J.append(p)
                                    #print(res[0])

                                # print("J: ", J)
                                # for s in J:
                                #     print("S: ", s)

                                # a = CERRADURA(J, gramatica)

                                # print("a: ", a)

                                return CERRADURA(J, gramatica)

                    
                    # Obteniendo lo que estaba a la derecha de ese punto.

    # print("J: ", J)

    # return CERRADURA(J, gramatica)

    #return CERRADURA(J, gramatica)



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


    agregado = True

    while agregado:

        agregado = False

        for conjunto in C:


            conjunto_copia = copy.deepcopy(conjunto)

            for X in simbolos_gram:
                #print("Símbolo: ", X, " conjunto: ", conjunto)

                goto = ir_A(conjunto_copia, X, gramatica)
                
                # if goto:

                #     print(goto)

                #     for s, v in goto.items():
                #         print("s de goto: ", s)

                #         for h in v:
                #             print("h de goto: ", h)
                    
                #     exit(1)

                if goto and goto not in C:

                    print(type(goto))
                    

                    # for s, v in goto.items():
                    #     print("s antes: ", s)

                    #     for w in v:
                    #         print("w antes: ", w)

                    # for elem in C:
                    #     for s, v in elem.items():
                    #         print("s antes: ", s)

                    #         for h in v:
                    #             print("h antes: ", h)
                

                    C.append(goto)

                    # for j in C:
                    #     for s, v in j.items():
                    #         print("s: ", s)

                    #         for h in v:
                    #             print("h: ", h)


                    agregado = True
    
    for el in C:
        for s, v in el.items():
            print("s: ", s)

            for h in v:
                print("h: ", h)
    
    #print("")

    # lista_nueva = []
    # for elemento in tabla:
    #     if elemento not in lista_nueva:
    #         lista_nueva.append(elemento)

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
