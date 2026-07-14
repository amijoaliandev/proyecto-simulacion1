import math
from generadores import generar_congruencial, generar_cuadrados_medios

# PRUEBAS ESTADÍSTICAS NATIVAS

def prueba_de_medias(numeros, alpha=0.05):
    """
    Evalúa si el promedio de la muestra está estadísticamente cerca de 0.5.
    """
    n = len(numeros)
    media = sum(numeros) / n
    
    # Valor crítico de Z para un nivel de significancia típico (alpha = 0.05 de dos colas)
    # El valor Z_critico para el 95% de confianza es siempre 1.96
    z_critico = 1.96
    
    # Calculamos los límites superior e inferior del intervalo de aceptación
    limite_inferior = 0.5 - z_critico * (1 / math.sqrt(12 * n))
    limite_superior = 0.5 + z_critico * (1 / math.sqrt(12 * n))
    
    aprobado = limite_inferior <= media <= limite_superior
    status = "APROBADO" if aprobado else "RECHAZADO"
    
    print("1. Prueba de Medias:")
    print(f"   -> Media Muestral: {media:.4f} (Esperada: 0.5)")
    print(f"   -> Intervalo de confianza (95%): [{limite_inferior:.4f}, {limite_superior:.4f}]")
    print(f"   -> Resultado: {status}")
    return aprobado


def prueba_de_varianza(numeros, alpha=0.05):
    """
    Evalúa si la dispersión de los datos se comporta estadísticamente bien.
    """
    n = len(numeros)
    media = sum(numeros) / n
    
    # Calculamos la varianza muestral de forma manual
    suma_cuadrados = sum((x - media) ** 2 for x in numeros)
    varianza = suma_cuadrados / (n - 1) if n > 1 else 0
    
    # Valores de la tabla Chi-cuadrado para n=6 grados de libertad (n-1 = 5) y alpha=0.05:
    # L_inf (percentil 0.025) = 0.831  |  L_sup (percentil 0.975) = 12.833
    if n == 6:
        limite_inferior_chi2 = 0.8312
        limite_superior_chi2 = 12.8325
    else:
        # Valores por defecto aproximados para otros tamaños de muestra pequeños
        limite_inferior_chi2 = 0.5 * (n - 1)
        limite_superior_chi2 = 2.5 * (n - 1)
        
    # El estadístico Chi-cuadrado calculado
    chi_calculado = (n - 1) * varianza / (1 / 12)
    
    aprobado = limite_inferior_chi2 <= chi_calculado <= limite_superior_chi2
    status = "APROBADO" if aprobado else "RECHAZADO"
    
    print("2. Prueba de Varianza:")
    print(f"   -> Varianza Muestral: {varianza:.4f} (Esperada: 0.0833)")
    print(f"   -> Chi-cuadrado calculado: {chi_calculado:.4f}")
    print(f"   -> Intervalo de aceptación Chi2: [{limite_inferior_chi2:.4f}, {limite_superior_chi2:.4f}]")
    print(f"   -> Resultado: {status}")
    return aprobado


def prueba_kolmogorov_smirnov_manual(numeros):
    """
    Prueba de Kolmogorov-Smirnov aproximada para uniformidad en muestras de n=6.
    Compara las posiciones de los números ordenados frente a una uniforme perfecta.
    """
    n = len(numeros)
    # Ordenamos los números de menor a mayor
    numeros_ordenados = sorted(numeros)
    
    d_max = 0
    for i in range(n):
        # i + 1 representa cuántos datos deberíamos llevar acumulados teóricamente
        teorico_i = (i + 1) / n
        teorico_anterior = i / n
        real_i = numeros_ordenados[i]
        
        # Calculamos las distancias por arriba y por abajo de la curva teórica uniforme
        d_mas = teorico_i - real_i
        d_menos = real_i - teorico_anterior
        
        d_max = max(d_max, d_mas, d_menos)
        
    # Para n=6 y un nivel de significancia del 5% (alpha = 0.05),
    # el valor crítico de la tabla de Kolmogorov-Smirnov es exactamente 0.521
    d_critico = 0.521
    
    aprobado = d_max < d_critico
    status = "APROBADO" if aprobado else "RECHAZADO"
    
    print("3. Prueba Kolmogorov-Smirnov:")
    print(f"   -> Máxima distancia (D): {d_max:.4f}")
    print(f"   -> Distancia límite permitida: {d_critico}")
    print(f"   -> Resultado: {status}")
    return aprobado


def ejecutar_reporte(numeros, nombre_metodo):
    print("-" * 65)
    print(f" REPORTE ESTADÍSTICO PARA: {nombre_metodo.upper()} ")
    print("-" * 65)
    print(f"Números a evaluar: {[round(x, 4) for x in numeros]}")
    print("-" * 65)
    
    prueba_de_medias(numeros)
    print()
    prueba_de_varianza(numeros)
    print()
    prueba_kolmogorov_smirnov_manual(numeros)
    print("-" * 65)
    print("\n")

# EJECUCIÓN AUTOMÁTICA

print("Iniciando validación de generadores...\n")

# Evaluamos Congruencial Mixto
ri_cong, _ = generar_congruencial(semilla=45, a=21, c=15, m=100, cantidad=6)
ejecutar_reporte(ri_cong, "Congruencial Mixto")

# Evaluamos Cuadrados Medios
ri_cuad, _ = generar_cuadrados_medios(semilla=5724, cantidad=6)
ejecutar_reporte(ri_cuad, "Cuadrados Medios")