# asistente_investigacion_ultra_simple.py
import streamlit as st
import requests
import time
from datetime import datetime
import io
import csv
import re

# Clase Agente con memoria
class AgenteConMemoria:
    def __init__(self):
        self.memoria = []
    
    def agregar_memoria(self, entrada, salida):
        self.memoria.append({"entrada": entrada, "salida": salida, "timestamp": datetime.now()})
    
    def obtener_memoria(self):
        return self.memoria
    
    def limpiar_memoria(self):
        self.memoria = []

# FUNCIONES DE BÚSQUEDA SIMULADAS (no necesitan dependencias externas)
def buscar_semantic_scholar(query, max_results=5):
    """Búsqueda simulada en Semantic Scholar"""
    articulos = []
    
    # Datos de ejemplo realistas
    temas = query.lower().split()
    tema_principal = " ".join(temas[:2]) if temas else query
    
    ejemplos_articulos = [
        {
            "titulo": f"Análisis de {tema_principal} en contextos digitales: Una revisión sistemática",
            "autor": "García, M., Rodríguez, P., López, A.",
            "año": "2023",
            "publicacion": "Journal of Digital Innovation",
            "url": "https://example.com/article1",
            "fuente": "Semantic Scholar"
        },
        {
            "titulo": f"Impacto de {tema_principal} en la transformación educativa contemporánea",
            "autor": "Smith, J., Johnson, L., Williams, R.",
            "año": "2022", 
            "publicacion": "International Journal of Educational Technology",
            "url": "https://example.com/article2",
            "fuente": "Semantic Scholar"
        }
    ]
    
    for i in range(min(max_results, len(ejemplos_articulos))):
        articulos.append(ejemplos_articulos[i])
    
    time.sleep(1)
    return articulos

def buscar_scielo(query, max_results=5):
    """Búsqueda simulada en SciELO"""
    articulos = []
    
    temas = query.lower().split()
    tema_principal = " ".join(temas[:2]) if temas else query
    
    ejemplos_articulos = [
        {
            "titulo": f"{tema_principal.title()} en América Latina: Un análisis regional",
            "autor": "Silva, A., Costa, M., Rojas, P.",
            "año": "2023",
            "publicacion": "Revista Latinoamericana de Estudios Educativos",
            "url": "https://scielo.example.com/article1",
            "fuente": "SciELO"
        },
        {
            "titulo": f"Aproximaciones metodológicas al estudio de {tema_principal} en contextos diversos",
            "autor": "Fernández, L., Ortega, R., Mendoza, S.",
            "año": "2022",
            "publicacion": "Investigación Educativa",
            "url": "https://scielo.example.com/article2",
            "fuente": "SciELO"
        }
    ]
    
    for i in range(min(max_results, len(ejemplos_articulos))):
        articulos.append(ejemplos_articulos[i])
    
    time.sleep(1)
    return articulos

# FUNCIONES DE PROCESAMIENTO
def extraer_tema_principal(user_input):
    """Extrae el tema real de investigación del input del usuario"""
    try:
        patron_pregunta = r'[¿]?(qué|cuales|como|por qué|dónde|cuándo)\s+([^?]+)[?]'
        coincidencia = re.search(patron_pregunta, user_input.lower())
        
        if coincidencia:
            return coincidencia.group(2).strip()
        
        palabras_excluir = ['formula', 'planteamiento', 'problema', 'interrogante', 
                           'redacta', 'elabora', 'desarrolla', 'haz', 'crea', 'genera',
                           'para la', 'sobre', 'acerca de', 'necesito', 'quiero']
        
        tema = user_input.lower()
        for palabra in palabras_excluir:
            tema = tema.replace(palabra, '')
        
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

# FUNCIONES DE GENERACIÓN
def generar_planteamiento_estructurado(tema, contexto=""):
    """Genera un planteamiento del problema bien estructurado"""
    return f"""
# PLANTEAMIENTO DEL PROBLEMA: {tema.title()}

## DESCRIPCIÓN DEL PROBLEMA
La acelerada transformación digital ha generado una disrupción significativa en las competencias requeridas. Existe una brecha creciente entre las habilidades que poseen los individuos y las demandadas por entornos tecnificados.

## JUSTIFICACIÓN
La identificación de competencias esenciales resulta urgente por:
- **Relevancia económica**: La brecha de habilidades representa un costo significativo
- **Inclusión social**: La falta de competencias puede exacerbar desigualdades
- **Sostenibilidad laboral**: La evolución tecnológica requiere reconversión constante

## PREGUNTAS DE INVESTIGACIÓN
1. ¿Qué competencias específicas son críticas para la resiliencia profesional?
2. ¿Cómo se articulan las competencias técnicas con habilidades socioemocionales?
3. ¿Qué estrategias de desarrollo demuestran mayor efectividad?
"""

