#[ "", [ "", "", ""], "", [ "", "", ""], [ "", "", ""]],
import json

with open("turing.json", "r",encoding="utf-8") as archivo: #en turing2, la diferencia está en q4 y q5
    turingEncriptar = json.load(archivo)
    
estados = turingEncriptar['estados']
alfabeto_input = turingEncriptar['alfabeto_input']
alfabeto_cinta = turingEncriptar['alfabeto_cinta']
inicial = turingEncriptar['inicial']
aceptacion = turingEncriptar['aceptacion']
reglas = turingEncriptar['reglas']


print("Bienvenido :D")
key = "10"
cadena = "HOLA_MUNDO" #HOLA_MUNDO = QYUK_VEWNY

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

# leer símbolos
def read_symbol(cinta, p):
    if 0 <= p < len(cinta):
        return cinta[p]
    return "?"  # blank por defecto

punteroS1 = read_symbol(cinta1, puntero1)
punteroS2 = read_symbol(cinta2, puntero2)
punteroS3 = read_symbol(cinta3, puntero3)

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
        estadoRegla = regla[0]
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
