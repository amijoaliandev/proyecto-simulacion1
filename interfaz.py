import tkinter as tk
from tkinter import messagebox, scrolledtext
import math

# =====================================================================
# LÓGICA DE LOS GENERADORES (MÉTODOS NATIVOS)
# =====================================================================
def generar_congruencial(semilla, a, c, m, cantidad):
    numeros_generados = []
    x_actual = semilla
    for _ in range(cantidad):
        x_siguiente = (a * x_actual + c) % m
        numeros_generados.append(x_siguiente / m)
        x_actual = x_siguiente
    return numeros_generados

def generar_cuadrados_medios(semilla, cantidad):
    numeros_generados = []
    x_actual = semilla
    for _ in range(cantidad):
        cuadrado = x_actual ** 2
        cadena_rellenada = str(cuadrado).zfill(8)
        digitos_centro = cadena_rellenada[2:6]
        x_siguiente = int(digitos_centro)
        numeros_generados.append(x_siguiente / 10000.0)
        x_actual = x_siguiente
    return numeros_generados

# =====================================================================
# MÉTODO DE INVERSIÓN (DE LA PIZARRA)
# =====================================================================
def simular_dado_inversion(numeros):
    """
    Simula el lanzamiento de un dado (1 a 6) usando el método de inversión.
    Rangos basados en probabilidades acumuladas (F(x)):
    - [0.00, 0.166] -> 1
    - (0.166, 0.333] -> 2
    - (0.333, 0.500] -> 3
    - (0.500, 0.666] -> 4
    - (0.666, 0.833] -> 5
    - (0.833, 1.000] -> 6
    """
    resultados = []
    for r in numeros:
        if r <= 0.1667:
            resultados.append(1)
        elif r <= 0.3333:
            resultados.append(2)
        elif r <= 0.5000:
            resultados.append(3)
        elif r <= 0.6667:
            resultados.append(4)
        elif r <= 0.8333:
            resultados.append(5)
        else:
            resultados.append(6)
    return resultados

def simular_binomial_inversion(numeros):
    """
    Simula una Binomial(n=10, p=0.5) usando el método de inversión de la pizarra.
    Compara el número aleatorio R con la función de distribución acumulada F(x).
    """
    # Tabla de probabilidades acumuladas F(x) de la pizarra para X ~ B(10, 0.5)
    f_acumulada = [
        0.000977,  # X = 0
        0.010742,  # X = 1
        0.054687,  # X = 2
        0.171875,  # X = 3
        0.376953,  # X = 4
        0.623047,  # X = 5
        0.828125,  # X = 6
        0.945312,  # X = 7
        0.989258,  # X = 8
        0.999023,  # X = 9
        1.000000   # X = 10
    ]
    
    resultados = []
    for r in numeros:
        # Buscamos el primer valor donde r es menor o igual a F(x)
        for x, limite in enumerate(f_acumulada):
            if r <= limite:
                resultados.append(x)
                break
    return resultados

# =====================================================================
# LÓGICA DE LAS PRUEBAS ESTADÍSTICAS (MANUALES)
# =====================================================================
def evaluar_numeros(numeros):
    n = len(numeros)
    if n == 0: return "No hay números para evaluar."
    
    media = sum(numeros) / n
    suma_cuadrados = sum((x - media) ** 2 for x in numeros)
    varianza = suma_cuadrados / (n - 1) if n > 1 else 0
    
    # Pruebas fijas para n=6
    z_critico = 1.96
    limite_inf_media = 0.5 - z_critico * (1 / math.sqrt(12 * n))
    limite_sup_media = 0.5 + z_critico * (1 / math.sqrt(12 * n))
    status_media = "APROBADO" if limite_inf_media <= media <= limite_sup_media else "RECHAZADO"
    
    limite_inf_chi2 = 0.8312
    limite_sup_chi2 = 12.8325
    chi_calculado = (n - 1) * varianza / (1 / 12)
    status_var = "APROBADO" if limite_inf_chi2 <= chi_calculado <= limite_sup_chi2 else "RECHAZADO"
    
    # Kolmogorov-Smirnov
    numeros_ordenados = sorted(numeros)
    d_max = 0
    for i in range(n):
        d_mas = ((i + 1) / n) - numeros_ordenados[i]
        d_menos = numeros_ordenados[i] - (i / n)
        d_max = max(d_max, d_mas, d_menos)
    status_ks = "APROBADO" if d_max < 0.521 else "RECHAZADO"
    
    # Simular las variables discretas de la pizarra
    dados_simulados = simular_dado_inversion(numeros)
    binomial_simulada = simular_binomial_inversion(numeros)
    
    # Construir reporte de texto
    reporte = "=====================================================\n"
    reporte += "            REPORTE DE VALIDACIÓN ESTADÍSTICA  \n"
    reporte += "=====================================================\n"
    reporte += f"Números generados: {[round(x,4) for x in numeros]}\n\n"
    reporte += f"1. PRUEBA DE MEDIAS: {status_media}\n"
    reporte += f"   -> Media calculada: {media:.4f} (Esperada: 0.5)\n"
    reporte += f"   -> Rango Aceptable: [{limite_inf_media:.4f}, {limite_sup_media:.4f}]\n\n"
    reporte += f"2. PRUEBA DE VARIANZA: {status_var}\n"
    reporte += f"   -> Varianza calculada: {varianza:.4f}\n"
    reporte += f"   -> Chi2 calculado: {chi_calculado:.4f} en rango [{limite_inf_chi2}, {limite_sup_chi2}]\n\n"
    reporte += f"3. PRUEBA KOLMOGOROV-SMIRNOV: {status_ks}\n"
    reporte += f"   -> Distancia Máxima D: {d_max:.4f} (Límite permitido: 0.521)\n"
    reporte += "=====================================================\n"
    reporte += "         SIMULACIÓN DE VARIABLES DISCRETAS (PIZARRA)  \n"
    reporte += "=====================================================\n"
    reporte += "Método de Inversión:\n"
    for j in range(n):
        reporte += f"   R[{j+1}] = {numeros[j]:.4f}  --->  Dado = {dados_simulados[j]}  |  Binomial(10, 0.5) = {binomial_simulada[j]}\n"
    reporte += "=====================================================\n"
    return reporte

