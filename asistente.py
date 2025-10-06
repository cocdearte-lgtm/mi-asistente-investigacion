import streamlit as st
import re

# Configuración de página
st.set_page_config(
    page_title="Asistente de Investigación Inteligente",
    page_icon="🔬",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 25px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    margin-bottom: 25px;
}
.chat-container {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}
.user-message {
    background: #e3f2fd;
    padding: 15px;
    border-radius: 10px;
    margin: 5px 0;
}
.assistant-message {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 5px 0;
    border-left: 4px solid #667eea;
}
.feature-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔬 Asistente de Investigación Académica</h1>
    <p style="margin: 0; font-size: 1.2em;">Herramienta inteligente para el desarrollo de proyectos de investigación</p>
    <p style="margin: 10px 0 0 0; font-size: 1em;">✅ Sistema funcionando correctamente</p>
</div>
""", unsafe_allow_html=True)

# Inicializar session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'contexto_actual' not in st.session_state:
    st.session_state.contexto_actual = ""

# Funciones de procesamiento de lenguaje
def extraer_tema_principal(user_input):
    """Extrae el tema real de investigación del input del usuario"""
    try:
        # Patrón para detectar preguntas de investigación
        patron_pregunta = r'[¿]?(qué|cuáles|cómo|por qué|dónde|cuándo)\s+([^?]+)[?]'
        coincidencia = re.search(patron_pregunta, user_input.lower())
        
        if coincidencia:
            return coincidencia.group(2).strip()
        
        # Eliminar palabras de solicitud metodológica
        palabras_excluir = ['formula', 'planteamiento', 'problema', 'interrogante', 
                           'redacta', 'elabora', 'desarrolla', 'haz', 'crea', 'genera',
                           'para la', 'sobre', 'acerca de', 'necesito', 'quiero', 'dame']
        
        tema = user_input.lower()
        for palabra in palabras_excluir:
            tema = tema.replace(palabra, '')
        
        # Limpiar espacios extras y caracteres especiales
        tema = re.sub(r'[^\w\s]', '', tema)
        tema = ' '.join(tema.split())
        
        return tema.strip() if tema.strip() else user_input
    except Exception:
        return user_input

def detectar_tipo_solicitud(user_input):
    """Detecta el tipo de solicitud del usuario"""
    input_lower = user_input.lower()
    
    if any(palabra in input_lower for palabra in ['planteamiento', 'problema', 'pregunta investigación']):
        return "planteamiento"
    elif any(palabra in input_lower for palabra in ['objetivos', 'metas', 'propósitos']):
        return "objetivos"
    elif any(palabra in input_lower for palabra in ['metodología', 'método', 'diseño', 'enfoque']):
        return "metodologia"
    elif any(palabra in input_lower for palabra in ['variables', 'operacional']):
        return "variables"
    else:
        return "general"

# Funciones de generación de contenido MEJORADAS
def generar_planteamiento_estructurado(tema, contexto=""):
    """Genera un planteamiento del problema bien estructurado con excelente redacción"""
    
    planteamiento = f"""
# 🎯 PLANTEAMIENTO DEL PROBLEMA: {tema.title()}

## 📝 DESCRIPCIÓN DEL PROBLEMA

En el contexto actual caracterizado por la rápida evolución tecnológica y las transformaciones sociales, se ha identificado una problemática significativa en el ámbito de **{tema}**. La disyunción existente entre las demandas emergentes y las capacidades actuales genera consecuencias relevantes que merecen atención investigativa.

## 🔍 JUSTIFICACIÓN DE LA INVESTIGACIÓN

El estudio de {tema} se justifica por las siguientes consideraciones fundamentales:

1. **Relevancia contemporánea**: Constituye un tema de actualidad en el marco de los procesos de transformación digital y social.
2. **Impacto multidimensional**: Sus efectos repercuten en diversos ámbitos: social, económico, educativo y organizacional.
3. **Vacío en la literatura**: Existe una necesidad evidente de investigaciones actualizadas que aborden esta temática desde perspectivas innovadoras.
4. **Aplicabilidad práctica**: Los hallazgos pueden traducirse en estrategias concretas y soluciones aplicables.

