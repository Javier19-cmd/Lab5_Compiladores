from prettytable import PrettyTable
from Grammar import *
from EstadosLR import *
import copy
import pydot

tabla = []


def aumentar_gramatica(gramatica): # Aumento de la gramática.
    nuevo_simbolo_inicial = gramatica.productions[0][0] + "'"
    nueva_gramatica = [[nuevo_simbolo_inicial, gramatica.productions[0][0]]]

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


    # for elemet in J:
    #     print("Elementos en I: ", elemet)
    # print("")

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
                    #print("Corazón a agregar en Cerradura: ", corazon)
                    
                    estados[corazon] = set() # Usamos un conjunto para evitar duplicados.

                    #print(estados[corazon])

            dot_pos = prod.index('.')

            #print("dot_pos: ", dot_pos)


            # Verificando si el punto no está a la izquierda, dado que eso será corazón también.
            if dot_pos > 0:

                # Imprimiendo el corazón a agregar.
                #print("item: ", item, " prod: ", prod, " posición del punto: ", dot_pos)

                #derecha_punto = dot_pos + 1

                # Viendo que hay a la derecha del punto.

                dot_po = item[1].index(".")

                if dot_po + 1 < len(item[1]):
                    # print("Derecha del punto: ", item[1][dot_pos + 2])

                    # print("Gramática: ", grammar)

                    # Buscando en la derecha de la regla todo lo que empiece con item[1][dot_pos + 2].
                    for rule in grammar.productions:

                        if rule[1][0] == "i":
                           # print("Regla del id: ", rule[1][0:])

                            if item[1][dot_pos + 2] == rule[1][0:]:
                                #print("Regla del id: ", rule[1][0:])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                #print("Nuevo corazón: ", corazon)

                                estados[corazon] = set()

                            else: 
                               # print("No hay transición", item[1][dot_pos + 2])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                estados[corazon] = set()
                        
                        else:
                            #print("Regla: ", rule[1][0])

                            if item[1][dot_pos + 2] == rule[1][0]:
                                #print("Regla: ", rule[1][0])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                estados[corazon] = set()

                                #print("Corazón en el else de id: ", corazon)
                            
                            else:
                                #print("No hay transición", item[1][dot_pos + 2])
                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])
                                estados[corazon] = set()

                # else:
                #     print("No hay nada a la derecha del punto.")

                # Imprimiendo el elemento que está a la izquierda del punto.
                #print("Símbolo en dot_pos > 0: ", prod[dot_pos - 1])

                if prod[dot_pos - 1] == "d":
                    
                    # Imprimiendo el elemento sin el punto.
                    #print("Símbolo en dot_pos > 0: ", prod[:dot_pos])

                    # Buscando en la derecha de la regla todo lo que empiece con prod[:dot_pos].
                    for rule in grammar.productions:
                        if rule[1][0] == "i":
                            #print("Regla del id: ", rule[1][0:])
                            
                            if prod[:dot_pos] == rule[1][0:]: # Creando corazones.

                                #print("prod: ", prod[:dot_pos], " rule: ", rule[1][0:])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                #print("Nuevo corazón: ", corazon)

                                estados[corazon] = set()
                        
                        else: 
                            #print("Regla: ", rule[1][0])

                            if prod[:dot_pos] == rule[1][0]: # Creando corazones.

                                #print("prod: ", prod[:dot_pos], " rule: ", rule[1][0])
                                
                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                estados[corazon] = set()

                                #print("Corazón en el else de id: ", corazon)

                else: 
                    #print("Símbolo en dot_pos > 0: ", prod[dot_pos - 1])
                    
                    for rule in grammar.productions:
                        
                       # print("Regla: ", rule[1][0])

                        #print("producción: ", prod[:dot_pos]," regla: ",  rule[1][0])

                        if prod[:dot_pos] == rule[1][0]: # Creando corazones.
                            corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                            #print("Nuevo corazón: ", corazon)

                            estados[corazon] = set()

            # Si el punto está a la izquierda, entonces es un resto.
            if dot_pos == 0:
                if simbolo != "E'" and prod != ".E":
                    resto = Resto(simbolo, prod)
                    # Buscar todas las producciones que empiecen con el elemento que está a la derecha del punto.
                    for rule in grammar.productions:

                        if resto.derecha[1] == "i":
                            # Agarrando el id.
                            #print("id: ", resto.derecha[1:])
                            
                            #print("Resto: ", resto, " posición 1 en resto ", resto.derecha[1:], "Rule en la posición 0 ", rule[0])

                            if rule[1] == resto.derecha[1:]:
                                # print("rule[0]: ", rule[1])
                                # print("Agregando: ", rule[1], "resto ",resto.derecha[1:])
                                #print("Agregando: ", resto.derecha[1:])

                                estados[corazon].add(resto)

                                #added = True
                        
                        else: 
                        
                            #print("Resto: ", resto, " posición 1 en resto ", resto.derecha[1], "Rule en la posición 0 ", rule[1][0])

                            #print("Rule: ", rule[1][0])

                            if rule[1][0] == "i":
                                #print("id dentro del else: ",rule[1][0:])

                                #print("Agregando el id: ", rule[1][0:])

                                if rule[1][0:] == resto.derecha[1]:
                                    #print("rule[]")
                                    #print("Agregando: ", rule[1][0:], "resto ", resto.derecha[1])
                                    #print()

                                    estados[corazon].add(resto)

                                    #added = True

                            if rule[1][0] == resto.derecha[1]:
                            
                                # print("Agregando: ", rule[0], " resto ",resto)
                                #print("Agregando: ", resto)

                                estados[corazon].add(resto)

                                #added = True

    # # Imprimiendo los estados.
    # for corazon, resto in estados.items():
    #     print("Corazón en CERRADURA: ", corazon)
    #print("")

    #print("Estados: ", estados, " J: ", J)

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

    #print("Gramática: ", gramatica)
    
    # print("Conjunto: ", I, " símbolo: ", X)

    lista_temp = []

    for corazon, resto in I.items():
        
        #print("Corazón: ", corazon)
        # print("Resto: ", resto)
        # print("Corazón derecha: ", corazon.derecha)
        # print("Corazón izquierda: ", corazon.izquierda)
        
        #print(corazon.derecha)

        #print("Corazón: ", corazon)

        # Esto solo es el corazón del estado.

        # Buscar el índice del punto.
        dot_pos = corazon.derecha.index('.')

        #print("Posición del punto: ", dot_pos, "corazón: ", corazon, " símbolo: ", X)

        # Revisando que hay a la derecha del punto para ver lo si hay movimiento.
        if dot_pos < len(corazon.derecha) - 1:
            
            """

                Verificar si hay espacio vacío y si lo hay revisar los símbolos después de ese.

            """

            #print("corazon.derecha: ", corazon.derecha[dot_pos + 1])

            # # Si hay un espacio vacío, revisar si hay elementos después del espacio vacío.
            if corazon.derecha[dot_pos + 1] == ' ':
                
                #print("corazon.derecha después del espacio: ", corazon.derecha[dot_pos + 2], " X: ", X, " conjunto: ", I)

                # Verificando si el X es igual al corazon.derecha[dot_pos + 2].

                if corazon.derecha[dot_pos + 2] == X:

                    #print("corazon.derecha: ", corazon.derecha[dot_pos + 2], " X: ", X)

                    # Moviendo el punto a la derecha del símbolo.
                    corazon.derecha = corazon.derecha[:dot_pos] + " " + corazon.derecha[dot_pos + 2] + '.' + "" + corazon.derecha[dot_pos + 3:]

                    #print("Nuevo corazón cuando habían dos espacios: ", corazon)

                    cora = [corazon.izquierda, corazon.derecha]

                    #print("Nuevo corazón cuando habían dos espacios: ", cora)

                    if cora not in J:
                        J.append(cora)
                    
                    for rule in gramatica.productions: 
                        inicio = rule[1][0]

                        if inicio == "i": # Detectando el id.
                            inicio = rule[1][0:]
                        
                        if inicio == X:
                            # Falta detectar el id.

                            # Obteniendo el índice del punto.
                            dot_pos = rule[1].index(X)

                            #print("Posición de X: ", X)

                            derecha = rule[1][:dot_pos] + rule[1][dot_pos] + '.' + rule[1][dot_pos + 1:]

                            #print("Nuevo corazón lado derecho: ", rule)

                            # Convirtiendo el rule en corazón.
                            corazon = Corazon(rule[0], derecha)

                            cora = [rule[0], derecha]

                            #print("Cora: ", cora)

                            #print("Corazón: ", corazon)

                            if cora not in J: # Guardando el corazón.
                                J.append(cora)


            else: 

                # Verificando el símbolo de la derecha del punto. (aún falta detectar el caso de id)
                if corazon.derecha[dot_pos + 1] == X:
                    #print("Sí hay corrimiento. ", corazon.derecha[dot_pos + 1], X)
                    
                    # Mover el punto a la derecha del símbolo.
                    corazon.derecha = corazon.derecha[:dot_pos] + " " + corazon.derecha[dot_pos + 1] + '.' + corazon.derecha[dot_pos + 2:]

                    #print("Corazón antes del for: ", corazon)

                    cora = [corazon.izquierda, corazon.derecha]

                    #print("Nuevo corazón: ", cora)

                    if cora not in J: # Guardando el corazón.
                        J.append(cora)

                    # Buscar en la gramática las partes derechas de las producciones.
                    for rule in gramatica.productions:
                            # Aún falta detectar el caso de id.
                            #print("Regla: ", rule[1])

                            inicio = rule[1][0] # Agarrando el inicio de la regla.

                            # Si el inicio es igual a i, entonces se jala la palabra completa.
                            if inicio == "i":
                                inicio = rule[1][0:]
                            
                            #print("Inicio: ", inicio)

                            if inicio == X: # Si el inicio es igual a X, entonces eso será un corazón.
                                #print("Posible corazón: ", rule, " X: ", X, " inicio: ", inicio)

                                # Falta detectar el id.

                                # Obteniendo el índice del punto.
                                dot_pos = rule[1].index(X)

                                #print("Posición de X: ", X)

                                derecha = rule[1][:dot_pos] + rule[1][dot_pos] + '.' + rule[1][dot_pos + 1:]

                                #print("Nuevo corazón lado derecho: ", rule)

                                # Convirtiendo el rule en corazón.
                                corazon = Corazon(rule[0], derecha)

                                cora = [rule[0], derecha]

                                #print("Cora: ", cora)

                                #print("Corazón: ", corazon)

                                if cora not in J: # Guardando el corazón.
                                    J.append(cora)

                                # # Poniendo el punto a la derecha del símbolo y luego imprimiendo la regla.
                                # rule[1] = rule[1][:dot_pos] + rule[1][dot_pos + 1] + '.' + rule[1][dot_pos + 2:]

                                # print("Regla después de mover el punto: ", rule)


                #print("Corazón después de mover el punto: ", corazon)
        
        # Leyendo el punto del resto.
        if resto: 
            #print("Resto: ", resto)

            for elem in resto:

                #print("Elemento: ", elem, " símbolo: ", X)

                # Buscar el índice del punto.
                dot_poss = elem.derecha.index('.')

                #print("Posición del punto: ", dot_poss, " elemento: ", elem, " símbolo: ", X)

                # Revisando que hay a la derecha del punto para ver lo si hay movimiento.
                if dot_poss < len(elem.derecha) - 1:

                    # Verificando el símbolo de la derecha del punto. (aún falta detectar el caso de id)
                    if elem.derecha[dot_poss + 1] == X:
                        #print("Sí hay corrimiento. ", elem.derecha[dot_poss + 1], X)
                        
                        # Mover el punto a la derecha del símbolo.
                        elem.derecha = elem.derecha[:dot_poss] + elem.derecha[dot_poss + 1] + '.' + elem.derecha[dot_poss + 2:]

                        #print("Corazón antes del for: ", corazon)

                        cora = [elem.izquierda, elem.derecha]

                        #print("Corazón: ", cora)

                        if cora not in J:
                            J.append(cora)
                        
                        #print("J: ", J)
                
                    if elem.derecha[dot_poss + 1] == "i":
                        # Aquí se detecta el id.
                        #print("Sí hay id. ", elem.derecha[dot_poss + 1:], X)

                        # Verificando si el símbolo es el mismo que X.
                        if elem.derecha[dot_poss + 1:] == X:

                            elem.derecha = elem.derecha[:dot_poss] + elem.derecha[dot_poss + 1:] + '.' + elem.derecha[dot_poss + 3:]

                            #print("Corazón antes del for: ", corazon)

                            cora = [elem.izquierda, elem.derecha]

                            #print("Corazón: ", cora)

                            if cora not in J:
                                J.append(cora)
        

    # Eliminando repeticiones de J.
    J = list(set(tuple(x) for x in J))
    
    # Convirtiendo las tuplas de J en listas.
    J = [list(x) for x in J]

    #print("J: ", J)

    # if J:
    #     print("J: ", J)

    #a = CERRADURA(J, gramatica)

    #CERRADURA(J, gramatica)

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

    # Crear la lista de conjuntos LR(0), el diccionario de transiciones y el diccionario de acciones
    C = [CERRADURA(I0, gramatica)]


    agregado = True

    while agregado:

        agregado = False

        for conjunto in C:

            for X in simbolos_gram:
                
                #conjunto_copia = copy.deepcopy(conjunto)

                #goto = ir_A(conjunto_copia, X, gramatica)

                #print("Conjunto: ", conjunto)

                # print("Conjunto: ", conjunto)
                # for cora, res in conjunto.items():
                #     print("Corazón: ", cora)

                goto = ir_A(conjunto, X, gramatica)


                if goto and goto not in C:
                    #print("Goto: ", goto)
                    # for corazon, resto in goto.items():
                    #     print("Corazón: ", corazon)

                    #     for r in resto:
                    #         print("Resto: ", r)
                    
                    # print("")

                    print("Conjunto: ", conjunto, " X: ", X, " resultado ", goto)

                    tabla.append([conjunto, X, goto])

                    C.append(goto)

                    agregado = True
    
    # for estado in C:
    #     #pass
    #     print("Estado: ", estado)

    #     for corazon, resto in estado.items():
    #         print("Corazón: ", corazon)

    #         for r in resto:
    #             print("Resto: ", r)
    
    # print("Estados: ", len(C))

    # for estadi in C:
    #     print(estadi)

    return tabla


