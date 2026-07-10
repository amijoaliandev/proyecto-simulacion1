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