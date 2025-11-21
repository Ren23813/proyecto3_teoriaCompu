#[ "", [ "", "", ""], "", [ "", "", ""], [ "", "", ""]],
import json
import re

import re

def procesar_cadena(cadena, desencriptar=False):
    # Selección del patrón según sea cifrado o descifrado
    if desencriptar:
        patron = r'^[a-zA-ZñÑ_ ]+$'   # permite letras, espacios y '_'
    else:
        patron = r'^[a-zA-ZñÑ ]+$'    # permite solo letras y espacios

    # Validación
    if not re.match(patron, cadena):
        return None  # cadena inválida

    # Convertir a mayúsculas
    cadena = cadena.upper()

    # Si estamos cifrando (desencriptar=False), reemplazar espacios con "_"
    if not desencriptar:
        cadena = cadena.replace(" ", "_")

    return cadena


def validar_numero_o_letra(entrada):
    entrada = entrada.strip()

    # ---- CASO 1: Número entre 1 y 27 ----
    if entrada.isdigit():
        if entrada.startswith("0"):
            return None  # No debe tener ceros a la izquierda
        numero = int(entrada)
        if 1 <= numero <= 27:
            return str(numero)
        return None

    # ---- CASO 2: Letra individual ----
    if len(entrada) == 1:
        letra = entrada.upper()

        # aceptar A–Z + Ñ, excepto la letra A
        if letra == "A":
            return None

        # patrón para letras sin tilde + ñ
        if re.match(r"[BCDEFGHIJKLMNÑOPQRSTUVWXYZ]", letra):
            return letra

    # Si no es ni número válido ni letra válida
    return None


# leer símbolos
def read_symbol(cinta, p):
    if 0 <= p < len(cinta):
        return cinta[p]
    return "?"  # blank por defecto


def match_pat(patron, actual):
    # "*" en el patrón = comodín (cualquier símbolo)
    if patron == "*":
        return True
    return patron == actual

def ensure_index(cinta, idx):
    # si idx < 0, insertar blanks a la izquierda hasta que idx sea >= 0
    while idx < 0:
        cinta.insert(0, "?")
        idx += 1
    # si idx fuera >= len, extendemos a la derecha
    while idx >= len(cinta):
        cinta.append("?")
    return idx

def apply_move(idx, mov):
    if mov == "L":
        return idx - 1
    if mov == "R":
        return idx + 1
    return idx  # "-" o cualquier otro -> quedarse



