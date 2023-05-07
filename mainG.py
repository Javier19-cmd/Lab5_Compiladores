from Grammar import *
from GramarF import primero, siguiente
from GrammarA import *
import re

yapar = "slr-2.yalp" # Variable que guarda el nombre del yapar.
yalex = "slr-2.yal" # Variable que guarda el nombre del yalex.

lista_tk = [] # Tokens del yalex.
lista_tkyp = [] # Tokens del yapar.

# Abriendo el archivo yalp.
with open(yapar) as y: 

    # Leyendo el archivo yalp.
    yalp = y.read()

    # print("Contenido: \n")
    # print(yalp)

    # Verificando que exista la misma cantidad de /* que de */.
    if yalp.count("/*") != yalp.count("*/"):
        #print("Error: Cantidad de comentarios /* y */ no coinciden.")

        # Buscando la línea que tiene el error.
        for i in range(len(yalp)):
            if yalp[i] == "/" and yalp[i+1] == "*":
                print("Error: Cantidad de comentarios /* y */ no coinciden en la línea " + str(i+1) + ".")
                break

    tokens = re.findall(r'(?<=\n)%token\s+[^%\s][^\n]*', yalp)

    toke = re.findall(r'(?<=\n)%token\s+[^%\s][^\n]*', yalp)

    #print("Toke: ", toke)

    #print(tokens)

    for token in tokens:

        #print("Token: ", token)

        token_name = token.split()[1]
        tok = token.split()[0]

        #print(token_name)

        # Guardando los tokens en una lista.
        lista_tkyp.append(token_name)

        # if tok != "%token":
        #     print(f"La definición de {token_name} es inválida")
    
    #print("Tokens del yapar: ", lista_tkyp)

    # Lista de tokens válidos
    valid_tokens = ["%token"]

    # Recorrer cada definición de token
    for token in toke:
        token_parts = token.split()
        token_name = token_parts[1]
        tok = token_parts[0]

        # Verificar si la definición es válida
        if not tok.startswith("%") or (tok not in valid_tokens and len(token_parts) < 3):
            print(f"La definición de {token_name} es inválida.")
        else:
            print(f"La definición de {token_name} es válida.")
    
    ti = re.findall(r'(?<=\n)token\s+[^\s][^\n]*', yalp)

    #print("Ti: ", ti)

    # Si hay una o más definiciones de token sin el %, entonces es un error.
    if len(ti) > 0:
        #print("Error: Definición de token sin el %.")
        
        # Imprimiendo la o las definiciones erróneas.
        for i in range(len(ti)):
            print("Definición errónea: ", ti[i])
    
    #print("Lista sin el token error: ", lista_tkyp)

    # Validando el token dentro del yalex.
    with open(yalex) as y:
        yalex = y.read()

        # Jalando los tokens especiales.
        if "rule tokens =" in yalex:
            # Extrayendo la cadena de texto que contiene los tokens especiales.
            cadena_tokens = yalex[yalex.find("rule tokens ="):]
            # Separando los tokens en una lista.
            lista_tokens = cadena_tokens.split("|")
            # Creando el diccionario para guardar los tokens.
            diccionario_tokens = {}
            # Iterando sobre la lista de tokens y agregándolos al diccionario.
            for token in lista_tokens:
                # Extrayendo el nombre del token y su valor.
                nombre, valor = token.split("return")
                # Agregando el token al diccionario.
                diccionario_tokens[nombre.strip()] = valor.strip().strip("\"")


            # Imprimiendo los tokens.
            #print("Imprimiendo los tokens...")
            for key, value in diccionario_tokens.items():
              #  print(f"{key.strip()} {value.strip()}")
              pass

            # Imprimiendo los valores dentro de las llaves {}.
            #print("Imprimiendo los valores dentro de las llaves {}...")
            for key, value in diccionario_tokens.items():
                token_value = value.strip()

                # Quitando los {} del token value.
                token_value = token_value.replace("{", "").replace("}", "")

                # Quitando los asteriscos y cualquier otro texto dentro de los {}
                token_value = token_value.split("(")[0].strip()
                
                lista_tk.append(token_value.strip())

                #print("Token value: ", token_value.strip())
    

    #print("Tokens: ", lista_tk)

    # Tokens del yalex: lista_tk.
    # Tokens del yapar: lista_tkyp.

    print("\n")

    # Verificando que los tokens de la lista_tkyp estén en la lista_tk.
    for token in lista_tkyp:
        if token not in lista_tk:
            print("Error: El token " + token + " no está definido en el yalex.")
        else: 
            print("El token " + token + " está definido en el yalex.")