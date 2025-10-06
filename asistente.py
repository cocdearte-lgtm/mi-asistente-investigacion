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
# Definición de prompt base para el asistente IA
PROMPT_BASE = """
Eres un investigador academico senior especializado en redaccion cientifica. Sigue ESTRICTAMENTE estas directivas:

1. ESTRUCTURA: Respetar exactamente la estructura solicitada (parrafos, longitud, formato)
2. EXTENSION: Cumplir con el numero exacto de parrafos y lineas solicitadas
3. CITAS: Incluir referencias verificables con autores reales, anos y fuentes
4. COHERENCIA: Mantener hilo conductor academico entre todos los parrafos
5. PROFUNDIDAD: Desarrollar cada punto con rigor academico y precision conceptual
6. FORMATEO: Usar encabezados, listas y formato claro cuando sea apropiado
7. LONGITUD: Asegurar que cada parrafo tenga 8-10 lineas de contenido sustancial
8. FUENTES: Proporcionar citas APA con autores, titulos, anos y fuentes verificables

Si el usuario solicita un numero especifico de parrafos, debes entregar EXACTAMENTE esa cantidad.

Consulta o instruccion del usuario:
"""

# Función para generar la respuesta del agente IA
def generar_respuesta_ia(mensaje_usuario, contexto=""):
    prompt_completo = PROMPT_BASE + mensaje_usuario
    if contexto:
        prompt_completo += f"\n\nContexto adicional: {contexto}"
    
    try:
        # Nota: Necesitaras configurar tu API key de OpenAI
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

Parece que hay un problema con la conexion a la API de OpenAI. Error: {str(e)}

**Mientras tanto, aqui tienes una guia general:**

Para consultas sobre '{mensaje_usuario}', te recomiendo:

**Fuentes academicas sugeridas:**
- Google Scholar para busqueda de articulos cientificos
- Scopus y Web of Science para literatura especializada
- ScienceDirect y JSTOR para acceso a textos completos

**Enfoque de investigacion recomendado:**
1. Realiza una revision sistematica de literatura
2. Identifica los autores mas citados en el area
3. Analiza las metodologias predominantes
4. Establece tu marco teorico y conceptual

**Proximos pasos:**
- Define claramente tu pregunta de investigacion
- Selecciona la metodologia apropiada
- Establece tus criterios de inclusion/exclusion
- Planifica tu estrategia de busqueda bibliografica

*Para usar la funcionalidad completa de IA, necesitaras configurar una API key de OpenAI.*"""

# Inicializar session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'contexto_actual' not in st.session_state:
    st.session_state.contexto_actual = ""
if 'modo_ia' not in st.session_state:
    st.session_state.modo_ia = False

# Funciones de procesamiento de lenguaje
def extraer_tema_principal(user_input):
    """Extrae el tema real de investigacion del input del usuario"""
    try:
        # Patron para detectar preguntas de investigacion
        patron_pregunta = r'[¿]?(que|cuales|como|por que|donde|cuando)\s+([^?]+)[?]'
        coincidencia = re.search(patron_pregunta, user_input.lower())
        
        if coincidencia:
            return coincidencia.group(2).strip()
        
        # Eliminar palabras de solicitud metodologica
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
    
    if any(palabra in input_lower for palabra in ['planteamiento', 'problema', 'pregunta investigacion']):
        return "planteamiento"
    elif any(palabra in input_lower for palabra in ['objetivos', 'metas', 'propositos']):
        return "objetivos"
    elif any(palabra in input_lower for palabra in ['metodologia', 'metodo', 'diseno', 'enfoque']):
        return "metodologia"
    elif any(palabra in input_lower for palabra in ['variables', 'operacional']):
        return "variables"
    else:
        return "general"

# Funciones de generacion de contenido MEJORADAS
def generar_planteamiento_estructurado(tema, contexto=""):
    """Genera un planteamiento del problema bien estructurado con excelente redaccion"""
    
    planteamiento = f"""
# PLANTEAMIENTO DEL PROBLEMA: {tema.title()}

## DESCRIPCION DEL PROBLEMA

En el contexto actual caracterizado por la rapida evolucion tecnologica y las transformaciones sociales, se ha identificado una problematica significativa en el ambito de **{tema}**. La disyuncion existente entre las demandas emergentes y las capacidades actuales genera consecuencias relevantes que merecen atencion investigativa.

## JUSTIFICACION DE LA INVESTIGACION

El estudio de {tema} se justifica por las siguientes consideraciones fundamentales:

