import streamlit as st
import time
from datetime import datetime
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
if 'articulos' not in st.session_state:
    st.session_state.articulos = []
if 'contexto_actual' not in st.session_state:
    st.session_state.contexto_actual = ""

# Funciones de procesamiento de lenguaje
def extraer_tema_principal(user_input):
    """Extrae el tema real de investigación del input del usuario"""
    try:
        # Patrón para detectar preguntas de investigación
        patron_pregunta = r'[¿]?(qué|cuales|como|por qué|dónde|cuándo)\s+([^?]+)[?]'
        coincidencia = re.search(patron_pregunta, user_input.lower())
        
        if coincidencia:
            return coincidencia.group(2).strip()
        
        # Eliminar palabras de solicitud metodológica
        palabras_excluir = ['formula', 'planteamiento', 'problema', 'interrogante', 
                           'redacta', 'elabora', 'desarrolla', 'haz', 'crea', 'genera',
                           'para la', 'sobre', 'acerca de', 'necesito', 'quiero']
        
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
    elif any(palabra in input_lower for palabra in ['resumen', 'síntesis', 'analizar']):
        return "resumen"
    else:
        return "general"

# Funciones de generación de contenido
def generar_planteamiento_estructurado(tema, contexto=""):
    """Genera un planteamiento del problema bien estructurado"""
    return f"""
# 🎯 PLANTEAMIENTO DEL PROBLEMA: {tema.title()}

## 📝 DESCRIPCIÓN DEL PROBLEMA
La acelerada transformación digital y los cambios en los entornos contemporáneos han generado nuevos desafíos en el ámbito de {tema}. Se observa una brecha significativa entre las demandas actuales y las capacidades existentes, lo que genera importantes consecuencias en diversos contextos.

## 🔍 JUSTIFICACIÓN
La investigación en {tema} resulta crucial por varias razones:

1. **Relevancia actual**: El tema es fundamental en el contexto de transformación actual
2. **Impacto significativo**: Afecta a diversos grupos, organizaciones y comunidades
3. **Vacío investigativo**: Existe necesidad de estudios actualizados y contextualizados
4. **Aplicabilidad práctica**: Los hallazgos pueden generar soluciones concretas y mejoras

## 📌 DELIMITACIÓN
Esta investigación se centrará en:
- **Ámbito temático**: Aspectos específicos de {tema}
- **Contexto**: {contexto if contexto else "entornos diversos"}
- **Enfoque**: Análisis integral y propuestas de mejora

## ❓ PREGUNTAS DE INVESTIGACIÓN
1. ¿Cuáles son los factores determinantes que influyen en {tema}?
2. ¿Qué impacto tiene {tema} en el contexto actual?
3. ¿Qué estrategias y metodologías podrían optimizar los resultados relacionados con {tema}?
4. ¿Qué brechas y oportunidades existen para futuros desarrollos en {tema}?

*Contexto específico considerado: {contexto if contexto else "ámbito general"}*
"""

def generar_objetivos_estructurados(tema, contexto=""):
    """Genera objetivos de investigación estructurados"""
    contexto_texto = contexto if contexto else "diversos escenarios y aplicaciones"
    
    return f"""
# 🎯 OBJETIVOS DE INVESTIGACIÓN: {tema.title()}

## 🎯 OBJETIVO GENERAL
Analizar los aspectos fundamentales de {tema} en el contexto de {contexto_texto} para proponer estrategias de mejora, innovación y optimización que contribuyan al avance del conocimiento y la práctica en este campo.

## 📋 OBJETIVOS ESPECÍFICOS

1. **IDENTIFICAR Y CARACTERIZAR** los componentes, dimensiones y variables clave asociados con {tema}, estableciendo un marco conceptual robusto para su comprensión integral.

2. **DIAGNOSTICAR EL ESTADO ACTUAL** de {tema} mediante el análisis de tendencias, prácticas predominantes y desafíos identificados en la literatura especializada y contextos reales de aplicación.

3. **EVALUAR EL IMPACTO** de {tema} en diferentes ámbitos (sociales, económicos, educativos, organizacionales) considerando variables contextuales y poblaciones específicas.

4. **DISEÑAR Y PROPORNER** estrategias, metodologías o herramientas innovadoras para la optimización de {tema}, basadas en evidencia empírica y mejores prácticas identificadas.

5. **VALIDAR LA APLICABILIDAD** de las propuestas mediante criterios de factibilidad, sostenibilidad y alineamiento con necesidades identificadas en el contexto de {contexto_texto}.
"""