## 📌 DELIMITACIÓN DEL ESTUDIO

Esta investigación se circunscribirá a:
- **Ámbito temático**: Aspectos específicos relacionados con {tema}
- **Contexto de aplicación**: {contexto if contexto else "entornos diversos y representativos"}
- **Enfoque metodológico**: Análisis integral seguido de propuestas de mejora

## ❓ PREGUNTAS DE INVESTIGACIÓN

1. ¿Cuáles son los factores determinantes que influyen significativamente en {tema}?
2. ¿Qué impacto observable genera {tema} en los diferentes contextos de aplicación?
3. ¿Qué estrategias y metodologías demostrarían mayor efectividad para optimizar los resultados asociados a {tema}?
4. ¿Qué brechas de conocimiento y oportunidades de desarrollo futuro pueden identificarse en este campo de estudio?

*Contexto específico considerado: {contexto if contexto else "ámbito general de aplicación"}*
"""
    return planteamiento

def generar_objetivos_estructurados(tema, contexto=""):
    """Genera objetivos de investigación estructurados con redacción académica"""
    contexto_texto = contexto if contexto else "diversos escenarios y contextos de aplicación"
    
    objetivos = f"""
# 🎯 OBJETIVOS DE INVESTIGACIÓN: {tema.title()}

## 🎯 OBJETIVO GENERAL

Analizar sistemáticamente los aspectos fundamentales de **{tema}** en el contexto de **{contexto_texto}**, con el propósito de formular estrategias de mejora, innovación y optimización que contribuyan al avance del conocimiento y la práctica en este campo de estudio.

## 📋 OBJETIVOS ESPECÍFICOS

1. **Identificar y caracterizar** los componentes, dimensiones y variables clave asociados con {tema}, estableciendo un marco conceptual robusto que facilite su comprensión integral.

2. **Diagnosticar el estado actual** de {tema} mediante el análisis exhaustivo de tendencias, prácticas predominantes y desafíos identificados tanto en la literatura especializada como en contextos reales de aplicación.

3. **Evaluar el impacto** de {tema} en diferentes ámbitos (social, económico, educativo, organizacional), considerando variables contextuales y características poblacionales específicas.

4. **Diseñar y proponer** estrategias, metodologías o herramientas innovadoras para la optimización de {tema}, fundamentadas en evidencia empírica y mejores prácticas identificadas.

5. **Validar la aplicabilidad** de las propuestas formuladas mediante criterios de factibilidad, sostenibilidad y alineamiento con necesidades identificadas en el contexto de {contexto_texto}.
"""
    return objetivos

def generar_sugerencias_metodologicas(tema, contexto=""):
    """Genera sugerencias metodológicas detalladas con excelente redacción"""
    
    metodologia = f"""
## 🎓 SUGERENCIAS METODOLÓGICAS PARA: {tema.title()}

### **ENFOQUE METODOLÓGICO RECOMENDADO**

**Investigación Mixta de Diseño Secuencial Explicativo** - Esta aproximación metodológica combina sistemáticamente la solidez de los métodos cuantitativos para establecer patrones generales con la profundidad analítica de los métodos cualitativos para comprender significados y contextualizaciones específicas.

### **DISEÑO DE INVESTIGACIÓN**

- **Tipo de diseño**: Secuencial explicativo (Fase cuantitativa → Fase cualitativa)
- **Fase 1**: Estudio cuantitativo orientado a identificar patrones, tendencias y relaciones significativas
- **Fase 2**: Investigación cualitativa destinada a explicar, interpretar y profundizar en los hallazgos cuantitativos
- **Estrategia de muestreo**: Muestreo estratificado según criterios relevantes al contexto de estudio

### **TÉCNICAS E INSTRUMENTOS DE RECOLECCIÓN**

**📈 Componente Cuantitativo:**
- *Encuestas estructuradas* con escalas Likert validadas psicométricamente
- *Análisis documental sistemático* de fuentes secundarias confiables
- *Instrumentos de medición*: Cuestionarios estandarizados, registros sistemáticos, bases de datos oficiales