# grammar = Grammar([
#     ["E", "E + T"],
#     ["E", "T"],
#     ["T", "T * F"],
#     ["T", "F"],
#     ["F", "( E )"],
#     ["F", "id"]
# ]) # Gramática a utilizar.

# tabla = construir_automata_LR0(grammar)


# print(tabla)

# graph = pydot.Dot(graph_type='digraph')

# # Creando los nodos.
# nodes = set()
# for lista in tabla:
#     #print(lista)

#         #print(tupla[0])

#     # Convertir cada lista en la posición 0 de la lista a tupla si en caso no lo es.
#     if type(lista[0]) == tuple:
#         #nodes.add(lista[0])
#         pass
#     elif type(lista[0]) == list:
#         tupla_general0 = tuple(tuple(lista) for lista in lista[0])

#         #print(tupla_general0)
#         nodes.add(tupla_general0)
    
#     # Convertir cada lista en la posición 2 de la lista a tupla si en caso no lo es.
#     if type(lista[2]) == tuple:
#         pass
#     elif type(lista[2]) == list:
#         tupla_general2 = tuple(tuple(lista) for lista in lista[2])

#         #print(tupla_general2)
#         nodes.add(tupla_general2)

# # Agregando los nodos a la estructura de datos.
# for node in nodes:

#     #print("Nodo: ", node)

#     graph.add_node(pydot.Node(str(node)))

# # Haciendo las conexiones.
# for lista in tabla:
    
#     tupla0 = lista[0]
#     tupla2 = lista[2]
#     etiqueta = lista[1]

#     # print("Tupla0: ", tupla0)
#     # print("Tupla2: ", tupla2)
#     # print("Etiqueta: ", etiqueta)
    

#     # Conversión de la lista[0] en caso de que sea necesario.
#     if type(lista[0]) == tuple:
#         tupla0 = lista[0]
#     elif type(lista[0]) == list:
#         tupla0 = tuple(tuple(lista) for lista in lista[0])

#     # Conversión de la lista[2] en caso de que sea necesario.
#     if type(lista[2]) == tuple:
#         tupla2 = lista[2]
#     elif type(lista[2]) == list:
#         tupla2 = tuple(tuple(lista) for lista in lista[2])
    
#     graph.add_edge(pydot.Edge(str(tupla0), str(tupla2), label=str(etiqueta)))

#     # Poniendo el grafo de manera vertical.
#     #graph.set_rankdir("LR")
    
#     graph.write_png('GramáticaA1.png')