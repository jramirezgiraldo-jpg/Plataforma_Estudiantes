import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(page_title="OVA - Mezclas Heterogéneas", layout="centered")

# CSS personalizado para colores amigables con la concentración
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F9F9;
    }
    h1, h2, h3 {
        color: #2C5F2D;
    }
    .stButton>button {
        background-color: #97BC62;
        color: white;
        border-radius: 5px;
    }
    .alerta-pedagogica {
        background-color: #FFDE7D;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #F8B400;
        color: #333;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZACIÓN DE VARIABLES DE SESIÓN
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'progress' not in st.session_state:
    st.session_state.progress = 0.0
if 'score' not in st.session_state:
    st.session_state.score = 0
for i in range(1, 11):
    if f'act_{i}_done' not in st.session_state:
        st.session_state[f'act_{i}_done'] = False
if 'eval_submitted' not in st.session_state:
    st.session_state.eval_submitted = False

# Sistema de Gamificación
elementos = {0: "Ninguno", 1: "Hidrógeno (H)", 2: "Helio (He)", 3: "Litio (Li)", 4: "Berilio (Be)", 5: "Boro (B)"}

def update_progress():
    # Calcula el progreso basado en actividades completadas (10 actividades = 50%, Evaluación = 50%)
    acts_completed = sum(1 for i in range(1, 11) if st.session_state[f'act_{i}_done'])
    base_progress = (acts_completed / 10.0) * 0.5
    eval_progress = 0.5 if st.session_state.eval_submitted else 0.0
    st.session_state.progress = base_progress + eval_progress

# ==========================================
# GESTIÓN DE USUARIO (LOGIN)
# ==========================================
if not st.session_state.logged_in:
    st.title("🧪 Laboratorio Virtual: Descubriendo las Mezclas")
    st.write("Bienvenido a tu Objeto Virtual de Aprendizaje. Por favor, ingresa tus datos para comenzar.")
    
    with st.form("login_form"):
        nombres = st.text_input("Nombres:")
        apellidos = st.text_input("Apellidos:")
        submit_login = st.form_submit_button("Ingresar")
        
        if submit_login:
            if nombres and apellidos:
                st.session_state.student_name = f"{nombres} {apellidos}"
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Por favor, completa ambos campos.")
    st.stop() # Detiene la ejecución hasta que se loguee

# ==========================================
# BARRA SUPERIOR CONSTANTE
# ==========================================
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown(f"**Estudiante:** {st.session_state.student_name}")
with col2:
    update_progress()
    st.progress(st.session_state.progress, text="Progreso de tu aventura")
with col3:
    st.markdown(f"**Nivel:** {elementos[st.session_state.score]}")

st.divider()

# ==========================================
# 1. INICIO: OBJETIVO Y PRE-SABERES
# ==========================================
st.header("🎯 Misión de Hoy")
st.write("**Objetivo de Aprendizaje:** Identificar y clasificar mezclas heterogéneas reconociendo sus fases visibles, relacionándolas con procesos cotidianos y el trabajo en equipo.")

st.subheader("🤔 ¿Qué sabemos hasta ahora?")
pre1 = st.radio("1. Cuando mezclas agua y aceite en un vaso, ¿qué observas?", 
                ["Se mezclan completamente formando un solo líquido.", "El aceite se queda arriba y el agua abajo, se ven separados.", "El agua cambia de color pero no se separa."], index=None)
if pre1 == "El aceite se queda arriba y el agua abajo, se ven separados.":
    st.success("¡Correcto! Tienen diferentes densidades y no se unen.")
elif pre1 is not None:
    st.warning("Piénsalo bien. ¿Alguna vez has visto el caldo de un sancocho? La grasa flota.")

pre2 = st.radio("2. ¿Qué es la materia?", 
                ["Todo lo que nos rodea, tiene masa y ocupa un lugar en el espacio.", "Solo las cosas sólidas como las rocas.", "La energía que nos da el sol."], index=None)
if pre2 == "Todo lo que nos rodea, tiene masa y ocupa un lugar en el espacio.":
    st.success("¡Excelente! Todo el universo está hecho de materia.")
elif pre2 is not None:
    st.warning("Recuerda que incluso el aire o el agua son materia.")

pre3 = st.selectbox("3. En el trabajo de laboratorio o en una finca, la escucha activa ayuda a:", 
                    ["No hacer caso a los demás.", "Aprender del equipo, evitar accidentes y hacer el trabajo mejor.", "Terminar más rápido haciendo el trabajo de los demás."], index=None)
if pre3 == "Aprender del equipo, evitar accidentes y hacer el trabajo mejor.":
    st.success("¡Así es! Trabajar en equipo es fundamental en la ciencia y en la vida.")
elif pre3 is not None:
    st.warning("El respeto y la comunicación son claves para el éxito colectivo.")

st.divider()

# ==========================================
# 2. CUERPO INDUCTIVO
# ==========================================
st.header("📖 Fase Inductiva: El Mundo en Partes Visibles")

texto_inductivo = """
En nuestro día a día interactuamos con la materia en múltiples formas. La materia se clasifica en sustancias puras y mezclas. Hoy nos centraremos en un tipo especial de mezcla: las **mezclas heterogéneas**. 

Una mezcla se forma cuando unimos dos o más sustancias sin que ocurra una reacción química entre ellas; es decir, cada sustancia conserva sus propiedades originales. Lo que hace "heterogénea" a una mezcla es que sus componentes no se distribuyen de manera uniforme. Si tomas una lupa y observas con cuidado, podrás **distinguir a simple vista (o con un microscopio simple) las diferentes partes que la componen**. A cada una de estas partes diferenciables las llamamos **fases**.

Imagina un vaso con agua al que le agregamos un puñado de arena. Por más que agitemos vigorosamente, después de unos minutos de reposo, la arena se depositará en el fondo por la acción de la gravedad. En este sistema, podemos identificar claramente dos fases: una fase sólida (la arena en el fondo) y una fase líquida (el agua en la parte superior). Este es el rasgo definitorio de las mezclas heterogéneas: la falta de uniformidad.

Otro ejemplo clásico ocurre entre líquidos que no se llevan bien, como el agua y el aceite. Al intentarlos mezclar, notaremos que forman capas separadas. El aceite, siendo menos denso que el agua, flotará en la superficie. A este tipo de líquidos que no se pueden mezclar uniformemente se les conoce como inmiscibles. 

La naturaleza heterogénea de estas mezclas nos permite utilizar métodos de separación físicos muy sencillos. Por ejemplo, si queremos separar la arena del agua, podemos usar un papel filtro (filtración) o simplemente inclinar el vaso con cuidado para verter el agua (decantación). Si queremos separar el agua del aceite, podemos usar un embudo de decantación, abriendo una llave para dejar caer el líquido más denso primero.

El reconocimiento visual de las fases es el primer paso del científico para entender de qué está hecha una muestra. Al comprender las propiedades físicas de cada componente (como su tamaño, su densidad o su estado magnético), podemos ingeniar métodos para separarlos y estudiarlos individualmente.
"""
st.markdown(texto_inductivo)

# Gráfico Inductivo con Matplotlib
st.subheader("Gráfica: Composición de una Muestra de Tierra")
fig1, ax1 = plt.subplots(figsize=(6, 3))
componentes = ['Arcilla', 'Arena', 'Materia Orgánica', 'Agua/Aire']
porcentajes = [30, 40, 5, 25]
colores = ['#8B4513', '#F4A460', '#2E8B57', '#87CEEB']
ax1.barh(componentes, porcentajes, color=colores)
ax1.set_xlabel('Porcentaje en la mezcla (%)')
ax1.set_title('Fases visibles en un puñado de tierra húmeda')
st.pyplot(fig1)

st.subheader("📝 Actividades para tu Cuaderno (Fase Inductiva)")
st.write("Realiza las siguientes actividades en tu cuaderno. Cuando termines cada una, haz clic en 'Hecho'.")

def make_activity_button(act_num, text):
    if not st.session_state[f'act_{act_num}_done']:
        if st.button(f"Hecho - Actividad {act_num}"):
            st.session_state[f'act_{act_num}_done'] = True
            st.rerun()
    else:
        st.success(f"✅ Actividad {act_num} completada.")

st.write("**1.** Dibuja un vaso de precipitados con agua y aceite, coloreando y señalando las dos fases.")
make_activity_button(1, "")
st.write("**2.** Escribe en tus propias palabras la definición de 'Mezcla Heterogénea'.")
make_activity_button(2, "")
st.write("**3.** Haz una tabla con 3 ejemplos de mezclas heterogéneas que encuentres en tu cocina.")
make_activity_button(3, "")
st.write("**4.** Dibuja el proceso de filtración para separar agua y arena.")
make_activity_button(4, "")
st.write("**5.** Explica en un párrafo corto por qué el aceite flota sobre el agua (pista: usa la palabra densidad).")
make_activity_button(5, "")

st.subheader("🧠 Reto ICFES - Competencia: Indagar")
st.write("Observa el siguiente esquema generado por nuestro laboratorio de densidad:")

# Gráfico para pregunta ICFES
fig2, ax2 = plt.subplots(figsize=(3, 4))
ax2.bar([1], [20], color='gray', label='Sólido X (Fondo)')
ax2.bar([1], [30], bottom=[20], color='blue', label='Líquido Y (Medio)')
ax2.bar([1], [15], bottom=[50], color='yellow', label='Líquido Z (Arriba)')
ax2.set_xticks([])
ax2.set_ylabel("Volumen (ml)")
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
st.pyplot(fig2)

icfes_ans = st.radio("De acuerdo con la gráfica del recipiente en reposo, un estudiante concluye correctamente que:",
                     ["El Líquido Z es el más denso de todos los componentes.",
                      "El Sólido X y el Líquido Y forman una mezcla homogénea.",
                      "El Sólido X tiene la mayor densidad de la mezcla.",
                      "El Líquido Y tiene menor densidad que el Líquido Z."], index=None)

if icfes_ans:
    with st.expander("Ver Retroalimentación Detallada"):
        if icfes_ans == "El Sólido X tiene la mayor densidad de la mezcla.":
            st.success("**¡Correcto!** En una mezcla heterogénea por decantación, los materiales más densos se van al fondo por la gravedad. Como el Sólido X está en la base, es el más denso.")
        else:
            st.error("**Incorrecto.** Recuerda que la gravedad tira con más fuerza hacia abajo a los objetos con mayor masa por volumen (mayor densidad). Si Z está arriba, es el menos denso. Si X está abajo, es el más denso.")

st.divider()

# ==========================================
# 3. CUERPO DEDUCTIVO
# ==========================================
st.header("🌿 Fase Deductiva: La Química de Nuestra Finca")

texto_deductivo = """
Ahora llevemos estos conceptos de laboratorio a nuestro entorno. Si vives en la región cafetera, seguramente has escuchado sobre el proceso de "beneficio del café". ¿Sabías que todo este proceso es un enorme trabajo de separación de mezclas heterogéneas?

Cuando los recolectores traen las cerezas de café del cultivo, no traen solo granos perfectos. En los costales viene una mezcla heterogénea de cerezas maduras, granos secos, hojas, palos e insectos. El primer paso en la tolva de recibo y los tanques o sifones es usar agua. Al sumergir esta mezcla en agua, ocurre la primera separación por densidad: las hojas, palos y granos brocados (defectuosos) flotan. A estos los llamamos "flotes". Los granos maduros y densos, que son de mejor calidad, se van al fondo. ¡Acabas de ver una decantación a gran escala!

Posteriormente, la cereza pasa por la despulpadora. Aquí, mediante fuerza mecánica, se separa la pulpa (la cáscara roja) de la semilla cubierta por el mucílago. En este punto, tenemos otra mezcla: pulpa por un lado y grano baboso por el otro. 

Luego viene la fase de fermentación y lavado. El mucílago es una capa dulce y gelatinosa pegada al grano. En los tanques, gracias a microorganismos naturales y luego con la ayuda de agua limpia, se "lava" el café. El agua arrastra el mucílago degradado, separando la fase líquida (aguas mieles) del grano sólido (café pergamino húmedo). 

En la finca cafetera, el trabajo en equipo y la escucha activa son esenciales. Imagina si el encargado del lavado no escucha las instrucciones del administrador sobre cuánto tiempo dejar fermentando el café; toda la mezcla podría arruinarse. De igual manera, en el laboratorio escolar de ciencias, escuchar a tu equipo, respetar las ideas del otro y seguir las instrucciones paso a paso garantiza que nuestros experimentos con mezclas sean seguros y exitosos.
"""
st.markdown(texto_deductivo)

# Gráfico Deductivo con Matplotlib
st.subheader("Gráfica: Componentes de una cereza de café madura")
fig3, ax3 = plt.subplots()
labels_cafe = ['Grano (Pergamino y Almendra)', 'Pulpa', 'Mucílago']
sizes_cafe = [40, 40, 20]
colors_cafe = ['#E6C280', '#D32F2F', '#FFF9C4']
ax3.pie(sizes_cafe, labels=labels_cafe, colors=colors_cafe, autopct='%1.1f%%', startangle=90)
ax3.axis('equal') 
st.pyplot(fig3)

st.subheader("📝 Actividades para tu Cuaderno (Fase Deductiva)")
st.write("**6.** Dibuja un tanque sifón de una finca cafetera mostrando los 'flotes' (hojas, granos malos) arriba y los granos buenos abajo.")
make_activity_button(6, "")
st.write("**7.** Escribe qué método de separación físico se utiliza cuando el agua arrastra el mucílago dejando el grano limpio.")
make_activity_button(7, "")
st.write("**8.** Explica en dos líneas por qué el trabajo en la finca es un ejemplo de manejo de mezclas heterogéneas.")
make_activity_button(8, "")
st.write("**9.** Redacta un pequeño párrafo sobre la importancia de la 'escucha activa' al hacer un trabajo en grupo con tus compañeros.")
make_activity_button(9, "")
st.write("**10.** Pregunta a alguien en tu casa si conoce otra parte del proceso del café donde se separen cosas y anótalo.")
make_activity_button(10, "")

st.divider()

# ==========================================
# 4. EVALUACIÓN FINAL
# ==========================================
st.header("📝 Evaluación Final y Ruta de Fortalecimiento")

with st.form("eval_form"):
    st.subheader("Preguntas de Selección Múltiple")
    q1 = st.radio("1. (Inductivo) Si observamos una ensalada de frutas, estamos frente a:", ["Mezcla Homogénea", "Sustancia Pura", "Mezcla Heterogénea", "Elemento Químico"])
    q2 = st.radio("2. (Inductivo) ¿Cuál de las siguientes opciones describe mejor a las 'fases' en una mezcla?", ["Los colores que cambian con la luz.", "Las partes visibles y diferenciables de la mezcla.", "Los gases invisibles en el aire.", "El tiempo que tarda en mezclarse."])
    q3 = st.radio("3. (Deductivo) En el beneficio del café, cuando se separan los 'flotes', se está aplicando el principio físico de:", ["Solubilidad", "Magnetismo", "Punto de Ebullición", "Densidad"])
    q4 = st.radio("4. (Deductivo) ¿Qué componentes se separan principalmente en la máquina despulpadora?", ["Agua y Aceite", "Pulpa y Grano con mucílago", "Tierra y Agua", "Hojas y Palos"])
    q5 = st.radio("5. (Transversal) ¿Por qué la escucha activa previene accidentes en un laboratorio o finca?", ["Porque mejora la audición física.", "Porque permite recibir y entender instrucciones de seguridad claras del equipo.", "Porque hace que el trabajo sea más silencioso.", "No previene accidentes."])
    
    st.subheader("Preguntas Abiertas")
    st.caption("Asegúrate de responder con argumentos (mínimo 10 palabras por respuesta).")
    open1 = st.text_area("A. Explica con tus palabras la diferencia entre una mezcla homogénea y una heterogénea.")
    open2 = st.text_area("B. Describe cómo separarías una mezcla de arena, agua y rocas grandes.")
    open3 = st.text_area("C. ¿Por qué crees que el agua es tan importante en el proceso del lavado del café?")
    open4 = st.text_area("D. Relata una situación donde el trabajo en equipo fue fundamental para resolver un problema.")
    open5 = st.text_area("E. ¿Qué fue lo que más te gustó aprender en esta unidad?")
    
    submit_eval = st.form_submit_button("Entregar Evaluación")

# ==========================================
# 5. SISTEMA DE RETROALIMENTACIÓN
# ==========================================
if submit_eval:
    # Validación de palabras en preguntas abiertas
    open_answers = [open1, open2, open3, open4, open5]
    invalid_length = False
    for i, ans in enumerate(open_answers):
        if len(ans.split()) < 10:
            st.warning(f"Tu respuesta a la pregunta abierta {chr(65+i)} es muy corta. ¡Desarrolla más tu idea! (Mínimo 10 palabras).")
            invalid_length = True
            
    if invalid_length:
        st.stop()
        
    st.session_state.eval_submitted = True
    
    # Calificación
    correct_answers = {
        'q1': "Mezcla Heterogénea",
        'q2': "Las partes visibles y diferenciables de la mezcla.",
        'q3': "Densidad",
        'q4': "Pulpa y Grano con mucílago",
        'q5': "Porque permite recibir y entender instrucciones de seguridad claras del equipo."
    }
    
    score = 0
    errores_inductivos = False
    errores_deductivos = False
    
    if q1 == correct_answers['q1']: score += 1
    else: errores_inductivos = True
        
    if q2 == correct_answers['q2']: score += 1
    else: errores_inductivos = True
        
    if q3 == correct_answers['q3']: score += 1
    else: errores_deductivos = True
        
    if q4 == correct_answers['q4']: score += 1
    else: errores_deductivos = True
        
    if q5 == correct_answers['q5']: score += 1
    
    st.session_state.score = score
    st.success(f"¡Evaluación completada! Tu puntaje es: {score}/5. Has alcanzado el nivel: {elementos[score]}")
    
    # Generación de la Ruta de Fortalecimiento
    st.markdown('<div class="alerta-pedagogica">⚠️ De acuerdo a tus resultados, debes copiar la siguiente retroalimentación en tu cuaderno para fortalecer tus debilidades.</div>', unsafe_allow_html=True)
    
    feedback_text = f"--- RUTA DE FORTALECIMIENTO PARA {st.session_state.student_name.upper()} ---\n\n"
    
    if score == 5:
        feedback_text += "¡Felicidades! Tienes un dominio excelente de las mezclas heterogéneas tanto en la teoría como en su aplicación en nuestra región cafetera. Eres un líder de laboratorio en potencia. Sigue practicando la escucha activa con tu equipo.\n"
    else:
        if errores_inductivos:
            feedback_text += "🔬 REFUERZO TEÓRICO (FASE INDUCTIVA):\nHas presentado dudas en los conceptos básicos. Recuerda copiar esto en tu cuaderno: Las mezclas heterogéneas son aquellas donde podemos ver sus partes (fases) a simple vista, como en el agua y el aceite, o en una ensalada. Sus componentes no se unen íntimamente y cada uno conserva sus características, lo que nos permite separarlos fácilmente.\n\n"
        if errores_deductivos:
            feedback_text += "🌱 REFUERZO APLICADO (FASE DEDUCTIVA):\nHubo confusiones al aplicar la ciencia en nuestro entorno. Copia esto en tu cuaderno: El beneficio del café es un gran sistema de separación de mezclas. Al usar agua en los tanques, aplicamos el concepto de 'densidad', permitiendo que los elementos livianos (flotes) se separen de los granos densos y buenos. La ciencia está presente en el campo.\n\n"
            
    st.code(feedback_text, language='markdown')
    
    # ==========================================
    # 6. CIERRE Y EXPORTACIÓN
    # ==========================================
    st.header("💾 Exportar Resultados")
    
    reporte_final = f"""REPORTE DE LABORATORIO VIRTUAL
Estudiante: {st.session_state.student_name}
Tema: Mezclas Heterogéneas
Nivel Gamificación Alcanzado: {elementos[score]}
Puntaje de Selección Múltiple: {score}/5

RESPUESTAS ABIERTAS:
A: {open1}
B: {open2}
C: {open3}
D: {open4}
E: {open5}

{feedback_text}
"""
    
    st.download_button(
        label="Descargar Reporte (.txt) para el Profesor",
        data=reporte_final,
        file_name=f"Reporte_Mezclas_{st.session_state.student_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )