import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="OVA: Métodos de Separación I", layout="wide")

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stProgress > div > div > div > div { background-color: #28a745; }
    .report-box { padding: 20px; border-radius: 10px; border: 2px solid #007bff; background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO (PERSISTENCIA) ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False
if 'nombre' not in st.session_state:
    st.session_state.nombre = ""
if 'puntos' not in st.session_state:
    st.session_state.puntos = 0
if 'progreso' not in st.session_state:
    st.session_state.progreso = 0
if 'actividades_hechas' not in st.session_state:
    st.session_state.actividades_hechas = set()
if 'respuestas_finales' not in st.session_state:
    st.session_state.respuestas_finales = {}

# --- LÓGICA DE GAMIFICACIÓN ---
elementos = {0: "Neutrón", 1: "Hidrógeno (H)", 2: "Helio (He)", 3: "Litio (Li)", 4: "Berilio (Be)", 5: "Boro (B)"}
nivel_actual = elementos[min(int(st.session_state.puntos), 5)]

# --- INTERFAZ DE LOGUEO ---
if not st.session_state.logueado:
    st.title("🧪 OVA: Métodos de Separación de Mezclas I")
    st.subheader("Bienvenido al Laboratorio Virtual de Ciencias Naturales")
    with st.container():
        nombre_input = st.text_input("Ingresa tus Nombres y Apellidos:")
        if st.button("Comenzar Aventura"):
            if len(nombre_input) > 5:
                st.session_state.nombre = nombre_input
                st.session_state.logueado = True
                st.rerun()
            else:
                st.warning("Por favor, ingresa tu nombre completo.")
    st.stop()

# --- BARRA DE NAVEGACIÓN FIJA (SIDEBAR) ---
with st.sidebar:
    st.header(f"👤 Estudiante: {st.session_state.nombre}")
    st.metric("Puntuación", f"{st.session_state.puntos}/5")
    st.write(f"🧬 Nivel Actual: **{nivel_actual}**")
    st.progress(st.session_state.progreso / 100)
    st.write(f"Progreso total: {st.session_state.progreso}%")

# --- CONTENIDO PRINCIPAL ---
st.title(f"🔍 Unidad 1: Filtración y Tamizado")
st.info("**Objetivo:** Aplicar técnicas de separación de mezclas sólidas y heterogéneas valorando el error como parte del aprendizaje.")

# --- INICIO: PRE-SABERES ---
st.header("1. ¿Qué tanto sabemos antes de empezar?")
col1, col2, col3 = st.columns(3)

with col1:
    q1 = st.radio("¿Si mezclas arena y piedras, cómo las separarías?", ["A mano", "Con un colador", "Con agua"], key="pre1")
    if q1 == "Con un colador": st.success("¡Exacto! Eso se llama tamizado.")

with col2:
    q2 = st.radio("¿Qué pasa si pasas agua con tierra por una tela?", ["Se mezcla más", "La tierra queda en la tela", "No pasa nada"], key="pre2")
    if q2 == "La tierra queda en la tela": st.success("¡Bien! Eso es una filtración simple.")

with col3:
    q3 = st.radio("En la ciencia, si un experimento sale mal...", ["Dejamos de intentar", "Es una oportunidad de aprender", "Lo borramos todo"], key="pre3")
    if q3 == "Es una oportunidad de aprender": st.success("¡Esa es la actitud científica!")

# --- CUERPO INDUCTIVO ---
st.divider()
st.header("2. Explorando los granos de nuestra tierra")

# Texto Inductivo (>500 palabras simulado con estructura)
st.markdown("""
### La materia no está sola
En la naturaleza, es muy raro encontrar sustancias puras. Casi todo lo que nos rodea, desde el aire que respiramos hasta el suelo que pisamos en nuestra región, son **mezclas**. Una mezcla es la unión de dos o más sustancias donde cada una conserva sus propiedades. Por ejemplo, si mezclas granos de café con arena, el café sigue siendo café y la arena sigue siendo arena.

Existen dos tipos principales de mezclas: las **homogéneas** (donde no se distinguen las partes, como el agua con sal disuelta) y las **heterogéneas** (donde sí vemos los componentes, como una ensalada o un puñado de tierra). 

Para separar estas mezclas, los científicos han diseñado métodos físicos. El **Tamizado** es uno de los más antiguos y se basa en la diferencia de tamaño de las partículas. Se usa un tamiz o cedazo que deja pasar lo pequeño y retiene lo grande. Imagina a los constructores separando la arena fina de las piedras para el revoque de una pared; eso es ciencia aplicada.

Por otro lado, la **Filtración** se usa para separar un sólido que no se disuelve en un líquido. Es lo que sucede cuando preparamos café: el filtro de papel retiene el grano molido (sólido) y deja pasar la infusión (líquido). En nuestra región, estos procesos son fundamentales para la industria agrícola y la purificación del agua de nuestros ríos.
""")

# Gráfico dinámico: Representación de partículas
fig, ax = plt.subplots(figsize=(6, 3))
x_grande = np.random.rand(10); y_grande = np.random.rand(10)
x_peque = np.random.rand(30); y_peque = np.random.rand(30)
ax.scatter(x_grande, y_grande, s=200, color='brown', label='Piedras/Granos')
ax.scatter(x_peque, y_peque, s=20, color='orange', label='Arena fina')
ax.set_title("Simulación de Mezcla Heterogénea")
ax.legend()
st.pyplot(fig)

# Actividades Inductivas
st.subheader("✍️ Actividades para tu cuaderno")
act_ind = ["Dibuja una mezcla de arena y granos de tu cocina.", 
           "Escribe 3 ejemplos de tamizado que veas en tu casa.",
           "Investiga qué es un tamiz y dibújalo.",
           "Realiza una tabla comparando mezcla homogénea vs heterogénea.",
           "Escribe un párrafo sobre por qué es importante separar la basura."]

for i, act in enumerate(act_ind):
    if st.button(f"Verificar Actividad {i+1}: {act[:30]}...", key=f"ind_{i}"):
        if f"ind_{i}" not in st.session_state.actividades_hechas:
            st.session_state.progreso += 5
            st.session_state.actividades_hechas.add(f"ind_{i}")
            st.rerun()

# Pregunta tipo ICFES
st.subheader("🧪 Desafío de Indagación")
st.write("Observa la gráfica de distribución de partículas anterior. Si el tamiz tiene poros de tamaño intermedio:")
opcion = st.radio("¿Qué sucedería?", ["Pasan todas las partículas", "Solo pasan las partículas naranjas (pequeñas)", "No pasa ninguna"])
with st.expander("Ver Retroalimentación"):
    if opcion == "Solo pasan las partículas naranjas (pequeñas)":
        st.success("¡Correcto! El tamizado funciona por tamaño de poro. Las partículas cafés son mayores al poro y quedan retenidas.")
        if "icfes_1" not in st.session_state.actividades_hechas:
            st.session_state.puntos += 0.5
            st.session_state.actividades_hechas.add("icfes_1")
    else:
        st.error("Incorrecto. Recuerda que el tamiz actúa como una barrera selectiva basada en el tamaño.")

# --- CUERPO DEDUCTIVO ---
st.divider()
st.header("3. Las Leyes de la Separación")
st.markdown("""
### ¿Por qué sucede la separación?
Desde un punto de vista deductivo, la separación de mezclas no es magia, es física. El principio fundamental es la **Diferencia de Propiedades Físicas**. 

1. **En el Tamizado:** La propiedad clave es el **Diámetro de Partícula**. Si $D_p > D_m$ (donde $D_p$ es el diámetro de la partícula y $D_m$ es el diámetro de la malla), la partícula no pasará.
2. **En la Filtración:** Intervienen la gravedad y la **Porosidad**. El filtro tiene canales diminutos que atrapan sólidos pero permiten el flujo del fluido debido a su baja viscosidad.

**Tolerancia al error:** En el laboratorio, es común que un filtro se rompa o que un tamiz deje pasar partículas que no debería. En la ciencia, esto no es un fracaso, se llama 'Incertidumbre' o 'Error Experimental'. Analizar por qué falló el método es lo que realmente hace a un científico.
""")

# Tabla de datos generada dinámicamente
datos_lab = pd.DataFrame({
    'Muestra': ['Arena Río', 'Suelo Volcánico', 'Granos Café'],
    'Método Sugerido': ['Tamizado', 'Filtración', 'Tamizado'],
    'Eficacia Esperada (%)': [95, 88, 99]
})
st.table(datos_lab)

# Actividades Deductivas
st.subheader("🧠 Aplicando lo aprendido en el cuaderno")
act_ded = ["Explica con tus palabras la fórmula de diámetro de partícula.",
           "Dibuja el montaje de una filtración usando un embudo.",
           "¿Qué pasaría si el papel filtro tiene huecos muy grandes? Explica.",
           "Crea un diagrama de flujo sobre cómo separar arena, agua y sal.",
           "Escribe un compromiso sobre cómo manejarás la frustración si un experimento no sale bien."]

for i, act in enumerate(act_ded):
    if st.button(f"Verificar Actividad {i+6}: {act[:30]}...", key=f"ded_{i}"):
        if f"ded_{i}" not in st.session_state.actividades_hechas:
            st.session_state.progreso += 5
            st.session_state.actividades_hechas.add(f"ded_{i}")
            st.rerun()

# --- EVALUACIÓN FINAL ---
st.divider()
st.header("4. Evaluación Final (Taller)")
with st.form("evaluacion"):
    st.write("### Selección Múltiple")
    ev1 = st.selectbox("1. ¿Qué método usarías para separar piedras de arena?", ["Filtración", "Tamizado", "Evaporación"])
    ev2 = st.selectbox("2. La filtración sirve para separar:", ["Sólido de Sólido", "Líquido de Líquido", "Sólido no soluble de Líquido"])
    ev3 = st.selectbox("3. Si un experimento falla, el científico debe:", ["Rendirse", "Analizar el error y repetir", "Cambiar los datos"])
    
    st.write("### Preguntas Abiertas")
    abierta1 = st.text_area("Explica detalladamente cómo realizarías una filtración de agua turbia de un río:")
    abierta2 = st.text_area("¿Por qué es importante el tamaño de los poros en un tamiz?")
    
    enviado = st.form_submit_button("Finalizar y Calificar")

if enviado:
    # Lógica de Calificación
    nota = 0
    errores = []
    if ev1 == "Tamizado": nota += 1
    else: errores.append("Tamizado/Teoría Básica")
    
    if ev2 == "Sólido no soluble de Líquido": nota += 1
    else: errores.append("Filtración/Aplicación de Leyes")
    
    if ev3 == "Analizar el error y repetir": nota += 1
    else: errores.append("Método Científico")

    # Validación de longitud de texto
    if len(abierta1.split()) < 10 or len(abierta2.split()) < 10:
        st.warning("⚠️ Tus respuestas abiertas son muy cortas. Debes escribir al menos 10-15 palabras para obtener los puntos completos.")
    else:
        nota += 2 # Puntos por esfuerzo en abiertas
    
    st.session_state.puntos = nota
    st.session_state.progreso = 100
    st.session_state.respuestas_finales = {"ev1": ev1, "ev2": ev2, "ev3": ev3, "ab1": abierta1, "ab2": abierta2}
    
    # --- RUTA DE FORTALECIMIENTO ---
    st.header("🏁 Ruta de Fortalecimiento Personalizada")
    with st.container():
        st.markdown("### ⚠️ De acuerdo a tus resultados, debes copiar la siguiente retroalimentación en tu cuaderno:")
        retro_text = ""
        if "Tamizado/Teoría Básica" in errores:
            retro_text += "- **Refuerzo en Tamizado:** Debo recordar que el tamizado es para separar sólidos de distintos tamaños usando una malla.\n"
        if "Filtración/Aplicación de Leyes" in errores:
            retro_text += "- **Refuerzo en Filtración:** El filtro atrapa sólidos que no se disuelven. Si el sólido es soluble, la filtración no funciona.\n"
        if not errores:
            retro_text = "¡Excelente trabajo! Has comprendido los conceptos fundamentales. Copia un resumen de los métodos en tu cuaderno como repaso."
        
        st.info(retro_text)
        st.session_state.retro_final = retro_text

# --- CIERRE Y EXPORTACIÓN ---
if st.session_state.progreso == 100:
    st.success(f"¡Felicidades {st.session_state.nombre}! Has alcanzado el nivel: {nivel_actual}")
    
    # Preparar archivo de descarga
    reporte = f"""
    REPORTE DE APRENDIZAJE - CIENCIAS NATURALES
    Estudiante: {st.session_state.nombre}
    Nota Final: {st.session_state.puntos}/5
    Elemento Alcanzado: {nivel_actual}
    
    RESUMEN DE EVALUACIÓN:
    1. Pregunta 1: {st.session_state.respuestas_finales.get('ev1')}
    2. Pregunta 2: {st.session_state.respuestas_finales.get('ev2')}
    3. Pregunta 3: {st.session_state.respuestas_finales.get('ev3')}
    
    RESPUESTAS ABIERTAS:
    - Filtración: {st.session_state.respuestas_finales.get('ab1')}
    - Tamices: {st.session_state.respuestas_finales.get('ab2')}
    
    RUTA DE FORTALECIMIENTO:
    {st.session_state.get('retro_final', 'No requerida')}
    """
    
    st.download_button(
        label="📥 Descargar mis resultados (TXT)",
        data=reporte,
        file_name=f"Resultado_{st.session_state.nombre.replace(' ', '_')}.txt",
        mime="text/plain"
    )