# =====================================================================
# ACCIONES DE LOS BOTONES DE LA INTERFAZ
# =====================================================================
def accion_congruencial():
    try:
        semilla = int(entrada_semilla.get())
        a = int(entrada_a.get())
        c = int(entrada_c.get())
        m = int(entrada_m.get())
        
        numeros = generar_congruencial(semilla, a, c, m, cantidad=6)
        reporte = evaluar_numeros(numeros)
        
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, "MÉTODO: CONGRUENCIAL MIXTO\n" + reporte)
    except ValueError:
        messagebox.showerror("Error de datos", "Por favor ingresa números enteros válidos en los campos.")

def accion_cuadrados():
    try:
        semilla = int(entrada_semilla_cuad.get())
        if len(str(semilla)) != 4:
            messagebox.showwarning("Aviso", "La semilla de Cuadrados Medios debe tener exactamente 4 dígitos.")
            return
            
        numeros = generar_cuadrados_medios(semilla, cantidad=6)
        reporte = evaluar_numeros(numeros)
        
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, "MÉTODO: CUADRADOS MEDIOS\n" + reporte)
    except ValueError:
        messagebox.showerror("Error de datos", "Por favor ingresa un número entero de 4 dígitos.")

# =====================================================================
# DISEÑO DE LA VENTANA PRINCIPAL
# =====================================================================
ventana = tk.Tk()
ventana.title("Simulador Estadístico de Números Aleatorios")
ventana.geometry("620x700")
ventana.resizable(False, False)

# Título Principal
lbl_titulo = tk.Label(ventana, text="Generador y Validador de Números Pseudoaleatorios", font=("Arial", 13, "bold"), fg="darkblue")
lbl_titulo.pack(pady=10)

# --- PANEL METODO CONGRUENCIAL ---
frame_cong = tk.LabelFrame(ventana, text=" Parámetros Congruencial Mixto ", font=("Arial", 10, "bold"), padx=10, pady=5)
frame_cong.pack(fill="x", padx=15, pady=5)

tk.Label(frame_cong, text="Semilla (X0):").grid(row=0, column=0, sticky="e")
entrada_semilla = tk.Entry(frame_cong, width=8)
entrada_semilla.insert(0, "45")
entrada_semilla.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_cong, text="Multiplicador (a):").grid(row=0, column=2, sticky="e")
entrada_a = tk.Entry(frame_cong, width=8)
entrada_a.insert(0, "21")
entrada_a.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_cong, text="Incremento (c):").grid(row=1, column=0, sticky="e")
entrada_c = tk.Entry(frame_cong, width=8)
entrada_c.insert(0, "15")
entrada_c.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_cong, text="Módulo (m):").grid(row=1, column=2, sticky="e")
entrada_m = tk.Entry(frame_cong, width=8)
entrada_m.insert(0, "100")
entrada_m.grid(row=1, column=3, padx=5, pady=2)

btn_cong = tk.Button(frame_cong, text="Generar y Validar", command=accion_congruencial, bg="lightblue", font=("Arial", 9, "bold"))
btn_cong.grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

# --- PANEL METODO CUADRADOS MEDIOS ---
frame_cuad = tk.LabelFrame(ventana, text=" Parámetros Cuadrados Medios ", font=("Arial", 10, "bold"), padx=10, pady=5)
frame_cuad.pack(fill="x", padx=15, pady=5)

tk.Label(frame_cuad, text="Semilla (4 dígitos):").grid(row=0, column=0, sticky="e")
entrada_semilla_cuad = tk.Entry(frame_cuad, width=12)
entrada_semilla_cuad.insert(0, "5724")
entrada_semilla_cuad.grid(row=0, column=1, padx=10, pady=5)

btn_cuad = tk.Button(frame_cuad, text="Generar y Validar", command=accion_cuadrados, bg="lightgreen", font=("Arial", 9, "bold"))
btn_cuad.grid(row=0, column=2, padx=40)

# --- CUADRO DE RESULTADOS ---
frame_resultados = tk.LabelFrame(ventana, text=" Consola de Resultados y Simulaciones ", font=("Arial", 10, "bold"))
frame_resultados.pack(fill="both", expand=True, padx=15, pady=10)

txt_resultados = scrolledtext.ScrolledText(frame_resultados, font=("Courier New", 9), bg="black", fg="lightgreen")
txt_resultados.pack(fill="both", expand=True, padx=5, pady=5)
txt_resultados.insert(tk.END, "Presiona cualquiera de los botones de arriba para iniciar la simulación...")

# Iniciar la aplicación
ventana.mainloop()