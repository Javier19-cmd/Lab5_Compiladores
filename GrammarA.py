def aumentar_gramatica(gramatica):
    nuevo_simbolo_inicial = gramatica[0][0] + "'"
    nueva_gramatica = [[nuevo_simbolo_inicial, gramatica[0][0]]]
    
    for produccion in gramatica:
        nueva_gramatica.append(produccion)
    
    return nueva_gramatica


def construir_gramatica_y_conjunto_I(lista_producciones):
    simbolo_inicial = lista_producciones[0][0]
    gramatica = [[produccion[0], produccion[1]] for produccion in lista_producciones]
    I = {simbolo_inicial + "' -> ." + simbolo_inicial}
    
    for produccion in gramatica:
        if produccion[0] == simbolo_inicial:
            I.add(simbolo_inicial + "' -> " + simbolo_inicial + ".")
        I.add(produccion[0] + " -> ." + produccion[1])
    
    return gramatica, list(I)


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


grammar = [
    ["E", "E + T"],
    ["E", "T"],
    ["T", "T * F"],
    ["T", "F"],
    ["F", "( E )"],
    ["F", "id"]
]

gr = aumentar_gramatica(grammar)

print(gr)

gram, I = construir_gramatica_y_conjunto_I(gr)

#print(I)

J = CERRADURA(I, gram)

print(J)

# # Imprimirla hacia abajo.
# for produccion in gr:
#     print(produccion[0] + " -> " + produccion[1])