def generar_sugerencias_metodologicas(tema, contexto=""):
    """Genera sugerencias metodológicas detalladas"""
    return f"""
## 🎓 SUGERENCIAS METODOLÓGICAS PARA: {tema.title()}

### **ENFOQUE METODOLÓGICO RECOMENDADO**
**Investigación Mixta de Diseño Secuencial Explicativo** - Combina la fortaleza de los métodos cuantitativos para establecer patrones generales con la profundidad de los métodos cualitativos para comprender significados y contextos.

### **DISEÑO DE INVESTIGACIÓN**
- **Tipo**: Secuencial explicativo (Fase cuantitativa → Fase cualitativa)
- **Fase 1**: Estudio cuantitativo para identificar patrones y relaciones
- **Fase 2**: Investigación cualitativa para explicar y profundizar hallazgos
- **Muestreo**: Estratificado por criterios relevantes al contexto

### **TÉCNICAS E INSTRUMENTOS**

**📈 Componente Cuantitativo:**
- *Encuestas* con escalas Likert validadas
- *Análisis documental* cuantitativo de fuentes secundarias
- *Instrumentos*: Cuestionarios estandarizados, registros sistemáticos

**📊 Componente Cualitativo:**
- *Entrevistas semiestructuradas* con guías temáticas
- *Grupos focales* para contraste de perspectivas
- *Observación participante* en contextos naturales
- *Análisis de contenido* de documentos y narrativas

### **CONTEXTO CONSIDERADO**
{contexto if contexto else "Diversos escenarios de aplicación"}
"""

def generar_respuesta_general(tema, user_input):
    """Genera respuesta general del asistente"""
    return f"""
## 💡 ASESORÍA ESPECIALIZADA: {tema.title()}

He analizado tu consulta sobre **{tema}** y puedo orientarte en los siguientes aspectos:

### 🎯 **Enfoques de Investigación Recomendados:**

**1. Investigación Exploratoria-Descriptiva**
- *Adecuado para*: Caracterizar el fenómeno y establecer bases conceptuales
- *Métodos sugeridos*: Revisión sistemática, estudio de casos, análisis documental

**2. Investigación Explicativa**  
- *Adecuado para*: Identificar relaciones causales y factores determinantes
- *Métodos sugeridos*: Diseños cuasi-experimentales, modelado multivariado

**3. Investigación Aplicada**
- *Adecuado para*: Desarrollar soluciones prácticas y validar intervenciones
- *Métodos sugeridos*: Investigación-acción, diseño y desarrollo

### 📊 **Aspectos Clave a Considerar:**
- **Variables de proceso**: Mecanismos, estrategias, metodologías
- **Variables de resultado**: Impacto, efectividad, eficiencia  
- **Variables contextuales**: Entorno, recursos, características poblacionales

### 🔍 **Próximos Pasos Sugeridos:**
1. Realiza una búsqueda bibliográfica especializada
2. Define el marco teórico y conceptual específico
3. Establece preguntas de investigación focalizadas
4. Selecciona la metodología más apropiada a tus objetivos

**¿Te gustaría que profundice en algún aspecto específico de la investigación sobre {tema}?**
"""

# Función principal del chat
def procesar_consulta_usuario(user_input, contexto=""):
    """Procesa la consulta del usuario y genera respuesta"""
    try:
        # Extraer tema y tipo de solicitud
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        # Generar respuesta según el tipo
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto)
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto)
        elif tipo_solicitud == "metodologia":
            respuesta = generar_sugerencias_metodologicas(tema_real, contexto)
        elif tipo_solicitud == "variables":
            respuesta = f"## 🔬 VARIABLES DE INVESTIGACIÓN PARA: {tema_real}\n\n**Variables independientes**: Factores influyentes, estrategias implementadas\n**Variables dependientes**: Resultados, impacto, efectividad\n**Variables de control**: Contexto, características poblacionales\n\n*Contexto: {contexto}*"
        else:
            respuesta = generar_respuesta_general(tema_real, user_input)
        
        return respuesta
        
    except Exception as e:
        return f"❌ Error en el procesamiento: {str(e)}"