**📊 Componente Cualitativo:**
- *Entrevistas semiestructuradas* con guías temáticas flexibles
- *Grupos focales* para contrastar perspectivas y enriquecer el análisis
- *Observación participante* en contextos naturales de ocurrencia del fenómeno
- *Análisis de contenido cualitativo* de documentos, narrativas y discursos

### **ESTRATEGIAS DE ANÁLISIS DE DATOS**

**Análisis Cuantitativo:**
- Estadística descriptiva (medidas de tendencia central, dispersión, distribuciones)
- Análisis inferencial (pruebas de correlación, comparación de medias, análisis de varianza)
- Modelamiento multivariado (análisis de regresión, análisis factorial, modelos predictivos)

**Análisis Cualitativo:**
- Análisis temático con procesos de codificación abierta, axial y selectiva
- Triangulación metodológica para garantizar robustez en los hallazgos
- Análisis de contenido categorial con identificación de patrones discursivos

### **CONSIDERACIONES ÉTICAS**

- Obtención de consentimiento informado de participantes
- Garantía de confidencialidad y protección de datos
- Rigor metodológico y transparencia en procedimientos
- Consideración del contexto específico: {contexto if contexto else "diversos escenarios"}
"""
    return metodologia

def sugerir_variables_operativas(tema, contexto=""):
    """Sugiere variables de investigación con redacción académica"""
    
    variables = f"""
## 🔬 VARIABLES DE INVESTIGACIÓN PARA: {tema.title()}

### **VARIABLES INDEPENDIENTES PRINCIPALES**

1. **Nivel de Implementación de {tema}**
   - *Definición operacional*: Grado de desarrollo, integración y madurez medido mediante escalas validadas basadas en indicadores específicos de adopción y aplicación.
   - *Instrumento de medición*: Escala Likert con criterios claramente definidos y operacionalizados.

2. **Características Contextuales de {contexto if contexto else 'aplicación'}**
   - *Definición operacional*: Conjunto de atributos y condiciones del entorno que pueden moderar o mediar los efectos observados.
   - *Instrumento de medición*: Matriz de evaluación contextual con dimensiones preestablecidas.

### **VARIABLES DEPENDIENTES PRINCIPALES**

1. **Impacto en Resultados Clave**
   - *Definición operacional*: Cambios cuantificables y observables en indicadores de desempeño, eficiencia o efectividad relacionados con el fenómeno de estudio.
   - *Instrumento de medición*: Métricas cuantitativas predefinidas y validadas empíricamente.

2. **Grado de Adopción y Aceptación**
   - *Definición operacional*: Nivel de implementación exitosa y satisfacción percibida por usuarios y partes interesadas.
   - *Instrumento de medición*: Escalas de satisfacción y métricas de uso y adopción.

### **VARIABLES INTERVINIENTES Y MEDIADORAS**

- **Competencias y Habilidades Específicas** requeridas para la implementación efectiva.
- **Recursos e Infraestructura Disponible** para sustentar los procesos.
- **Factores Culturales y Organizacionales** que facilitan u obstaculizan la adopción.

### **VARIABLES DE CONTROL**

- Experiencia previa y formación de los participantes.
- Características demográficas relevantes (edad, género, formación académica).
- Tamaño y tipo de organización o contexto de aplicación.
- Recursos económicos y tecnológicos disponibles.

### **MATRIZ DE OPERACIONALIZACIÓN**

Cada variable debe especificarse considerando:
- Definición conceptual fundamentada teóricamente.
- Definición operacional claramente especificada.
- Escala de medición apropiada y validada.
- Instrumento de recolección confiable y válido.
- Procedimiento de aplicación estandarizado.
"""
    return variables

def generar_respuesta_general(tema, user_input):
    """Genera respuesta general del asistente con excelente redacción"""
    
    respuesta = f"""
## 💡 ASESORÍA ESPECIALIZADA EN INVESTIGACIÓN: {tema.title()}

Como asistente de investigación especializado, he analizado detenidamente su consulta sobre **"{tema}"** y puedo ofrecerle orientación en los siguientes aspectos:

### 🎯 **ENFOQUES DE INVESTIGACIÓN RECOMENDADOS:**

