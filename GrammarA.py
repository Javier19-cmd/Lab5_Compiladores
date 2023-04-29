# Definimos la función cerradura
def cerradura(I, rules):
    J = set(I)
    while True:
        added = False
        for item in J:
            if '.' in item[1]:
                continue
            B = item[1][item[1].index('.')+1]
            if B in rules:
                for prod in rules[B]:
                    newItem = (B, '.' + prod)
                    if newItem not in J:
                        J.add(newItem)
                        added = True
        if not added:
            break
    return J

# Definimos la función irA
def irA(I, X, rules):
    J = set()
    for item in I:
        if '.' in item[1] and item[1][-1] == X:
            newItem = (item[0], item[1][:-1] + X + '.')
            J.add(newItem)
    if X == '$' and not J:
        lastItem = I.pop()
        newItem = (lastItem[0], lastItem[1] + '$.')
        J.add(newItem)
    if X not in rules and X not in ['.', '$']:
        rules[X] = []
    return cerradura(J, rules)

def generar_automata(rules):
    # Creamos el item inicial
    I0 = {('S', '.')}

    # Obtenemos la cerradura del item inicial
    C = cerradura(I0, rules)

    # Creamos un diccionario para guardar los conjuntos de items
    conjuntos = {0: C}

    # Creamos una lista para guardar las transiciones del autómata
    transitions = []

    # Recorremos los conjuntos de items existentes
    for i, I in conjuntos.items():
        # Creamos una copia de las reglas de producción
        rules_copy = rules.copy()

        # Para cada símbolo de la gramática
        nuevos_conjuntos = []  # Creamos una nueva lista para almacenar los nuevos conjuntos de elementos
        for X in rules_copy:
            # Obtenemos el conjunto de items resultante al aplicar irA con el símbolo X
            J = irA(I, X, rules_copy)

            # Si el conjunto resultante no es vacío
            if J and J not in conjuntos.values() and J not in nuevos_conjuntos:
                # Obtenemos la cerradura del conjunto resultante
                J = cerradura(J, rules_copy)
                # Añadimos el conjunto resultante a los conjuntos de items
                nuevos_conjuntos.append(J)

                # Añadimos la transición del conjunto i al conjunto recién creado
                transitions.append((i, X, len(conjuntos) + len(nuevos_conjuntos) - 1))

            # Si el conjunto resultante ya existe en los conjuntos de items
            elif J in conjuntos.values():
                # Añadimos la transición del conjunto i al conjunto existente
                transitions.append((i, X, list(conjuntos.keys())[list(conjuntos.values()).index(J)]))

        # Añadimos los nuevos conjuntos de items al diccionario
        for j, conjunto in enumerate(nuevos_conjuntos):
            conjuntos[len(conjuntos) + j] = conjunto

        # Creamos una copia de las claves del diccionario para evitar el error "dictionary changed size during iteration"
        for rule in list(rules_copy.keys()):
            for prod in rules_copy[rule]:
                for symbol in prod:
                    if symbol not in rules_copy and symbol not in ['.', '$']:
                        rules_copy[symbol] = []

    # Devolvemos el resultado.
    return conjuntos, transitions


# Definimos las reglas de producción
rules = {
    'S': ['E $'],
    'E': ['T + E', 'T'],
    'T': ['F * T', 'F'],
    'F': ['( E )', 'id']
}

# Generamos el autómata a partir de las reglas de producción
conjuntos, transitions = generar_automata(rules)

# Mostramos los conjuntos de items
print("Conjuntos de items:")
for i, conjunto in conjuntos.items():
    print(f"I{i} = {{")
    for item in conjunto:
        print(f"    {item[0]} -> {item[1]}")
    print("}")

# Mostramos las transiciones
print("\nTransiciones:")
for transition in transitions:
    print(f"I{transition[0]} --{transition[1]}--> I{transition[2]}")