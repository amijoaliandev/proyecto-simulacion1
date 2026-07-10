# =====================================================================
# MÉTODO CONGRUENCIAL MIXTO
# =====================================================================

# Definimos una "función". Velo como una máquina o una receta.
# Le damos un nombre ('generar_congruencial') y le decimos qué datos necesita para funcionar:
# - semilla: el número de arranque
# - a: el multiplicador
# - c: la constante aditiva
# - m: el módulo
# - cantidad: cuántos números queremos generar (en tu cuaderno piden 6)
def generar_congruencial(semilla, a, c, m, cantidad):
    
    # Creamos una lista vacía para ir guardando los números decimales (entre 0 y 1)
    numeros_generados = []
    
    # Creamos otra lista vacía para guardar los valores enteros X (por si queremos verlos)
    valores_x = []
    
    # Empezamos nuestro valor actual con la semilla que el usuario decida
    x_actual = semilla
    
    # Hacemos un ciclo "for". Esto le dice a Python: "repite estas instrucciones
    # tantas veces como diga la variable 'cantidad'"
    for i in range(cantidad):
        
        # Aplicamos la fórmula del cuaderno:
        # En Python, el símbolo '*' es multiplicación y '%' es el operador MÓDULO (residuo)
        x_siguiente = (a * x_actual + c) % m
        
        # Convertimos este número entero a un decimal entre 0 y 1 dividiéndolo por el módulo 'm'
        r_i = x_siguiente / m
        
        # Guardamos el decimal en nuestra lista de resultados
        numeros_generados.append(r_i)
        
        # Guardamos el entero X en nuestra lista de enteros
        valores_x.append(x_siguiente)
        
        # IMPORTANTE: El número que acabamos de calcular (x_siguiente) se convierte
        # en el número inicial (x_actual) para la siguiente vuelta del ciclo
        x_actual = x_siguiente
        
    # Cuando el ciclo termina, nuestra "máquina" nos devuelve las dos listas con los resultados
    return numeros_generados, valores_x


# --- PRUEBA DEL GENERADOR ---
# Para comprobar que funciona, vamos a darle unos valores iniciales de prueba:
mi_semilla = 45
multiplicador_a = 21
constante_c = 15
modulo_m = 100
cantidad_a_generar = 6

# Llamamos a nuestra función pasándole nuestras variables de prueba
resultados_decimales, enteros_x = generar_congruencial(mi_semilla, multiplicador_a, constante_c, modulo_m, cantidad_a_generar)

# Imprimimos los resultados en la consola para ver qué pasó
print("Valores enteros generados (X_i):", enteros_x)
print("Números pseudoaleatorios (R_i) entre 0 y 1:")
print(resultados_decimales)
# =====================================================================
# MÉTODO CONGRUENCIAL MIXTO
# =====================================================================
def generar_congruencial(semilla, a, c, m, cantidad):
    numeros_generados = []
    valores_x = []
    x_actual = semilla
    for i in range(cantidad):
        x_siguiente = (a * x_actual + c) % m
        r_i = x_siguiente / m
        numeros_generados.append(r_i)
        valores_x.append(x_siguiente)
        x_actual = x_siguiente
    return numeros_generados, valores_x


# =====================================================================
# MÉTODO DE CUADRADOS MEDIOS
# =====================================================================
# Le pedimos una semilla de 4 dígitos y cuántos números queremos generar
def generar_cuadrados_medios(semilla, cantidad):
    numeros_generados = []
    valores_x = []
    x_actual = semilla
    
    for i in range(cantidad):
        # 1. Elevamos al cuadrado
        cuadrado = x_actual ** 2
        
        # Convertimos el número a texto (string) para poder manipular sus dígitos fácilmente
        cadena_cuadrado = str(cuadrado)
        
        # 2. Si el número al cuadrado tiene menos de 8 dígitos, le agregamos ceros a la izquierda
        # .zfill(8) hace exactamente eso de manera automática en Python
        cadena_rellenada = cadena_cuadrado.zfill(8)
        
        # 3. Extraemos los 4 dígitos centrales.
        # En Python, el texto funciona como una lista. Del índice 2 al 6 tomamos el centro:
        # Ejemplo: "32 7641 76" -> Índices de posición: 01 2345 67. Tomamos de la posición 2 a la 5.
        digitos_centro = cadena_rellenada[2:6]
        
        # Convertimos de nuevo ese texto a un número entero X_i
        x_siguiente = int(digitos_centro)
        
        # 4. Convertimos a un decimal R_i entre 0 y 1 dividiéndolo por 10,000
        r_i = x_siguiente / 10000.0
        
        # Guardamos los resultados
        numeros_generados.append(r_i)
        valores_x.append(x_siguiente)
        
        # Preparamos la semilla para la siguiente iteración
        x_actual = x_siguiente
        
    return numeros_generados, valores_x


# --- SECCIÓN DE PRUEBAS ---
# Probamos el Congruencial Mixto
res_dec_cong, enteros_x_cong = generar_congruencial(semilla=45, a=21, c=15, m=100, cantidad=6)

# Probamos Cuadrados Medios (usamos una semilla clásica de 4 dígitos)
res_dec_cuad, enteros_x_cuad = generar_cuadrados_medios(semilla=5724, cantidad=6)

# Imprimimos ambos resultados de forma ordenada
print("=== RESULTADOS DEL MÉTODO CONGRUENCIAL MIXTO ===")
print("Valores enteros (X_i):", enteros_x_cong)
print("Números R_i:", res_dec_cong)
print("\n")

print("=== RESULTADOS DEL MÉTODO DE CUADRADOS MEDIOS ===")
print("Valores enteros (X_i):", enteros_x_cuad)
print("Números R_i:", res_dec_cuad)