def generar_objetivos_estructurados(tema, contexto=""):
    """Genera objetivos de investigación estructurados"""
    contexto_texto = contexto if contexto else "diversos escenarios"
    return f"""
OBJETIVO GENERAL:
Analizar los aspectos fundamentales de {tema} en el contexto de {contexto_texto} para proponer estrategias de mejora e innovación.

OBJETIVOS ESPECÍFICOS:

1. **Identificar y caracterizar** los componentes clave asociados con {tema}

2. **Diagnosticar el estado actual** mediante el análisis de tendencias y desafíos

3. **Evaluar el impacto** de {tema} en diferentes ámbitos

4. **Diseñar y proponer** estrategias innovadoras basadas en evidencia
"""

# FUNCIÓN DE CHAT PRINCIPAL
def chat_con_agente(agente, user_input, contexto_usuario=""):
    """Función principal del chat completamente funcional"""
    try:
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        st.info(f"🔍 **Tema detectado:** {tema_real}")
        if contexto_usuario:
            st.info(f"🎯 **Contexto considerado:** {contexto_usuario}")
        
        # Generar respuesta según el tipo de solicitud
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto_usuario)
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto_usuario)
        elif tipo_solicitud == "metodologia":
            respuesta = f"## 🎓 SUGERENCIAS METODOLÓGICAS PARA: {tema_real}\n\n**Enfoque recomendado:** Investigación mixta\n**Diseño:** Secuencial explicativo\n**Técnicas:** Encuestas, entrevistas, análisis documental"
        elif tipo_solicitud == "variables":
            respuesta = f"## 🔬 VARIABLES PARA: {tema_real}\n\n**Variables independientes:** Nivel de implementación, características contextuales\n**Variables dependientes:** Impacto en resultados, grado de adopción"
        else:
            respuesta = f"**💡 Respuesta sobre: {tema_real}**\n\nPuedo ayudarte con:\n- Planteamiento del problema\n- Objetivos de investigación\n- Metodología\n- Variables operativas\n\n¿En qué aspecto específico necesitas ayuda?"
        
        # Guardar en memoria
        agente.agregar_memoria(user_input, respuesta)
        return respuesta
        
    except Exception as e:
        return f"❌ Error en el procesamiento: {str(e)}"

# FUNCIÓN PRINCIPAL DE STREAMLIT
def main():
    st.set_page_config(
        page_title="Asistente de Investigación",
        page_icon="🔬",
        layout="wide"
    )
    
    # CSS simple
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔬 Asistente de Investigación Académica</h1>
        <p>Herramienta inteligente para el desarrollo de proyectos de investigación</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if 'articulos' not in st.session_state:
        st.session_state.articulos = []
    if 'agente' not in st.session_state:
        st.session_state.agente = AgenteConMemoria()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Pestañas principales
    tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "🔍 Búsqueda", "💬 Chat"])
    
    with tab1:
        st.markdown("### 🚀 ¿Qué puedes hacer?")
        st.markdown("""
        - **Chat inteligente** con procesamiento de lenguaje natural
        - **Búsqueda académica** simulada en bases de datos
        - **Generación automática** de elementos de investigación
        - **Exportación** de resultados
        """)
        
        st.markdown("### 💡 Ejemplos de preguntas:")
        st.code("""
"Formula el planteamiento sobre competencias digitales"
"Genera objetivos para investigación sobre IA en educación" 
"Sugiere metodología para estudiar impacto de redes sociales"
        """)
    
    with tab2:
        st.markdown("### 🔍 Búsqueda Académica")
        
        consulta = st.text_input(
            "Tema de investigación:",
            value="competencias digitales",
            placeholder="Escribe tu tema de investigación..."
        )
        
        if st.button("🚀 Buscar Artículos"):
            with st.spinner("Buscando en bases académicas..."):
                articulos_ss = buscar_semantic_scholar(consulta)
                articulos_scielo = buscar_scielo(consulta)
                
                st.session_state.articulos = articulos_ss + articulos_scielo
                
                st.success(f"✅ Encontrados {len(st.session_state.articulos)} artículos")
                
                for art in st.session_state.articulos:
                    st.markdown(f"**{art['titulo']}**")
                    st.markdown(f"*{art['autor']}* - {art['año']}")
                    st.markdown(f"Fuente: {art['fuente']}")
                    st.markdown("---")
    
    with tab3:
        st.markdown("### 💬 Chat con el Agente")
        
        # Contexto
        contexto = st.text_input(
            "Contexto de investigación (opcional):",
            placeholder="Ej: educación superior, empresas tecnológicas..."
        )
        
        # Mostrar historial
        for mensaje in st.session_state.chat_history:
            with st.chat_message(mensaje["role"]):
                st.markdown(mensaje["content"])
        
        # Input de chat
        prompt = st.chat_input("Escribe tu pregunta sobre investigación...")
        
        if prompt:
            # Agregar mensaje del usuario
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Respuesta del agente
            with st.chat_message("assistant"):
                with st.spinner("Generando respuesta..."):
                    respuesta = chat_con_agente(st.session_state.agente, prompt, contexto)
                    st.markdown(respuesta)
            
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

if __name__ == "__main__":
    main()
