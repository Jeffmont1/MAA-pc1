import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Simulador MAA - UTP", layout="wide")

st.title("Simulador de ejercicio tipo sobre Movimiento Armónico Amortiguado")
st.markdown("---")
st.markdown("""
### Ejercicio de Tipo:
**Enunciado:** El oscilador representado en la figura posee una masa de 2 kg, una constante elástica $k = 8\\text{ N/m}$ y una constante de amortiguamiento $c = 1\\text{ N}\\cdot\\text{s/m}$. En el instante $t = 0$, la masa se libera del reposo en la posición $x = 0.1\\text{ m}$.

**Se requiere:**
1. Establecer una ecuación que describa la posición de la masa en función del tiempo.
2. Calcular el periodo y la frecuencia natural del sistema.
3. Determinar el periodo y la frecuencia central en ausencia de amortiguamiento.
4. Generar una gráfica que represente el movimiento oscilatorio.
""")
st.markdown("---")
# Barra lateral para ingreso de datos
st.sidebar.header("Parámetros del Sistema")
m = st.sidebar.number_input("Masa m (kg)", value=2.0, min_value=0.1)
k = st.sidebar.number_input("Constante k (N/m)", value=8.0, min_value=0.1)
b = st.sidebar.number_input("Amortiguamiento b (Ns/m)", value=1.0, min_value=0.0)
x0 = st.sidebar.number_input("Posición inicial x0 (m)", value=0.1)
v0 = st.sidebar.number_input("Velocidad inicial v0 (m/s)", value=0.0)

# 1. Cálculos Físicos
w0 = np.sqrt(k/m)      # Frecuencia natural
gamma = b/(2*m)        # Factor de amortiguamiento

# Caso Ideal (b=0)
T_ideal = 2 * np.pi / w0
f_ideal = 1 / T_ideal

# Columnas para mostrar resultados rápidos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Análisis de Frecuencias")
    st.write(f"**Frecuencia natural (w0):** {w0:.4f} rad/s")
    st.write(f"**Factor gamma:** {gamma:.4f}")
    st.info(f"**Periodo Ideal (T0):** {T_ideal:.4f} s | **Frecuencia:** {f_ideal:.4f} Hz")

with col2:
    st.subheader("Ecuaciones del Movimiento")
    if gamma < w0:
        tipo = "Subamortiguado"
        w_d = np.sqrt(w0**2 - gamma**2)
        T_d = 2 * np.pi / w_d
        f_d = 1 / T_d
        
        # Constantes para condiciones iniciales
        phi = np.arctan(-(v0 + gamma*x0) / (w_d*x0))
        A = x0 / np.cos(phi)
        
        st.success(f"Sistema: **{tipo}**")
        st.write(f"**x(t):** {A:.3f} · e^(-{gamma:.3f}t) · cos({w_d:.3f}t + {phi:.3f})")
        st.write(f"**v(t):** Derivada de x(t)")
        st.write(f"**a(t):** -({b/m:.2f})v - ({k/m:.2f})x")
        st.info(f"**Periodo Real (Td):** {T_d:.4f} s | **Frecuencia:** {f_d:.4f} Hz")
    else:
        st.warning("El sistema no es subamortiguado (revisar b, m, k).")

# 2. Generación de Gráficas
t = np.linspace(0, 15, 1000)
if gamma < w0:
    # Datos de las curvas
    x_t = A * np.exp(-gamma * t) * np.cos(w_d * t + phi)
    v_t = -A * np.exp(-gamma * t) * (gamma * np.cos(w_d * t + phi) + w_d * np.sin(w_d * t + phi))
    a_t = -(b/m)*v_t - (k/m)*x_t
    
    # Caso ideal para comparación
    x_ideal = x0 * np.cos(w0 * t)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    
    # Gráfica Posición
    axs[0].plot(t, x_t, 'b', label='Amortiguado')
    axs[0].plot(t, x_ideal, 'k--', alpha=0.3, label='Ideal (b=0)')
    axs[0].set_ylabel("Posición (m)")
    axs[0].legend()
    axs[0].grid(True)
    
    # Gráfica Velocidad
    axs[1].plot(t, v_t, 'g', label='Velocidad')
    axs[1].set_ylabel("Velocidad (m/s)")
    axs[1].grid(True)
    
    # Gráfica Aceleración
    axs[2].plot(t, a_t, 'r', label='Aceleración')
    axs[2].set_ylabel("Aceleración (m/s²)")
    axs[2].set_xlabel("Tiempo (s)")
    axs[2].grid(True)

    st.pyplot(fig)
