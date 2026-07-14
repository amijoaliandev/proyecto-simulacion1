import tkinter as tk
from tkinter import messagebox, scrolledtext
import math

# LÓGICA DE LOS GENERADORES (MÉTODOS NATIVOS)

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

# MÉTODO DE INVERSIÓN 

def simular_dado_inversion(numeros):
    resultados = []
    for r in numeros:
        if r <= 0.1667: resultados.append(1)
        elif r <= 0.3333: resultados.append(2)
        elif r <= 0.5000: resultados.append(3)
        elif r <= 0.6667: resultados.append(4)
        elif r <= 0.8333: resultados.append(5)
        else: resultados.append(6)
    return resultados

def simular_binomial_inversion(numeros):
    f_acumulada = [0.000977, 0.010742, 0.054687, 0.171875, 0.376953, 0.623047, 0.828125, 0.945312, 0.989258, 0.999023, 1.000000]
    resultados = []
    for r in numeros:
        for x, limite in enumerate(f_acumulada):
            if r <= limite:
                resultados.append(x)
                break
    return resultados

# LÓGICA DE LAS PRUEBAS ESTADÍSTICAS

def evaluar_numeros(numeros):
    n = len(numeros)
    if n == 0: return "No hay números para evaluar."
    
    media = sum(numeros) / n
    suma_cuadrados = sum((x - media) ** 2 for x in numeros)
    varianza = suma_cuadrados / (n - 1) if n > 1 else 0
    
    z_critico = 1.96
    limite_inf_media = 0.5 - z_critico * (1 / math.sqrt(12 * n))
    limite_sup_media = 0.5 + z_critico * (1 / math.sqrt(12 * n))
    status_media = "✅ APROBADO" if limite_inf_media <= media <= limite_sup_media else "❌ RECHAZADO"
    
    limite_inf_chi2 = 0.8312
    limite_sup_chi2 = 12.8325
    chi_calculado = (n - 1) * varianza / (1 / 12)
    status_var = "✅ APROBADO" if limite_inf_chi2 <= chi_calculado <= limite_sup_chi2 else "❌ RECHAZADO"
    
    numeros_ordenados = sorted(numeros)
    d_max = 0
    for i in range(n):
        d_mas = ((i + 1) / n) - numeros_ordenados[i]
        d_menos = numeros_ordenados[i] - (i / n)
        d_max = max(d_max, d_mas, d_menos)
    status_ks = "✅ APROBADO" if d_max < 0.521 else "❌ RECHAZADO"
    
    dados_simulados = simular_dado_inversion(numeros)
    binomial_simulada = simular_binomial_inversion(numeros)
    
    reporte = "=====================================================\n"
    reporte += "            REPORTE DE VALIDACIÓN ESTADÍSTICA  \n"
    reporte += "=====================================================\n"
    reporte += f"🔢 Números uniformes U(0,1): {[round(x,4) for x in numeros]}\n\n"
    reporte += f"1. PRUEBA DE MEDIAS: {status_media}\n"
    reporte += f"   -> Media: {media:.4f}  |  Rango Seguro: [{limite_inf_media:.4f}, {limite_sup_media:.4f}]\n\n"
    reporte += f"2. PRUEBA DE VARIANZA: {status_var}\n"
    reporte += f"   -> Varianza: {varianza:.4f}  |  Chi2: {chi_calculado:.4f} en [{limite_inf_chi2}, {limite_sup_chi2}]\n\n"
    reporte += f"3. PRUEBA KOLMOGOROV-SMIRNOV: {status_ks}\n"
    reporte += f"   -> Distancia Máxima D: {d_max:.4f} (Límite permitido: 0.521)\n"
    reporte += "=====================================================\n"
    reporte += "        TRANSFORMACIÓN A VARIABLES DISCRETAS (PIZARRA)  \n"
    reporte += "=====================================================\n"
    reporte += "Aplicando Método de Inversión:\n"
    for j in range(n):
        reporte += f"   • R[{j+1}] = {numeros[j]:.4f}  --->  🎲 Dado = {dados_simulados[j]}  |  📊 Binomial(10, 0.5) = {binomial_simulada[j]}\n"
    reporte += "=====================================================\n"
    return reporte

# ACCIONES

    try:
        semilla = int(entrada_semilla.get())
        a = int(entrada_a.get())
        c = int(entrada_c.get())
        m = int(entrada_m.get())
        numeros = generar_congruencial(semilla, a, c, m, cantidad=6)
        reporte = evaluar_numeros(numeros)
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, "⚙️ METODO: CONGRUENCIAL MIXTO\n" + reporte)
    except ValueError:
        messagebox.showerror("Error", "Ingresa números enteros válidos.")

def accion_cuadrados():
    try:
        semilla = int(entrada_semilla_cuad.get())
        if len(str(semilla)) != 4:
            messagebox.showwarning("Aviso", "La semilla debe tener 4 dígitos.")
            return
        numeros = generar_cuadrados_medios(semilla, cantidad=6)
        reporte = evaluar_numeros(numeros)
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, "⚙️ METODO: CUADRADOS MEDIOS\n" + reporte)
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número entero de 4 dígitos.")