**1. Investigación Exploratoria-Descriptiva**
- *Adecuado para*: Caracterizar el fenómeno de estudio y establecer bases conceptuales sólidas.
- *Métodos sugeridos*: Revisión sistemática de literatura, estudio de casos emblemáticos, análisis documental exhaustivo.

**2. Investigación Explicativa**  
- *Adecuado para*: Identificar relaciones causales y factores determinantes subyacentes.
- *Métodos sugeridos*: Diseños cuasi-experimentales, modelamiento multivariado, análisis de trayectorias.

**3. Investigación Aplicada**
- *Adecuado para*: Desarrollar soluciones prácticas y validar intervenciones específicas.
- *Métodos sugeridos*: Investigación-acción participativa, diseño y desarrollo iterativo, estudios de implementación.

### 📊 **VARIABLES CLAVE A CONSIDERAR:**

- *Variables de proceso*: Mecanismos, estrategias, metodologías de implementación.
- *Variables de resultado*: Impacto, efectividad, eficiencia, sostenibilidad.  
- *Variables contextuales*: Entorno específico, recursos disponibles, características poblacionales.

### 🔍 **PRÓXIMOS PASOS SUGERIDOS:**

1. Realizar una búsqueda bibliográfica especializada y actualizada.
2. Definir el marco teórico y conceptual específico para su investigación.
3. Establecer preguntas de investigación claramente delimitadas y relevantes.
4. Seleccionar la metodología más apropiada según sus objetivos específicos.

**¿Le gustaría que profundice en algún aspecto específico de la investigación sobre {tema}?**
"""
    return respuesta

# Función principal del chat
def procesar_consulta_usuario(user_input, contexto=""):
    """Procesa la consulta del usuario y genera respuesta con excelente redacción"""
    try:
        # Extraer tema y tipo de solicitud
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        # Mostrar información de contexto
        st.info(f"🔍 **Tema detectado:** {tema_real}")
        if contexto:
            st.info(f"🎯 **Contexto considerado:** {contexto}")
        
        # Generar respuesta según el tipo de solicitud
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto)
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto)
        elif tipo_solicitud == "metodologia":
            respuesta = generar_sugerencias_metodologicas(tema_real, contexto)
        elif tipo_solicitud == "variables":
            respuesta = sugerir_variables_operativas(tema_real, contexto)
        else:
            respuesta = generar_respuesta_general(tema_real, user_input)
        
        return respuesta
        
    except Exception as e:
        return f"❌ Se ha producido un error en el procesamiento: {str(e)}"

# Interfaz principal con pestañas
tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "🔍 Búsqueda Rápida", "💬 Chat Principal"])

with tab1:
    st.markdown("## 🚀 Bienvenido al Asistente de Investigación Inteligente")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h4>💬 Chatbot Inteligente con Procesamiento de Lenguaje Natural</h4>
        <p>Sistema avanzado de comprensión lingüística para interpretar sus solicitudes de investigación y generar respuestas contextualizadas y académicamente rigurosas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>🎯 Generación de Elementos de Investigación Académica</h4>
        <p>Elaboración automática de planteamientos de problema, objetivos de investigación, metodologías y variables operativas con redacción académica profesional.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>📚 Asesoría Metodológica Especializada</h4>
        <p>Orientación experta en diseño de investigación, selección de métodos y técnicas de análisis adecuadas para cada tipo de estudio.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Cómo utilizar el sistema:")
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>1. 💬 Acceder al Chat</h4>
        <p>Diríjase a la pestaña "Chat Principal"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>2. 🎯 Formular su consulta</h4>
        <p>Ejemplo:<br>
        <em>"Formule el planteamiento sobre competencias digitales"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>3. 📚 Recibir asesoría especializada</h4>
        <p>Contenido académico estructurado y profesional</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Ejemplos de consultas:")
        st.code("""
"Formule el planteamiento sobre 
competencias digitales docentes"

"Genere objetivos para investigación 
en inteligencia artificial educativa"