1. **Relevancia contemporanea**: Constituye un tema de actualidad en el marco de los procesos de transformacion digital y social.
2. **Impacto multidimensional**: Sus efectos repercuten en diversos ambitos: social, economico, educativo y organizacional.
3. **Vacio en la literatura**: Existe una necesidad evidente de investigaciones actualizadas que aborden esta tematica desde perspectivas innovadoras.
4. **Aplicabilidad practica**: Los hallazgos pueden traducirse en estrategias concretas y soluciones aplicables.

## DELIMITACION DEL ESTUDIO

Esta investigacion se circunscribira a:
- **Ambito tematico**: Aspectos especificos relacionados con {tema}
- **Contexto de aplicacion**: {contexto if contexto else "entornos diversos y representativos"}
- **Enfoque metodologico**: Analisis integral seguido de propuestas de mejora

## PREGUNTAS DE INVESTIGACION

1. ¿Cuales son los factores determinantes que influyen significativamente en {tema}?
2. ¿Que impacto observable genera {tema} en los diferentes contextos de aplicacion?
3. ¿Que estrategias y metodologias demostrarian mayor efectividad para optimizar los resultados asociados a {tema}?
4. ¿Que brechas de conocimiento y oportunidades de desarrollo futuro pueden identificarse en este campo de estudio?

*Contexto especifico considerado: {contexto if contexto else "ambito general de aplicacion"}*
"""
    return planteamiento

def generar_objetivos_estructurados(tema, contexto=""):
    """Genera objetivos de investigacion estructurados con redaccion academica"""
    contexto_texto = contexto if contexto else "diversos escenarios y contextos de aplicacion"
    
    objetivos = f"""
# OBJETIVOS DE INVESTIGACION: {tema.title()}

## OBJETIVO GENERAL

Analizar sistematicamente los aspectos fundamentales de **{tema}** en el contexto de **{contexto_texto}**, con el proposito de formular estrategias de mejora, innovacion y optimizacion que contribuyan al avance del conocimiento y la practica en este campo de estudio.

## OBJETIVOS ESPECIFICOS

1. **Identificar y caracterizar** los componentes, dimensiones y variables clave asociados con {tema}, estableciendo un marco conceptual robusto que facilite su comprension integral.

2. **Diagnosticar el estado actual** de {tema} mediante el analisis exhaustivo de tendencias, practicas predominantes y desafios identificados tanto en la literatura especializada como en contextos reales de aplicacion.

3. **Evaluar el impacto** de {tema} en diferentes ambitos (social, economico, educativo, organizacional), considerando variables contextuales y caracteristicas poblacionales especificas.

4. **Diseñar y proponer** estrategias, metodologias o herramientas innovadoras para la optimizacion de {tema}, fundamentadas en evidencia empirica y mejores practicas identificadas.

5. **Validar la aplicabilidad** de las propuestas formuladas mediante criterios de factibilidad, sostenibilidad y alineamiento con necesidades identificadas en el contexto de {contexto_texto}.
"""
    return objetivos

# Funcion principal del chat MEJORADA con IA
def procesar_consulta_usuario(user_input, contexto="", usar_ia=False):
    """Procesa la consulta del usuario y genera respuesta con excelente redaccion"""
    try:
        # Extraer tema y tipo de solicitud
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        # Mostrar informacion de contexto
        st.info(f"Tema detectado: {tema_real}")
        if contexto:
            st.info(f"Contexto considerado: {contexto}")
        if usar_ia:
            st.success("Modo IA activado - Generando respuesta con inteligencia artificial")
        
        # Si el modo IA esta activado, usar la funcion de IA
        if usar_ia:
            with st.spinner("Consultando con IA..."):
                respuesta = generar_respuesta_ia(user_input, contexto)
                return respuesta
        
        # Si no, usar las funciones predefinidas
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto)
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto)
        elif tipo_solicitud == "metodologia":
            respuesta = f"""
## SUGERENCIAS METODOLOGICAS PARA: {tema_real.title()}

### ENFOQUE METODOLOGICO RECOMENDADO
**Investigacion Mixta de Diseño Secuencial Explicativo** - Combina metodos cuantitativos y cualitativos para un analisis comprehensivo.

### DISEÑO DE INVESTIGACION
- **Tipo**: Secuencial explicativo
- **Fase 1**: Analisis cuantitativo (encuestas, datos secundarios)
- **Fase 2**: Profundizacion cualitativa (entrevistas, estudios de caso)

### TECNICAS DE RECOLECCION
- Encuestas con escalas Likert validadas
- Entrevistas semiestructuradas
- Analisis documental sistematico
- Grupos focales para triangulacion