# DISEÑO DE LA APLICACIÓN (Look Moderno & Minimalista)

COLOR_BG = "#F4F6F9"         # Gris claro de fondo moderno
COLOR_CARD = "#FFFFFF"       # Blanco para los paneles
COLOR_TEXTO = "#2C3E50"      # Azul oscuro para las letras
COLOR_PRIMARY = "#3498DB"    # Azul para botones congruenciales
COLOR_SECONDARY = "#2ECC71"  # Verde para botones cuadrados medios

ventana = tk.Tk()
ventana.title("Simulador y Validador de Modelos Estocásticos")
ventana.geometry("640x720")
ventana.configure(bg=COLOR_BG)
ventana.resizable(False, False)

# Encabezado Estilizado
frame_header = tk.Frame(ventana, bg="#2C3E50", height=60)
frame_header.pack(fill="x", pady=(0, 15))
lbl_titulo = tk.Label(frame_header, text="LABORATORIO DE SIMULACIÓN", font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#2C3E50")
lbl_titulo.pack(pady=15)

# --- PANEL CONGRUENCIAL MIXTO ---
frame_cong = tk.LabelFrame(ventana, text=" Método Congruencial Mixto ", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO, bd=1, relief="solid", padx=15, pady=10)
frame_cong.pack(fill="x", padx=20, pady=5)

# Estilo de etiquetas internas
estilo_lbl = {"bg": COLOR_CARD, "fg": COLOR_TEXTO, "font": ("Segoe UI", 9)}

tk.Label(frame_cong, text="Semilla (X0):", **estilo_lbl).grid(row=0, column=0, sticky="e", pady=4)
entrada_semilla = tk.Entry(frame_cong, width=8, font=("Segoe UI", 9))
entrada_semilla.insert(0, "45")
entrada_semilla.grid(row=0, column=1, padx=5)

tk.Label(frame_cong, text="Multiplicador (a):", **estilo_lbl).grid(row=0, column=2, sticky="e")
entrada_a = tk.Entry(frame_cong, width=8, font=("Segoe UI", 9))
entrada_a.insert(0, "21")
entrada_a.grid(row=0, column=3, padx=5)

tk.Label(frame_cong, text="Incremento (c):", **estilo_lbl).grid(row=1, column=0, sticky="e", pady=4)
entrada_c = tk.Entry(frame_cong, width=8, font=("Segoe UI", 9))
entrada_c.insert(0, "15")
entrada_c.grid(row=1, column=1, padx=5)

tk.Label(frame_cong, text="Módulo (m):", **estilo_lbl).grid(row=1, column=2, sticky="e")
entrada_m = tk.Entry(frame_cong, width=8, font=("Segoe UI", 9))
entrada_m.insert(0, "100")
entrada_m.grid(row=1, column=3, padx=5)

btn_cong = tk.Button(frame_cong, text="Simular Sistema", command=accion_congruencial, bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", activebackground="#2980B9", activeforeground="white")
btn_cong.grid(row=0, column=4, rowspan=2, padx=20, ipadx=10, ipady=5, sticky="nsew")

# --- PANEL CUADRADOS MEDIOS ---
frame_cuad = tk.LabelFrame(ventana, text=" Método de Cuadrados Medios ", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO, bd=1, relief="solid", padx=15, pady=10)
frame_cuad.pack(fill="x", padx=20, pady=10)

tk.Label(frame_cuad, text="Semilla (4 dígitos):", **estilo_lbl).grid(row=0, column=0, sticky="e")
entrada_semilla_cuad = tk.Entry(frame_cuad, width=12, font=("Segoe UI", 9))
entrada_semilla_cuad.insert(0, "5724")
entrada_semilla_cuad.grid(row=0, column=1, padx=10)

btn_cuad = tk.Button(frame_cuad, text="Simular Sistema", command=accion_cuadrados, bg=COLOR_SECONDARY, fg="white", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", activebackground="#27AE60", activeforeground="white")
btn_cuad.grid(row=0, column=2, padx=45, ipadx=10, ipady=4)

# --- PANEL CONSOLA DE RESULTADOS ---
frame_resultados = tk.Frame(ventana, bg=COLOR_BG)
frame_resultados.pack(fill="both", expand=True, padx=20, pady=(5, 20))

lbl_consola = tk.Label(frame_resultados, text="📊 Pantalla de Resultados y Análisis de la Pizarra", font=("Segoe UI", 10, "bold"), bg=COLOR_BG, fg=COLOR_TEXTO)
lbl_consola.pack(anchor="w", pady=(0, 5))

txt_resultados = scrolledtext.ScrolledText(frame_resultados, font=("Consolas", 10), bg="#1E272C", fg="#E0E6ED", insertbackground="white", bd=0)
txt_resultados.pack(fill="both", expand=True)
txt_resultados.insert(tk.END, "Configura los parámetros de arriba y presiona 'Simular Sistema' para ver la magia...")

ventana.mainloop()