def interpreteTuring(key, cadena, archivo_json):

    with open(archivo_json, "r",encoding="utf-8") as archivo: #en turing2, la diferencia está en q4 y q5
        turingEncriptar = json.load(archivo)
        
    estados = turingEncriptar['estados']
    alfabeto_input = turingEncriptar['alfabeto_input']
    alfabeto_cinta = turingEncriptar['alfabeto_cinta']
    inicial = turingEncriptar['inicial']
    aceptacion = turingEncriptar['aceptacion']
    reglas = turingEncriptar['reglas']

    cinta1 = ["?"]
    cinta2 = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?","?", "?", "?", "?","?", "?","?", "?","?", "?","?", "?"]
    cinta3 = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?","?", "?","?", "?","?", "?","?", "?","?","?", "?","?", "?"]

    cinta1.append(key)
    cinta1.append("#")
    cinta1 += list(cadena)      
    cinta1.append("?")

    puntero1 = 1
    puntero2 = 1
    puntero3 = 1

    punteroS1 = read_symbol(cinta1, puntero1)
    punteroS2 = read_symbol(cinta2, puntero2)
    punteroS3 = read_symbol(cinta3, puntero3)

    reglas_por_estado = {}
    for r in reglas:
        s = r[0]
        reglas_por_estado.setdefault(s, []).append(r)



    # bucle principal
    estadoActual = inicial
    max_steps = 100000
    steps = 0

    while estadoActual != aceptacion and steps < max_steps:
        steps += 1
        regla_aplicada = False

        lista_reglas = reglas_por_estado.get(estadoActual, [])
        for idx_regla, regla in enumerate(lista_reglas):
         
            entradaC1, entradaC2, entradaC3 = regla[1]
            estadoResultadoRegla = regla[2]
            escribe1, escribe2, escribe3 = regla[3]
            mov1, mov2, mov3 = regla[4]

            # comprobar coincidencia (respetando "*" como comodín, "?" como símbolo vacío)
            if (match_pat(entradaC1, punteroS1) and
                match_pat(entradaC2, punteroS2) and
                match_pat(entradaC3, punteroS3)):

                if escribe1 != "*":
                    cinta1[puntero1] = escribe1
                if escribe2 != "*":
                    cinta2[puntero2] = escribe2
                if escribe3 != "*":
                    cinta3[puntero3] = escribe3

                # --- mover punteros ---
                puntero1 = apply_move(puntero1, mov1)
                puntero2 = apply_move(puntero2, mov2)
                puntero3 = apply_move(puntero3, mov3)
                print(mov3)

                # --- asegurar índices válidos y ajustar cintas ---
                puntero1 = ensure_index(cinta1, puntero1)
                puntero2 = ensure_index(cinta2, puntero2)
                puntero3 = ensure_index(cinta3, puntero3)

                # --- actualizar lecturas ---
                punteroS1 = cinta1[puntero1]
                punteroS2 = cinta2[puntero2]
                punteroS3 = cinta3[puntero3]

                # --- actualizar estado ---
                estadoActual = estadoResultadoRegla

                regla_aplicada = True

                print(f"[{steps}] {regla[0]} --( {regla[1]} )-> {estadoResultadoRegla} | escribe=({regla[3]}) mov=({regla[4]})")
                break  # aplicar sólo la primera regla aplicable

        if not regla_aplicada:
            print("No se encontró regla aplicable en estado", estadoActual,
                "con símbolos", punteroS1, punteroS2, punteroS3, "pasos:", steps)
            break

    if estadoActual == aceptacion:
        print("Máquina aceptó en", steps, "pasos")
    else:
        print("Terminó sin aceptar (posible falta de regla o límite).")


        

    # muestra la cinta1 final (resultado) y cinta 2,3 
    #print("Cinta1 final (fragmento):", "".join(cinta1[:]))
    # print("Cinta2 (fragmento):", "".join(cinta2[:80]))
    # print("Cinta3 (fragmento):", "".join(cinta3[:80]))
    cinta1.pop(-1)
    cinta1.pop(0)
    print("".join(cinta1))






print("Bienvenido al programa de cifrado César")

menu = "1"
key = "12"
cadena = "FGDTYR"

while menu != "0":
    print("")
    print("1. Cifrar una frase")
    print("2. Descifrar una frase")
    print("0. Salir")

    menu = input("Seleccione una opción: ")

    if menu == "1":
        print("----Cifrar----")
        print("La frase solo debe de contener letras, puede escribir espacios y las mayúsculas y minúsculas se procesarán automáticamente")

        cadena = input("Ingrese la frase: ")
        resultado = procesar_cadena(cadena, desencriptar=False)

        if resultado is None:
            print("Error: solo se permiten letras y espacios (sin tildes, sin símbolos).")
      
        
                
        print("Ingresa un número del 1 al 27 o una letra de la B a la Z")

        key = str(input("Ingrese la llave: "))
        v = validar_numero_o_letra(key)

        if v != None:
            interpreteTuring(v, resultado, "fgdtyr.json")
        else:
            print("Ingresa un número del 1 al 27 o una letra de la B a la Z")

        
        
    


        

    elif menu == "2":
        print("----Descifrar----")
        print("La frase solo debe de contener letras, puede escribir espacios y las mayúsculas y minúsculas se procesarán automáticamente")

        cadena = input("Ingrese la frase: ")
        resultado = procesar_cadena(cadena, desencriptar=True)

        if resultado is None:
            print("Error: solo se permiten letras y espacios (sin tildes, sin símbolos).")
       
        
        print("Ingresa un número del 1 al 27 o una letra de la B a la Z")
 
      
        key = str(input("Ingrese la llave: "))
        v = validar_numero_o_letra(key)

        if v != None:
        
       
            interpreteTuring(v, resultado, "turing.json")
        else:
            print("Ingresa un número del 1 al 27 o una letra de la B a la Z")
  
        

        
        
           
    
    elif menu == "0":
        print("Gracias por usar el programa")

    else:
        print("Seleccione una opción válida")


key = "12"
cadena = "FGDTYR"
#cadena = "HOLA_MUNDO" #HOLA_MUNDO = QYUK_VEWNY


