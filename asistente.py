import streamlit as st
import re
import openai
import os

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
.ia-feature {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔬 Asistente de Investigación Académica Inteligente</h1>
    <p style="margin: 0; font-size: 1.2em;">Herramienta con IA para el desarrollo de proyectos de investigación</p>
    <p style="margin: 10px 0 0 0; font-size: 1em;">🤖 Con tecnología GPT-4 | ✅ Sistema funcionando correctamente</p>
</div>
""", unsafe_allow_html=True)

# Definición de prompt base para el asistente IA
PROMPT_BASE = """
Eres un investigador académico senior especializado en metodología de investigación. Sigue ESTRICTAMENTE estas directivas:

1. ESTRUCTURA: Respetar exactamente la estructura solicitada (párrafos, longitud, formato)
2. EXTENSIÓN: Cumplir con el número exacto de párrafos y líneas solicitadas
3. CITAS: Incluir referencias verificables con autores reales, años y fuentes
4. COHERENCIA: Mantener hilo conductor académico entre todos los párrafos
5. PROFUNDIDAD: Desarrollar cada punto con rigor académico y precisión conceptual

FORMATO OBLIGATORIO:
- Cada párrafo: 8-10 líneas de contenido sustancial
- Citas en formato APA con autores verificables
- Lenguaje académico formal pero claro
- Numeración de párrafos cuando se solicite
"""

Consulta o instrucción del usuario:
"""

# Función para generar la respuesta del agente IA
def generar_respuesta_ia(mensaje_usuario, contexto=""):
    prompt_completo = PROMPT_BASE + mensaje_usuario
    if contexto:
        prompt_completo += f"\n\nContexto adicional: {contexto}"
    
    try:
        # Nota: Necesitarás configurar tu API key de OpenAI
        # openai.api_key = st.secrets["OPENAI_API_KEY"]
        
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",  # Puedes cambiar a "gpt-3.5-turbo" si prefieres
            messages=[
                {"role": "system", "content": PROMPT_BASE},
                {"role": "user", "content": mensaje_usuario}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return respuesta['choices'][0]['message']['content']
    except Exception as e:
       
        return f"""**Respuesta del Asistente IA:**

Parece que hay un problema con la conexión a la API de OpenAI. Error: {str(e)}

**Mientras tanto, aquí tienes una guía general:**

Para consultas sobre '{mensaje_usuario}', te recomiendo:

**Fuentes académicas sugeridas:**
- Google Scholar para búsqueda de artículos científicos
- Scopus y Web of Science para literatura especializada
- ScienceDirect y JSTOR para acceso a textos completos

**Enfoque de investigación recomendado:**
1. Realiza una revisión sistemática de literatura
2. Identifica los autores más citados en el área
3. Analiza las metodologías predominantes
4. Establece tu marco teórico y conceptual

**Próximos pasos:**
- Define claramente tu pregunta de investigación
- Selecciona la metodología apropiada
- Establece tus criterios de inclusión/exclusión
- Planifica tu estrategia de búsqueda bibliográfica

*Para usar la funcionalidad completa de IA, necesitarás configurar una API key de OpenAI.*"""

**Mientras tanto, aquí tienes una guía general:**

Para consultas sobre '{mensaje_usuario}', te recomiendo:

📚 **Fuentes académicas sugeridas:**
- Google Scholar para búsqueda de artículos científicos
- Scopus y Web of Science para literatura especializada
- ScienceDirect y JSTOR para acceso a textos completos

🔍 **Enfoque de investigación recomendado:**
1. Realiza una revisión sistemática de literatura
2. Identifica los autores más citados en el área
3. Analiza las metodologías predominantes
4. Establece tu marco teórico y conceptual

💡 **Próximos pasos:**
- Define claramente tu pregunta de investigación
- Selecciona la metodología apropiada
- Establece tus criterios de inclusión/exclusión
- Planifica tu estrategia de búsqueda bibliográfica

*Para usar la funcionalidad completa de IA, necesitarás configurar una API key de OpenAI.*"""

# Inicializar session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'contexto_actual' not in st.session_state:
    st.session_state.contexto_actual = ""
if 'modo_ia' not in st.session_state:
    st.session_state.modo_ia = False

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

# Función principal del chat MEJORADA con IA
def procesar_consulta_usuario(user_input, contexto="", usar_ia=False):
    """Procesa la consulta del usuario y genera respuesta con excelente redacción"""
    try:
        # Extraer tema y tipo de solicitud
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        # Mostrar información de contexto
        st.info(f"🔍 **Tema detectado:** {tema_real}")
        if contexto:
            st.info(f"🎯 **Contexto considerado:** {contexto}")
        if usar_ia:
            st.success("🤖 **Modo IA activado** - Generando respuesta con inteligencia artificial")
        
        # Si el modo IA está activado, usar la función de IA
        if usar_ia:
            with st.spinner("🤖 Consultando con IA..."):
                respuesta = generar_respuesta_ia(user_input, contexto)
                return respuesta
        
        # Si no, usar las funciones predefinidas
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto)
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto)
        elif tipo_solicitud == "metodologia":
            respuesta = f"""
## 🎓 SUGERENCIAS METODOLÓGICAS PARA: {tema_real.title()}

### **ENFOQUE METODOLÓGICO RECOMENDADO**
**Investigación Mixta de Diseño Secuencial Explicativo** - Combina métodos cuantitativos y cualitativos para un análisis comprehensivo.

### **DISEÑO DE INVESTIGACIÓN**
- **Tipo**: Secuencial explicativo
- **Fase 1**: Análisis cuantitativo (encuestas, datos secundarios)
- **Fase 2**: Profundización cualitativa (entrevistas, estudios de caso)

### **TÉCNICAS DE RECOLECCIÓN**
- 📊 Encuestas con escalas Likert validadas
- 🎤 Entrevistas semiestructuradas
- 📑 Análisis documental sistemático
- 👥 Grupos focales para triangulación

*Contexto: {contexto if contexto else "diversos escenarios de aplicación"}*
"""
        elif tipo_solicitud == "variables":
            respuesta = f"""
## 🔬 VARIABLES DE INVESTIGACIÓN PARA: {tema_real.title()}

### **VARIABLES INDEPENDIENTES**
- Factores influyentes en {tema_real}
- Estrategias implementadas
- Características contextuales

### **VARIABLES DEPENDIENTES**
- Resultados observables
- Impacto medible
- Efectividad de intervenciones

### **VARIABLES DE CONTROL**
- Contexto específico
- Características poblacionales
- Recursos disponibles

*Contexto: {contexto}*
"""
        else:
            respuesta = f"""
## 💡 ASESORÍA ESPECIALIZADA EN INVESTIGACIÓN: {tema_real.title()}

He analizado su consulta sobre **"{tema_real}"** y puedo ofrecerle orientación en:

### 🎯 **ENFOQUES RECOMENDADOS:**
- **Investigación exploratoria**: Para caracterizar el fenómeno
- **Investigación explicativa**: Para identificar relaciones causales
- **Investigación aplicada**: Para desarrollar soluciones prácticas

### 📊 **ASPECTOS CLAVE:**
- Definición clara del problema de investigación
- Establecimiento de preguntas guía
- Selección de metodología apropiada
- Operacionalización de variables

### 🔍 **PRÓXIMOS PASOS:**
1. Búsqueda bibliográfica especializada
2. Delimitación del marco teórico-conceptual
3. Formulación de hipótesis o preguntas
4. Diseño metodológico detallado

**¿Le gustaría que profundice en algún aspecto específico?**
"""
        
        return respuesta
        
    except Exception as e:
        return f"❌ Se ha producido un error en el procesamiento: {str(e)}"

# Interfaz principal con pestañas
tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "🔍 Búsqueda Rápida", "💬 Chat Inteligente"])

with tab1:
    st.markdown("## 🚀 Bienvenido al Asistente de Investigación con IA")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="ia-feature">
        <h4>🤖 ASISTENTE CON INTELIGENCIA ARTIFICIAL</h4>
        <p>Ahora potenciado con GPT-4 para respuestas más inteligentes, contextualizadas y fundamentadas académicamente.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        <h4>1. 💬 Acceder al Chat Inteligente</h4>
        <p>Diríjase a la pestaña "Chat Inteligente"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>2. 🤖 Activar el modo IA (Opcional)</h4>
        <p>Active el interruptor para respuestas con inteligencia artificial</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>3. 🎯 Formular su consulta</h4>
        <p>Ejemplo:<br>
        <em>"Analice las tendencias actuales en educación virtual"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Ejemplos de consultas con IA:")
        st.code("""
"Revise la literatura sobre competencias 
digitales docentes y sugiera referencias APA"

"Analice metodologías mixtas para estudiar 
el impacto de redes sociales en adolescentes"

"Proponga un marco teórico para investigación 
en inteligencia artificial educativa"
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
                respuesta = f"""
## 🎓 SUGERENCIAS METODOLÓGICAS PARA: {tema_consulta.title()}

### **ENFOQUE RECOMENDADO**
Investigación mixta con diseño secuencial explicativo.

### **TÉCNICAS DE RECOLECCIÓN**
- Encuestas cuantitativas
- Entrevistas cualitativas
- Análisis documental
- Observación sistemática

*Contexto: {contexto_consulta}*
"""
                st.markdown(respuesta)
    
    with col_btn4:
        if st.button("📊 Generar Variables", use_container_width=True):
            with st.spinner("Generando variables de investigación..."):
                respuesta = f"""
## 🔬 VARIABLES PARA: {tema_consulta.title()}

### **VARIABLES INDEPENDIENTES**
- Factores contextuales
- Estrategias implementadas
- Recursos disponibles

### **VARIABLES DEPENDIENTES**
- Resultados observables
- Impacto medible
- Efectividad

*Contexto: {contexto_consulta}*
"""
                st.markdown(respuesta)

with tab3:
    st.markdown("## 💬 Chat Inteligente con IA")
    
    # Configuración del contexto y modo IA
    col_config1, col_config2 = st.columns([2, 1])
    
    with col_config1:
        contexto_chat = st.text_input(
            "🎯 Contexto de investigación para esta conversación:",
            placeholder="Ej: mi tesis de maestría, investigación en educación superior...",
            value="proyecto de investigación académica"
        )
    
    with col_config2:
        # Interruptor para modo IA
        modo_ia = st.toggle("🤖 Activar modo IA", value=False)
        st.session_state.modo_ia = modo_ia
    
    # Botón para limpiar chat
    col_clear, col_stats = st.columns([1, 3])
    with col_clear:
        if st.button("🔄 Limpiar Conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_stats:
        if st.session_state.chat_history:
            st.info(f"💬 Conversación activa: {len(st.session_state.chat_history)//2} intercambios")
        if st.session_state.modo_ia:
            st.success("🤖 Modo IA activado - Respuestas con inteligencia artificial")
    
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
        if st.button("🧩 Planteamiento", use_container_width=True):
            st.session_state.ejemplo_activo = "Formule el planteamiento del problema sobre competencias digitales para la empleabilidad en la era digital"
    
    with col_ex2:
        if st.button("🎯 Objetivos", use_container_width=True):
            st.session_state.ejemplo_activo = "Genere objetivos de investigación sobre la implementación de inteligencia artificial en instituciones educativas"
    
    with col_ex3:
        if st.button("🔬 Metodología", use_container_width=True):
            st.session_state.ejemplo_activo = "Sugiera una metodología para investigar el impacto de las redes sociales en el aprendizaje de adolescentes"
    
    with col_ex4:
        if st.button("📚 Con IA", use_container_width=True):
            st.session_state.ejemplo_activo = "Analice las tendencias actuales en educación virtual y sugiera referencias bibliográficas recientes en formato APA"
    
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
            with st.spinner("🤔 Analizando su consulta..."):
                respuesta = procesar_consulta_usuario(prompt, contexto_chat, st.session_state.modo_ia)
                st.markdown(respuesta)
        
        # Agregar respuesta al historial
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

# Configuración de API Key - SEGURA
with st.sidebar.expander("🔧 Configuración de API OpenAI", expanded=False):
    st.info("Para uso personal - configura tu API key temporalmente")
    
    # Opción 1: Usar secrets de Streamlit (recomendado)
    try:
        if st.secrets["openai_api_key"]:
            openai.api_key = st.secrets["openai_api_key"]
            st.success("✅ API Key configurada (vía secrets)")
            st.session_state.api_key_configurada = True
    except:
        # Opción 2: Input temporal (solo para esta sesión)
        api_key = st.text_input("API Key Temporal:", type="password", placeholder="sk-...", key="api_key_temp")
        if api_key:
            openai.api_key = api_key
            st.success("✅ API Key temporal configurada")
            st.warning("⚠️ Esta key solo funciona en tu sesión actual")
            st.session_state.api_key_configurada = True
        else:
            st.warning("🔒 Modo IA no disponible - Configura tu API key")
    
    st.markdown("---")
    st.markdown("**¿No tienes API Key?**")
    st.markdown("[Obtener API Key de OpenAI](https://platform.openai.com/api-keys)")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🔬 Asistente de Investigación Académica Inteligente | "
    "🤖 Con tecnología GPT-4 | "
    "✅ Sistema funcionando correctamente"
    "</div>", 
    unsafe_allow_html=True
)