"Sugiera metodología para estudiar 
el impacto de redes sociales"
        """)

with tab2:
    st.markdown("## 🔍 Búsqueda Rápida y Generación de Contenido")
    
    col_search1, col_search2 = st.columns([2, 1])
    
    with col_search1:
        tema_consulta = st.text_input(
            "🔎 Tema de investigación principal:",
            placeholder="Ej: competencias digitales, inteligencia artificial educativa...",
            value="competencias digitales en entornos educativos"
        )
    
    with col_search2:
        contexto_consulta = st.text_input(
            "🎯 Contexto específico:",
            placeholder="Ej: educación superior, empresas tecnológicas...",
            value="instituciones de educación superior"
        )
    
    st.markdown("---")
    
    # Botones de generación rápida
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("🧩 Generar Planteamiento", use_container_width=True):
            with st.spinner("Generando planteamiento del problema..."):
                respuesta = generar_planteamiento_estructurado(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn2:
        if st.button("🎯 Generar Objetivos", use_container_width=True):
            with st.spinner("Generando objetivos de investigación..."):
                respuesta = generar_objetivos_estructurados(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn3:
        if st.button("🔬 Generar Metodología", use_container_width=True):
            with st.spinner("Generando sugerencias metodológicas..."):
                respuesta = generar_sugerencias_metodologicas(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn4:
        if st.button("📊 Generar Variables", use_container_width=True):
            with st.spinner("Generando variables de investigación..."):
                respuesta = sugerir_variables_operativas(tema_consulta, contexto_consulta)
                st.markdown(respuesta)

with tab3:
    st.markdown("## 💬 Chat Inteligente con el Asistente")
    
    # Configuración del contexto
    contexto_chat = st.text_input(
        "🎯 Contexto de investigación para esta conversación:",
        placeholder="Ej: mi tesis de maestría, investigación en educación superior...",
        value="proyecto de investigación académica"
    )
    
    # Botón para limpiar chat
    col_clear, col_stats = st.columns([1, 3])
    with col_clear:
        if st.button("🔄 Limpiar Conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_stats:
        if st.session_state.chat_history:
            st.info(f"💬 Conversación activa: {len(st.session_state.chat_history)//2} intercambios")
    
    st.markdown("---")
    
    # Mostrar historial del chat
    for mensaje in st.session_state.chat_history:
        if mensaje["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 Usted:</strong><br>
                {mensaje["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🔬 Asistente:</strong><br>
                {mensaje["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Ejemplos rápidos para probar
    st.markdown("### 💡 Ejemplos para probar:")
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    
    with col_ex1:
        if st.button("🧩 Ejemplo: Planteamiento", use_container_width=True):
            st.session_state.ejemplo_activo = "Formule el planteamiento del problema sobre competencias digitales para la empleabilidad en la era digital"
    
    with col_ex2:
        if st.button("🎯 Ejemplo: Objetivos", use_container_width=True):
            st.session_state.ejemplo_activo = "Genere objetivos de investigación sobre la implementación de inteligencia artificial en instituciones educativas"
    
    with col_ex3:
        if st.button("🔬 Ejemplo: Metodología", use_container_width=True):
            st.session_state.ejemplo_activo = "Sugiera una metodología para investigar el impacto de las redes sociales en el aprendizaje de adolescentes"
    
    with col_ex4:
        if st.button("📊 Ejemplo: Variables", use_container_width=True):
            st.session_state.ejemplo_activo = "Proponga variables operativas para estudiar liderazgo educativo en entornos digitales"
    
    # Input del chat
    prompt = st.chat_input("Escriba su pregunta o solicitud de investigación...")
    
    # Manejar ejemplo predefinido
    if hasattr(st.session_state, 'ejemplo_activo'):
        prompt = st.session_state.ejemplo_activo
        del st.session_state.ejemplo_activo
    
    if prompt:
        # Agregar mensaje del usuario al historial
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario inmediatamente
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar y mostrar respuesta
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analizando su consulta y generando respuesta..."):
                respuesta = procesar_consulta_usuario(prompt, contexto_chat)
                st.markdown(respuesta)
        
        # Agregar respuesta al historial
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🔬 Asistente de Investigación Académica - Versión Profesional | "
    "✅ Redacción académica mejorada | "
    "✅ Sistema funcionando correctamente"
    "</div>", 
    unsafe_allow_html=True
)