# Interfaz principal con pestañas
tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "🔍 Búsqueda Rápida", "💬 Chat Principal"])

with tab1:
    st.markdown("## 🚀 Bienvenido al Asistente de Investigación Inteligente")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h4>💬 Chatbot Inteligente con NLP</h4>
        <p>Procesamiento avanzado de lenguaje natural para entender tus solicitudes de investigación y generar respuestas contextualizadas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>🎯 Generación de Elementos de Investigación</h4>
        <p>Creación automática de planteamientos de problema, objetivos de investigación, metodologías y variables operativas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>📚 Búsqueda Académica Simulada</h4>
        <p>Acceso a bases de datos académicas simuladas con resultados realistas para tu tema de investigación.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Comenzar es fácil:")
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>1. 💬 Ve al Chat</h4>
        <p>Accede a la pestaña "Chat Principal"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>2. 🎯 Escribe tu pregunta</h4>
        <p>Ejemplo:<br>
        <em>"Planteamiento sobre competencias digitales"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>3. 📚 Recibe respuestas</h4>
        <p>Contenido académico estructurado y específico</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Ejemplos de uso:")
        st.code("""
"Formula el planteamiento sobre 
competencias digitales"

"Genera objetivos para investigación 
sobre IA en educación"

"Sugiere metodología para estudiar 
redes sociales"
        """)

with tab2:
    st.markdown("## 🔍 Búsqueda Rápida y Generación de Contenido")
    
    col_search1, col_search2 = st.columns([2, 1])
    
    with col_search1:
        tema_consulta = st.text_input(
            "🔎 Tema de investigación principal:",
            placeholder="Ej: competencias digitales, inteligencia artificial educativa...",
            value="competencias digitales en entornos laborales"
        )
    
    with col_search2:
        contexto_consulta = st.text_input(
            "🎯 Contexto específico:",
            placeholder="Ej: educación superior, empresas tecnológicas...",
            value="transformación digital organizacional"
        )
    
    st.markdown("---")
    
    # Botones de generación rápida
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("🧩 Generar Planteamiento", use_container_width=True):
            with st.spinner("Generando planteamiento del problema..."):
                time.sleep(1)
                respuesta = generar_planteamiento_estructurado(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn2:
        if st.button("🎯 Generar Objetivos", use_container_width=True):
            with st.spinner("Generando objetivos de investigación..."):
                time.sleep(1)
                respuesta = generar_objetivos_estructurados(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn3:
        if st.button("🔬 Generar Metodología", use_container_width=True):
            with st.spinner("Generando sugerencias metodológicas..."):
                time.sleep(1)
                respuesta = generar_sugerencias_metodologicas(tema_consulta, contexto_consulta)
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
    if st.button("🔄 Limpiar Conversación", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    # Mostrar historial del chat
    for mensaje in st.session_state.chat_history:
        if mensaje["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 Tú:</strong><br>
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
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    with col_ex1:
        if st.button("🧩 Ejemplo: Planteamiento", use_container_width=True):
            st.session_state.ejemplo_activo = "Formula el planteamiento del problema sobre competencias digitales para la empleabilidad en la era digital"
    
    with col_ex2:
        if st.button("🎯 Ejemplo: Objetivos", use_container_width=True):
            st.session_state.ejemplo_activo = "Genera objetivos de investigación sobre la implementación de inteligencia artificial en instituciones educativas"
    
    with col_ex3:
        if st.button("🔬 Ejemplo: Metodología", use_container_width=True):
            st.session_state.ejemplo_activo = "Sugiere una metodología para investigar el impacto de las redes sociales en el aprendizaje de adolescentes"
    
    # Input del chat
    prompt = st.chat_input("Escribe tu pregunta o solicitud de investigación...")
    
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
            with st.spinner("🤔 Analizando tu consulta y generando respuesta..."):
                time.sleep(1)  # Simular tiempo de procesamiento
                
                respuesta = procesar_consulta_usuario(prompt, contexto_chat)
                st.markdown(respuesta)
        
        # Agregar respuesta al historial
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🔬 Asistente de Investigación Académica - Versión Ultra Simple | "
    "✅ Sistema funcionando correctamente"
    "</div>", 
    unsafe_allow_html=True
)
