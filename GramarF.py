def primero(gramatica):
    primeros = {}
    # Inicializar los conjuntos primeros para cada símbolo
    for simbolo in gramatica.no_terminales | gramatica.terminales:
        primeros[simbolo] = set()
        if simbolo in gramatica.terminales:
            primeros[simbolo].add(simbolo)
    # Iterar hasta que no haya cambios en los conjuntos primeros
    while True:
        cambios = False
        for produccion in gramatica.producciones:
            simbolos_der = produccion.derecha
            primeros_prod = set()
            i = 0
            while i < len(simbolos_der) and '' in primeros[simbolos_der[i]]:
                primeros_prod |= primeros[simbolos_der[i]] - {''}
                i += 1
            if i == len(simbolos_der):
                primeros_prod.add('')
            elif simbolos_der[i] in gramatica.terminales:
                primeros_prod.add(simbolos_der[i])
            else:
                primeros_prod |= primeros[simbolos_der[i]] - {''}
            antes = len(primeros[produccion.izquierda])
            primeros[produccion.izquierda] |= primeros_prod
            if len(primeros[produccion.izquierda]) > antes:
                cambios = True
        if not cambios:
            break
    return primeros


def siguiente(gramatica, primeros):
    siguientes = {}
    # Inicializar los conjuntos siguientes para cada símbolo no terminal
    for no_terminal in gramatica.no_terminales:
        siguientes[no_terminal] = set()
    # Agregar el símbolo de fin de cadena al conjunto siguiente del símbolo no terminal inicial
    siguientes[gramatica.inicial].add('$')
    # Iterar hasta que no haya cambios en los conjuntos siguientes
    while True:
        cambios = False
        for produccion in gramatica.producciones:
            simbolos_der = produccion.derecha
            for i, simbolo_der in enumerate(simbolos_der):
                if simbolo_der in gramatica.no_terminales:
                    antes = len(siguientes[simbolo_der])
                    # El siguiente del símbolo no terminal de la derecha es el primer
                    # símbolo terminal que sigue en la producción o el conjunto siguiente
                    # del símbolo no terminal de la derecha si todos los símbolos siguientes
                    # derivan en la cadena vacía
                    if i == len(simbolos_der) - 1:
                        siguientes[simbolo_der] |= siguientes[produccion.izquierda]
                    else:
                        siguientes_simbolo = primeros[simbolos_der[i+1]] | {''}
                        siguientes[simbolo_der] |= siguientes_simbolo - {''}
                        # Si todos los símbolos siguientes derivan en la cadena vacía,
                        # se agrega el conjunto siguiente del símbolo de la izquierda
                        if '' in primeros[simbolos_der[i+1]]:
                            siguientes[simbolo_der] |= siguientes[produccion.izquierda]
                    if len(siguientes[simbolo_der]) > antes:
                        cambios = True
                else:
                    continue
        if not cambios:
            break
    return siguientes