*Contexto: {contexto if contexto else "diversos escenarios de aplicacion"}*
"""
        elif tipo_solicitud == "variables":
            respuesta = f"""
## VARIABLES DE INVESTIGACION PARA: {tema_real.title()}

### VARIABLES INDEPENDIENTES
- Factores influyentes en {tema_real}
- Estrategias implementadas
- Caracteristicas contextuales

### VARIABLES DEPENDIENTES
- Resultados observables
- Impacto medible
- Efectividad de intervenciones

### VARIABLES DE CONTROL
- Contexto especifico
- Caracteristicas poblacionales
- Recursos disponibles

*Contexto: {contexto}*
"""
        else:
            respuesta = f"""
## ASESORIA ESPECIALIZADA EN INVESTIGACION: {tema_real.title()}

He analizado su consulta sobre **"{tema_real}"** y puedo ofrecerle orientacion en:

### ENFOQUES RECOMENDADOS:
- **Investigacion exploratoria**: Para caracterizar el fenomeno
- **Investigacion explicativa**: Para identificar relaciones causales
- **Investigacion aplicada**: Para desarrollar soluciones practicas

### ASPECTOS CLAVE:
- Definicion clara del problema de investigacion
- Establecimiento de preguntas guia
- Seleccion de metodologia apropiada
- Operacionalizacion de variables

### PROXIMOS PASOS:
1. Busqueda bibliografica especializada
2. Delimitacion del marco teorico-conceptual
3. Formulacion de hipotesis o preguntas
4. Diseño metodologico detallado

**¿Le gustaria que profundice en algun aspecto especifico?**
"""
        
        return respuesta
        
    except Exception as e:
        return f"Se ha producido un error en el procesamiento: {str(e)}"

# Interfaz principal con pestañas
tab1, tab2, tab3 = st.tabs(["Inicio", "Busqueda Rapida", "Chat Inteligente"])

with tab1:
    st.markdown("## Bienvenido al Asistente de Investigacion con IA")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="ia-feature">
        <h4>ASISTENTE CON INTELIGENCIA ARTIFICIAL</h4>
        <p>Ahora potenciado con GPT-4 para respuestas mas inteligentes, contextualizadas y fundamentadas academicamente.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>Chatbot Inteligente con Procesamiento de Lenguaje Natural</h4>
        <p>Sistema avanzado de comprension linguistica para interpretar sus solicitudes de investigacion y generar respuestas contextualizadas y academicamente rigurosas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>Generacion de Elementos de Investigacion Academica</h4>
        <p>Elaboracion automatica de planteamientos de problema, objetivos de investigacion, metodologias y variables operativas con redaccion academica profesional.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>Asesoria Metodologica Especializada</h4>
        <p>Orientacion experta en diseño de investigacion, seleccion de metodos y tecnicas de analisis adecuadas para cada tipo de estudio.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Como utilizar el sistema:")
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>1. Acceder al Chat Inteligente</h4>
        <p>Dirijase a la pestaña "Chat Inteligente"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>2. Activar el modo IA (Opcional)</h4>
        <p>Active el interruptor para respuestas con inteligencia artificial</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h4>3. Formular su consulta</h4>
        <p>Ejemplo:<br>
        <em>"Analice las tendencias actuales en educacion virtual"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Ejemplos de consultas con IA:")
        st.code("""
"Revise la literatura sobre competencias 
digitales docentes y sugiera referencias APA"

"Analice metodologias mixtas para estudiar 
el impacto de redes sociales en adolescentes"

"Proponga un marco teorico para investigacion 
en inteligencia artificial educativa"
        """)

with tab2:
    st.markdown("## Busqueda Rapida y Generacion de Contenido")
    
    col_search1, col_search2 = st.columns([2, 1])
    
    with col_search1:
        tema_consulta = st.text_input(
            "Tema de investigacion principal:",
            placeholder="Ej: competencias digitales, inteligencia artificial educativa...",
            value="competencias digitales en entornos educativos"
        )
    
    with col_search2:
        contexto_consulta = st.text_input(
            "Contexto especifico:",
            placeholder="Ej: educacion superior, empresas tecnologicas...",
            value="instituciones de educacion superior"
        )
    
    st.markdown("---")
    
    # Botones de generacion rapida
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("Generar Planteamiento", use_container_width=True):
            with st.spinner("Generando planteamiento del problema..."):
                respuesta = generar_planteamiento_estructurado(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn2:
        if st.button("Generar Objetivos", use_container_width=True):
            with st.spinner("Generando objetivos de investigacion..."):
                respuesta = generar_objetivos_estructurados(tema_consulta, contexto_consulta)
                st.markdown(respuesta)
    
    with col_btn3:
        if st.button("Generar Metodologia", use_container_width=True):
            with st.spinner("Generando sugerencias metodologicas..."):
                respuesta = f"""
