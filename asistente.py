import streamlit as st
import re
import openai
import os

# Configuración de página
st.set_page_config(
    page_title="Asistente de Investigación Inteligente",
    page_icon="  ",
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

<h1>   Asistente de Investigación Académica Inteligente</h1> 
    <p style="margin: 0; font-size: 1.2em;">Herramienta con IA para el desarrollo de proyectos 
de investigación</p> 
    <p style="margin: 10px 0 0 0; font-size: 1em;">   Con tecnología GPT-4 |    Sistema 
funcionando correctamente</p> 
</div> 
""", unsafe_allow_html=True)

# Definición de prompt base para el asistente IA
PROMPT_BASE = """
Eres un catedrático universitario especializado en redacción académica de alto nivel. Sigue 
ESTRICTAMENTE estas directivas de calidad: 

**NIVEL REDACIONAL EXIGENTE:** 
- Evitar absolutamente frases como "El Del Qué", "En Cuanto A", "Cabe Señalar Que" 
- Usar sintaxis compleja pero elegante, con subordinación adecuada 
- Emplear vocabulario académico preciso y especializado 
- Mantener coherencia textual entre párrafos 
- Utilizar conectores discursivos sofisticados 

**ESTRUCTURA ACADÉMICA:** 
- Desarrollar argumentos con introducción, desarrollo y conclusión en cada párrafo 
- Establecer relaciones causales y lógicas entre ideas 
- Fundamentar cada afirmación con evidencia o referencias 
- Mantener objetividad y tono académico formal 

**FORMATO Y PRECISIÓN:** 
- Respetar exactamente la extensión solicitada 
- Incluir citas verificables cuando sea requerido 
- Numerar párrafos si se solicita explícitamente

- Usar encabezados jerárquicos cuando corresponda 

**EJEMPLO DE REDACCIÓN CORRECTA:** 
"Incorporar las competencias digitales en la formación docente constituye un imperativo 
pedagógico en la sociedad contemporánea, donde la transformación tecnológica redefine los 
procesos de enseñanza-aprendizaje y exige nuevas capacidades profesionales." 

**EJEMPLO DE REDACCIÓN INCORRECTA A EVITAR:** 
"El Del Qué Competencias digitales son importantes en la educación de hoy en día." 

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

# Funciones de procesamiento de lenguaje que mejoran la extracción limpia y académica del tema
def limpiar_tema(tema):
    # Elimina conectores y palabras vacías frecuentemente mal incluidas en el tema principal
    palabras_excluir = [
        "el del que", "el del qué", "el", "la", "los", "las", "del", "de la",
        "de los", "sobre", "acerca de", "tema", "planteamiento", "problema",
        "interrogante", "redacta", "elabora", "desarrolla", "haz", "crea", 
        "genera", "para la", "para el", "para", "necesito", "quiero", "dame", 
        "un", "una"
    ]
    tema = tema.lower()
    # Elimina las frases completas primero
    for palabra in palabras_excluir:
        tema = tema.replace(palabra, "")
    # Sustituye dobles espacios por espacio único
    tema = " ".join(tema.split())
    # Elimina espacios al inicio y fin
    return tema.strip()

def extraer_tema_principal(user_input):
    """
    Extrae el tema real del input del usuario y lo limpia.
    Devuelve la idea central, sin conectores ni frases innecesarias.
    """
    try:
        patron_pregunta = r"(¿|que|cuales|como|por que|donde|cuando)?(.*)"
        coincidencia = re.search(patron_pregunta, user_input.lower())
        if coincidencia:
            tema = coincidencia.group(2).strip()
        else:
            tema = user_input
        tema_limpio = limpiar_tema(tema)
        # Si el resultado queda vacío, regresa el texto original.
        return tema_limpio if tema_limpio else user_input
    except Exception:
        return user_input

# Función para detectar tipo de solicitud (planteamiento, objetivos, etc.)
def detectar_tipo_solicitud(user_input):
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

# Funciones de generación de contenido académico
def generar_planteamiento_estructurado(tema, contexto=""):
    planteamiento = f"""
# PLANTEAMIENTO DEL PROBLEMA: {tema.title()}

## DESCRIPCION DEL PROBLEMA

En el contexto actual caracterizado por la rápida evolución tecnológica y las transformaciones
sociales, se ha identificado una problemática significativa en el ámbito de **{tema}**. La
disyunción existente entre las demandas emergentes y las capacidades actuales genera
consecuencias relevantes que merecen atención investigativa.

## JUSTIFICACION DE LA INVESTIGACION

El estudio de {tema} se justifica por las siguientes consideraciones fundamentales:

1. **Relevancia contemporánea**: Constituye un tema de actualidad en el marco de los
procesos de transformación digital y social.
2. **Impacto multidimensional**: Sus efectos repercuten en diversos ámbitos: social,
económico, educativo y organizacional.
3. **Vacío en la literatura**: Existe una necesidad evidente de investigaciones actualizadas que
aborden esta temática desde perspectivas innovadoras.
4. **Aplicabilidad práctica**: Los hallazgos pueden traducirse en estrategias concretas y
soluciones aplicables.

## DELIMITACION DEL ESTUDIO

Esta investigación se circunscribirá a:
- **Ámbito temático**: Aspectos específicos relacionados con {tema}
- **Contexto de aplicación**: {contexto if contexto else "entornos diversos y representativos"}
- **Enfoque metodológico**: Análisis integral seguido de propuestas de mejora

## PREGUNTAS DE INVESTIGACION

1. ¿Cuáles son los factores determinantes que influyen significativamente en {tema}?
2. ¿Qué impacto observable genera {tema} en los diferentes contextos de aplicación?
3. ¿Qué estrategias y metodologías demostrarían mayor efectividad para optimizar los
resultados asociados a {tema}?
4. ¿Qué brechas de conocimiento y oportunidades de desarrollo futuro pueden identificarse en
este campo de estudio?

*Contexto específico considerado: {contexto if contexto else "ámbito general de aplicación"}*
"""
    return planteamiento

def generar_objetivos_estructurados(tema, contexto=""):
    contexto_texto = contexto if contexto else "diversos escenarios y contextos de aplicación"
    
    objetivos = f"""
# OBJETIVOS DE INVESTIGACION: {tema.title()}

## OBJETIVO GENERAL

Analizar sistemáticamente los aspectos fundamentales de **{tema}** en el contexto de
**{contexto_texto}**, con el propósito de formular estrategias de mejora, innovación y
optimización que contribuyan al avance del conocimiento y la práctica en este campo de
estudio.

## OBJETIVOS ESPECIFICOS

1. **Identificar y caracterizar** los componentes, dimensiones y variables clave asociados con
{tema}, estableciendo un marco conceptual robusto que facilite su comprensión integral.

2. **Diagnosticar el estado actual** de {tema} mediante el análisis exhaustivo de tendencias,
prácticas predominantes y desafíos identificados tanto en la literatura especializada como en
contextos reales de aplicación.

3. **Evaluar el impacto** de {tema} en diferentes ámbitos (social, económico, educativo,
organizacional), considerando variables contextuales y características poblacionales específicas.

4. **Diseñar y proponer** estrategias, metodologías o herramientas innovadoras para la
optimización de {tema}, fundamentadas en evidencia empírica y mejores prácticas
identificadas.

5. **Validar la aplicabilidad** de las propuestas formuladas mediante criterios de factibilidad,
sostenibilidad y alineamiento con necesidades identificadas en el contexto de {contexto_texto}.
"""
    return objetivos

# Función principal para procesar la consulta del usuario y generar la respuesta adecuada
def procesar_consulta_usuario(user_input, contexto="", usar_ia=False):
    try:
        # Extraer tema y tipo de solicitud
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        # Mostrar información de contexto (para debug/interfaz)
        st.info(f"Tema detectado: {tema_real}")
        if contexto:
            st.info(f"Contexto considerado: {contexto}")
        if usar_ia:
            st.success("Modo IA activado - Generando respuesta con inteligencia artificial")
        
        # Si el modo IA está activado, usar la función de IA
        if usar_ia:
            with st.spinner("Consultando con IA..."):
                respuesta = generar_respuesta_ia(user_input, contexto)
                return respuesta
        
        # Si no, usar las funciones predefinidas para cada tipo de solicitud
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto)
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto)
        elif tipo_solicitud == "metodologia":
            respuesta = f"""
## SUGERENCIAS METODOLOGICAS PARA: {tema_real.title()}

### ENFOQUE METODOLOGICO RECOMENDADO
**Investigación Mixta de Diseño Secuencial Explicativo** - Combina métodos cuantitativos y
cualitativos para un análisis comprensivo.

### DISEÑO DE INVESTIGACION
- **Tipo**: Secuencial explicativo
- **Fase 1**: Análisis cuantitativo (encuestas, datos secundarios)
- **Fase 2**: Profundización cualitativa (entrevistas, estudios de caso)

### TÉCNICAS DE RECOLECCIÓN
- Encuestas con escalas Likert validadas
- Entrevistas semiestructuradas
- Análisis documental sistemático
- Grupos focales para triangulación

*Contexto: {contexto if contexto else "diversos escenarios de aplicación"}*
"""
        elif tipo_solicitud == "variables":
            respuesta = f"""
## VARIABLES DE INVESTIGACION PARA: {tema_real.title()}

### VARIABLES INDEPENDIENTES
- Factores influyentes en {tema_real}
- Estrategias implementadas
- Características contextuales

### VARIABLES DEPENDIENTES
- Resultados observables
- Impacto medible
- Efectividad de intervenciones

### VARIABLES DE CONTROL
- Contexto específico
- Características poblacionales
- Recursos disponibles

*Contexto: {contexto}*
"""
        else:
            respuesta = f"""
## ASESORÍA ESPECIALIZADA EN INVESTIGACIÓN: {tema_real.title()}

He analizado su consulta sobre **\"{tema_real}\"** y puedo ofrecerle orientación en:

### ENFOQUES RECOMENDADOS:
- **Investigación exploratoria**: Para caracterizar el fenómeno
- **Investigación explicativa**: Para identificar relaciones causales
- **Investigación aplicada**: Para desarrollar soluciones prácticas

### ASPECTOS CLAVE:
- Definición clara del problema de investigación
- Establecimiento de preguntas guía
- Selección de metodología apropiada
- Operacionalización de variables

### PRÓXIMOS PASOS:
1. Búsqueda bibliográfica especializada
2. Delimitación del marco teórico-conceptual
3. Formulación de hipótesis o preguntas
4. Diseño metodológico detallado

**¿Le gustaría que profundice en algún aspecto específico?**
"""
        
        return respuesta

    except Exception as e:
        return f"Se ha producido un error en el procesamiento: {str(e)}"


# Inicializar interfaz y lógica aquí (no modificado, solo para referencia)
# ... seguiría el código que maneja la interfaz Streamlit y las interacciones de usuario (botones, pestañas, chat, etc.)