## SUGERENCIAS METODOLOGICAS PARA: {tema_consulta.title()}

### ENFOQUE RECOMENDADO
Investigacion mixta con diseño secuencial explicativo.

### TECNICAS DE RECOLECCION
- Encuestas cuantitativas
- Entrevistas cualitativas
- Analisis documental
- Observacion sistematica

*Contexto: {contexto_consulta}*
"""
                st.markdown(respuesta)
    
    with col_btn4:
        if st.button("Generar Variables", use_container_width=True):
            with st.spinner("Generando variables de investigacion..."):
                respuesta = f"""
## VARIABLES PARA: {tema_consulta.title()}

### VARIABLES INDEPENDIENTES
- Factores contextuales
- Estrategias implementadas
- Recursos disponibles

### VARIABLES DEPENDIENTES
- Resultados observables
- Impacto medible
- Efectividad

*Contexto: {contexto_consulta}*
"""
                st.markdown(respuesta)

with tab3:
    st.markdown("## Chat Inteligente con IA")
    
    # Configuracion del contexto y modo IA
    col_config1, col_config2 = st.columns([2, 1])
    
    with col_config1:
        contexto_chat = st.text_input(
            "Contexto de investigacion para esta conversacion:",
            placeholder="Ej: mi tesis de maestria, investigacion en educacion superior...",
            value="proyecto de investigacion academica"
        )
    
    with col_config2:
        # Interruptor para modo IA
        modo_ia = st.toggle("Activar modo IA", value=False)
        st.session_state.modo_ia = modo_ia
    
    # Boton para limpiar chat
    col_clear, col_stats = st.columns([1, 3])
    with col_clear:
        if st.button("Limpiar Conversacion", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_stats:
        if st.session_state.chat_history:
            st.info(f"Conversacion activa: {len(st.session_state.chat_history)//2} intercambios")
        if st.session_state.modo_ia:
            st.success("Modo IA activado - Respuestas con inteligencia artificial")
    
    st.markdown("---")
    
    # Mostrar historial del chat
    for mensaje in st.session_state.chat_history:
        if mensaje["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>Usted:</strong><br>
                {mensaje["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>Asistente:</strong><br>
                {mensaje["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Ejemplos rapidos para probar
    st.markdown("### Ejemplos para probar:")
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    
    with col_ex1:
        if st.button("Planteamiento", use_container_width=True):
            st.session_state.ejemplo_activo = "Formule el planteamiento del problema sobre competencias digitales para la empleabilidad en la era digital"
    
    with col_ex2:
        if st.button("Objetivos", use_container_width=True):
            st.session_state.ejemplo_activo = "Genere objetivos de investigacion sobre la implementacion de inteligencia artificial en instituciones educativas"
    
    with col_ex3:
        if st.button("Metodologia", use_container_width=True):
            st.session_state.ejemplo_activo = "Sugiera una metodologia para investigar el impacto de las redes sociales en el aprendizaje de adolescentes"
    
    with col_ex4:
        if st.button("Con IA", use_container_width=True):
            st.session_state.ejemplo_activo = "Analice las tendencias actuales en educacion virtual y sugiera referencias bibliograficas recientes en formato APA"
    
    # Input del chat
    prompt = st.chat_input("Escriba su pregunta o solicitud de investigacion...")
    
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
            with st.spinner("Analizando su consulta..."):
                respuesta = procesar_consulta_usuario(prompt, contexto_chat, st.session_state.modo_ia)
                st.markdown(respuesta)
        
        # Agregar respuesta al historial
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

# Configuracion de API Key (seccion colapsada)
with st.sidebar.expander("Configuracion de API OpenAI", expanded=True):
    st.info("Para usar el modo IA, necesitas configurar tu API key de OpenAI")
    api_key = st.text_input("API Key de OpenAI:", type="password", placeholder="sk-...", key="api_key_input")
    if api_key:
        openai.api_key = api_key
        st.success("API Key configurada correctamente")
        st.session_state.api_key_configurada = True
    else:
        st.warning("Ingresa tu API Key para activar el modo IA completo")
    
    st.markdown("---")
    st.markdown("**¿No tienes API Key?**")
    st.markdown("[Obtener API Key de OpenAI](https://platform.openai.com/api-keys)")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Asistente de Investigacion Academica Inteligente | "
    "Con tecnologia GPT-4 | "
    "Sistema funcionando correctamente"
    "</div>", 
    unsafe_allow_html=True
)

