import streamlit as st
import requests
import time
from datetime import datetime
import io
import csv
import re

# Manejo de importaciones con instalación automática
def instalar_dependencias():
    """Intenta instalar las dependencias faltantes"""
    try:
        import subprocess
        import sys
        
        paquetes = [
            "beautifulsoup4",
            "google-generativeai", 
            "python-docx",
            "semantic-scholar"
        ]
        
        for paquete in paquetes:
            try:
                if paquete == "beautifulsoup4":
                    from bs4 import BeautifulSoup
                elif paquete == "google-generativeai":
                    import google.generativeai as genai
                elif paquete == "python-docx":
                    from docx import Document
                elif paquete == "semantic-scholar":
                    from semantic_scholar import SemanticScholar
            except ImportError:
                st.info(f"Instalando {paquete}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
                
    except Exception as e:
        st.warning(f"No se pudieron instalar todas las dependencias: {e}")

# Intentar instalar dependencias al inicio
instalar_dependencias()

# Ahora importar después de posible instalación
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    import google.generativeai as genai
    from google.generativeai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from semantic_scholar import SemanticScholar
    SEMANTIC_SCHOLAR_AVAILABLE = True
except ImportError:
    SEMANTIC_SCHOLAR_AVAILABLE = False

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

# FUNCIONES DE BÚSQUEDA SIMULADAS (para cuando no hay dependencias)
def buscar_semantic_scholar_simulada(query, max_results=5):
    """Búsqueda simulada en Semantic Scholar"""
    articulos = []
    temas = ["inteligencia artificial", "aprendizaje automático", "ciencia de datos", "educación digital"]
    
    for i in range(min(max_results, 3)):
        articulos.append({
            "titulo": f"Estudio sobre {query} - Artículo {i+1}",
            "autor": f"Autor {i+1}, Investigador Principal",
            "año": "2023",
            "publicacion": "Journal of Simulated Research",
            "url": f"https://example.com/article{i+1}",
            "fuente": "Semantic Scholar (Simulado)"
        })
    return articulos

def buscar_scielo_simulada(query, max_results=5):
    """Búsqueda simulada en SciELO"""
    articulos = []
    
    for i in range(min(max_results, 3)):
        articulos.append({
            "titulo": f"Análisis de {query} en contexto latinoamericano - Estudio {i+1}",
            "autor": f"Investigador Latinoamericano {i+1}",
            "año": "2023",
            "publicacion": "Revista Científica Simulada",
            "url": f"https://scielo.example.com/article{i+1}",
            "fuente": "SciELO (Simulado)"
        })
    return articulos

def buscar_semantic_scholar(query, max_results=5):
    """Búsqueda en Semantic Scholar con fallback a simulación"""
    if not SEMANTIC_SCHOLAR_AVAILABLE:
        return buscar_semantic_scholar_simulada(query, max_results)
    
    articulos = []
    try:
        scholar = SemanticScholar()
        resultados = scholar.search_paper(query, limit=max_results)
        count = 0
        for paper in resultados:
            articulos.append({
                "titulo": paper.title,
                "autor": ". ".join([author['name'] for author in paper.authors]) if paper.authors else 'Desconocido',
                "año": str(paper.year) if paper.year else "s.f.",
                "publicacion": paper.venue if paper.venue else "",
                "url": paper.url if paper.url else "",
                "fuente": "Semantic Scholar"
            })
            count += 1
            if count >= max_results:
                break
        time.sleep(0.5)
    except Exception as e:
        st.error(f"Error en Semantic Scholar: {e}")
        # Fallback a simulación
        articulos = buscar_semantic_scholar_simulada(query, max_results)
    return articulos

def buscar_scielo(query, max_results=5):
    """Búsqueda en SciELO con fallback a simulación"""
    if not BEAUTIFULSOUP_AVAILABLE:
        return buscar_scielo_simulada(query, max_results)
    
    articulos = []
    try:
        url = f"https://search.scielo.org/?q={query}&lang=es"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.select(".item")
        
        for resultado in resultados[:max_results]:
            try:
                titulo_elem = resultado.select_one(".title")
                autores_elem = resultado.select_one(".authors")
                enlace_elem = resultado.select_one(".line a")
                
                titulo = titulo_elem.text.strip() if titulo_elem else "Sin titulo"
                autores = autores_elem.text.strip() if autores_elem else "Desconocido"
                enlace = enlace_elem["href"] if enlace_elem else ""
                
                articulos.append({
                    "titulo": titulo,
                    "autor": autores,
                    "año": "s.f.",
                    "publicacion": "SciELO",
                    "url": f"https:{enlace}" if enlace else "",
                    "fuente": "SciELO"
                })
            except Exception:
                continue
    except Exception as e:
        st.error(f"Error en SciELO: {e}")
        # Fallback a simulación
        articulos = buscar_scielo_simulada(query, max_results)
    return articulos

# FUNCIONES DE PROCESAMIENTO DE LENGUAJE MEJORADAS
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
                           'para la', 'sobre', 'acerca de']
        
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

# FUNCIONES DE GENERACIÓN MEJORADAS CON RESPUESTAS PREDEFINIDAS
def generar_planteamiento_estructurado(tema, contexto=""):
    """Genera un planteamiento del problema bien estructurado"""
    
    ejemplos_plantemientos = {
        "competencias digitales": """
# PLANTEAMIENTO DEL PROBLEMA: Competencias Digitales para la Resiliencia en Entornos Automatizados

## DESCRIPCIÓN DEL PROBLEMA
La acelerada transformación digital y la integración de sistemas automatizados e inteligencia artificial en los entornos laborales han generado una disrupción significativa en las competencias requeridas para mantener la empleabilidad y adaptación efectiva. Existe una brecha creciente entre las habilidades digitales que poseen los individuos y las demandadas por entornos cada vez más tecnificados.

## JUSTIFICACIÓN
La identificación de competencias digitales esenciales resulta urgente por:
- **Relevancia económica**: La brecha de habilidades digitales representa un costo para la productividad
- **Inclusión social**: La falta de competencias puede exacerbar desigualdades
- **Sostenibilidad laboral**: La evolución tecnológica amenaza con hacer obsoletas habilidades tradicionales

## DELIMITACIÓN
- **Población**: Profesionales en sectores con alto grado de automatización
- **Contexto**: Entornos laborales en proceso de transformación digital
- **Temporalidad**: Competencias requeridas para los próximos 5 años

## PREGUNTAS DE INVESTIGACIÓN
1. ¿Qué competencias digitales específicas son críticas para la resiliencia profesional en entornos automatizados?
2. ¿Cómo se articulan las competencias técnicas con habilidades socioemocionales para la adaptación efectiva?
3. ¿Qué estrategias de desarrollo demuestran mayor efectividad para fortalecer la resiliencia digital?
""",
        "inteligencia artificial educación": """
# PLANTEAMIENTO DEL PROBLEMA: Inteligencia Artificial en Educación

## DESCRIPCIÓN DEL PROBLEMA
La integración de inteligencia artificial en los procesos educativos representa una transformación paradigmática que afecta metodologías, evaluación y roles docentes. Sin embargo, persisten desafíos en su implementación efectiva y ética.

## JUSTIFICACIÓN
- Mejora de procesos de aprendizaje personalizado
- Optimización de la gestión educativa
- Preparación para entornos laborales futuros
- Necesidad de frameworks éticos para IA educativa

## DELIMITACIÓN
- Niveles educativos: educación superior
- Enfoque: herramientas de IA para aprendizaje adaptativo
- Contexto: instituciones latinoamericanas

## PREGUNTAS DE INVESTIGACIÓN
1. ¿Cómo impacta la IA en los resultados de aprendizaje en educación superior?
2. ¿Qué factores influyen en la adopción efectiva de herramientas de IA educativa?
3. ¿Qué consideraciones éticas deben incorporarse en el diseño de sistemas de IA para educación?
"""
    }
    
    # Buscar ejemplo más cercano al tema
    tema_lower = tema.lower()
    for clave, valor in ejemplos_plantemientos.items():
        if clave in tema_lower:
            return valor
    
    # Plantemiento genérico si no hay coincidencia
    return f"""
# PLANTEAMIENTO DEL PROBLEMA: {tema.title()}

## DESCRIPCIÓN DEL PROBLEMA
La investigación se centra en el análisis de {tema} como área de creciente relevancia en el contexto actual. Este fenómeno presenta desafíos y oportunidades que requieren estudio sistemático.

## JUSTIFICACIÓN
El estudio de {tema} es fundamental debido a su impacto en diversos ámbitos sociales, económicos y tecnológicos. La comprensión profunda de este tema puede contribuir significativamente al avance del conocimiento y la práctica.

## DELIMITACIÓN
- **Ámbito**: Análisis de {tema} en contextos específicos
- **Enfoque**: Investigación aplicada con implicaciones prácticas
- **Alcance**: Estudio de tendencias actuales y prospectivas

## PREGUNTAS DE INVESTIGACIÓN
1. ¿Cuáles son los factores determinantes que influyen en {tema}?
2. ¿Qué relaciones existen entre {tema} y otros constructos relevantes?
3. ¿Qué estrategias pueden implementarse para optimizar los resultados relacionados con {tema}?
4. ¿Qué brechas de conocimiento persisten en la investigación sobre {tema}?
"""

def generar_objetivos_estructurados(tema, contexto=""):
    """Genera objetivos de investigación estructurados"""
    return f"""
OBJETIVO GENERAL:
Analizar los aspectos fundamentales de {tema} en el contexto de {contexto if contexto else 'diversos escenarios'} para proponer estrategias de mejora e innovación.

OBJETIVOS ESPECÍFICOS:
1. Identificar y caracterizar los componentes principales de {tema}
2. Evaluar el impacto y las implicaciones de {tema} en diferentes contextos
3. Diagnosticar los desafíos y oportunidades asociados con {tema}
4. Proponer lineamientos y estrategias para la optimización de {tema}
5. Validar la efectividad de las propuestas mediante indicadores específicos
"""

def generar_respuesta_general(tema, user_input):
    """Genera respuesta general del asistente"""
    return f"""
**Respuesta sobre: {tema}**

Como asistente de investigación, puedo sugerirte los siguientes enfoques para investigar **{tema}**:

## 📚 Enfoques Metodológicos Recomendados:
- **Investigación mixta**: Combinar métodos cuantitativos y cualitativos
- **Revisión sistemática**: Análisis exhaustivo de literatura existente
- **Estudio de casos**: Análisis en profundidad de situaciones específicas

## 🔍 Líneas de Investigación Sugeridas:
1. Análisis del impacto de {tema} en diferentes contextos
2. Identificación de factores determinantes en {tema}
3. Desarrollo de estrategias para optimizar {tema}
4. Evaluación de tendencias futuras en {tema}

## 💡 Próximos Pasos:
- Realiza una búsqueda bibliográfica en las pestañas correspondientes
- Define el contexto específico de tu investigación  
- Establece preguntas de investigación claras y focalizadas

¿Te gustaría que profundice en algún aspecto específico de {tema}?
"""

# FUNCIÓN DE CHAT COMPLETAMENTE REDISEÑADA
def chat_con_agente(agente, user_input, contexto_usuario=""):
    """Función principal del chat completamente mejorada"""
    try:
        # Extraer el tema real de la consulta
        tema_real = extraer_tema_principal(user_input)
        tipo_solicitud = detectar_tipo_solicitud(user_input)
        
        # Generar respuesta según el tipo de solicitud
        if tipo_solicitud == "planteamiento":
            respuesta = generar_planteamiento_estructurado(tema_real, contexto_usuario)
            
        elif tipo_solicitud == "objetivos":
            respuesta = generar_objetivos_estructurados(tema_real, contexto_usuario)
            
        elif tipo_solicitud == "metodologia":
            respuesta = generar_sugerencias_metodologicas_simulada(tema_real, contexto_usuario)
            
        elif tipo_solicitud == "variables":
            respuesta = sugerir_variables_operativas_simulada(tema_real, contexto_usuario)
            
        elif tipo_solicitud == "resumen":
            if hasattr(st.session_state, 'resumen_actual'):
                respuesta = st.session_state.resumen_actual
            else:
                respuesta = "Primero realiza una búsqueda académica para generar resúmenes."
                
        else:
            respuesta = generar_respuesta_general(tema_real, user_input)
        
        # Guardar en memoria
        agente.agregar_memoria(user_input, respuesta)
        return respuesta
        
    except Exception as e:
        return f"Error en el chat: {e}"

# FUNCIONES SIMULADAS PARA CUANDO NO HAY IA
def generar_sugerencias_metodologicas_simulada(tema, contexto=""):
    return f"""
## SUGERENCIAS METODOLÓGICAS PARA: {tema}

### 🎯 Enfoque Recomendado:
**Investigación Mixta** - Combinación de métodos cuantitativos y cualitativos para una comprensión integral.

### 📊 Diseño de Investigación:
- **Diseño secuencial explicativo**: Primero datos cuantitativos, luego cualitativos para profundizar
- **Estudio de casos múltiples**: Análisis comparativo de diferentes contextos

### 🔍 Técnicas de Recolección:
1. **Encuestas** para datos cuantitativos (escalas Likert)
2. **Entrevistas semiestructuradas** para profundizar
3. **Análisis documental** de fuentes secundarias
4. **Grupos focales** para validación colectiva

### 📈 Estrategias de Análisis:
- **Estadística descriptiva e inferencial**
- **Análisis de contenido cualitativo**
- **Triangulación de métodos** para validación
"""

def sugerir_variables_operativas_simulada(tema, contexto=""):
    return f"""
## VARIABLES DE INVESTIGACIÓN PARA: {tema}

### 📊 Variables Independientes:
1. **Nivel de {tema}** - Grado o intensidad del fenómeno estudiado
   *Definición operacional:* Escala de 1-5 basada en indicadores específicos

2. **Contexto de aplicación** - Entorno donde se manifiesta {tema}
   *Definición operacional:* Clasificación según características definidas

### 📈 Variables Dependientes:
1. **Impacto en resultados** - Efecto medible de {tema}
   *Definición operacional:* Métricas cuantitativas predefinidas

2. **Grado de adopción** - Nivel de implementación exitosa
   *Definición operacional:* Porcentaje de implementación vs. objetivo

### 🔄 Variables de Control:
- Experiencia previa
- Recursos disponibles
- Características demográficas
"""

def resumir_articulos_con_gemini(texto):
    """Resumen simulado de artículos"""
    return f"""
## RESUMEN Y ANÁLISIS DE LITERATURA

### 📚 Temas Principales Identificados:
1. **Tendencia creciente** en la investigación del área
2. **Enfoques multidisciplinarios** para abordar el tema
3. **Vacíos de investigación** en aplicaciones prácticas

### 🔍 Vacíos de Investigación Detectados:
- Falta de estudios longitudinales
- Limitada investigación en contextos específicos
- Necesidad de marcos teóricos integradores

### 💡 Líneas de Trabajo Sugeridas:
1. Investigación aplicada en entornos reales
2. Desarrollo de herramientas de evaluación
3. Estudios comparativos internacionales

### 📈 Recomendaciones para Proyecto:
- Enfocar en aplicación práctica
- Considerar variables contextuales
- Incluir perspectiva multidisciplinaria
"""

# FUNCIONES AUXILIARES
def preparar_texto_para_gemini(articulos):
    texto = ""
    for art in articulos:
        texto += f"Título: {art['titulo']}\nAutores: {art['autor']}\nAño: {art['año']}\nURL: {art['url']}\n\n"
    return texto

def generar_bibliografia(referencias, estilo="APA"):
    def formatear_cita(ref):
        autor = ref.get("autor", "Desconocido").strip()
        año = ref.get("año", "").strip() or "s.f."
        titulo = ref.get("titulo", "").strip()
        publicacion = ref.get("publicacion", "").strip()
        url = ref.get("url", "").strip()

        if estilo.upper() == "APA":
            partes = []
            partes.append(f"{autor} ({año})")
            if titulo:
                partes.append(f"{titulo}.")
            if publicacion:
                partes.append(f"{publicacion}.")
            cita = " ".join(partes)
            if url:
                cita += f" Recuperado de {url}"
        else:
            cita = f"{autor} ({año}). {titulo}. {publicacion}"
        return cita

    bibliografia = [formatear_cita(ref) for ref in referencias]
    return "\n\n".join(bibliografia)

# FUNCIÓN PRINCIPAL DE STREAMLIT
def main():
    # Configuración de página
    st.set_page_config(
        page_title="Asistente de Investigación Inteligente",
        page_icon="🔬",
        layout="wide"
    )
    
    # Header principal
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
        <h1>🔬 Asistente de Investigación Inteligente</h1>
        <p>Chatbot mejorado con procesamiento avanzado de lenguaje natural</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar estado de dependencias
    with st.expander("🔧 Estado de Dependencias", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("BeautifulSoup:", "✅" if BEAUTIFULSOUP_AVAILABLE else "❌")
        with col2:
            st.write("Google AI:", "✅" if GENAI_AVAILABLE else "❌")
        with col3:
            st.write("Python-docx:", "✅" if DOCX_AVAILABLE else "❌")
        with col4:
            st.write("Semantic Scholar:", "✅" if SEMANTIC_SCHOLAR_AVAILABLE else "❌")
        
        if not all([BEAUTIFULSOUP_AVAILABLE, GENAI_AVAILABLE, DOCX_AVAILABLE, SEMANTIC_SCHOLAR_AVAILABLE]):
            st.info("""
            💡 **Para funcionalidades completas, instala:**
            ```bash
            pip install beautifulsoup4 google-generativeai python-docx semantic-scholar
            ```
            """)
    
    # Inicializar session state
    if 'articulos' not in st.session_state:
        st.session_state.articulos = []
    if 'agente' not in st.session_state:
        st.session_state.agente = AgenteConMemoria()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'contexto_actual' not in st.session_state:
        st.session_state.contexto_actual = ""
    
    # Pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Inicio", 
        "🔍 Búsqueda Académica", 
        "💬 Chat con Agente",
        "📅 Exportar Resultados"
    ])
    
    # Pestaña de Inicio
    with tab1:
        st.markdown("### 💡 Bienvenido al Asistente de Investigación Inteligente")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🚀 ¿Qué puedes hacer con esta herramienta?
            
            **🔍 Chatbot Inteligente MEJORADO**
            - Procesamiento avanzado de lenguaje natural
            - Detección automática de temas de investigación
            - Generación contextualizada de planteamientos
            - Respuestas específicas y relevantes
            
            **📚 Búsqueda Académica Integrada**
            - Buscar en Semantic Scholar (Internacional)
            - Buscar en SciELO (América Latina)
            - Resultados en tiempo real
            - Filtrado por relevancia
            
            **🤖 Análisis con Inteligencia Artificial**
            - Resúmenes automáticos de literatura
            - Detección de tendencias de investigación
            - Identificación de vacíos en la literatura
            - Sugerencias de líneas de investigación
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 Comenzar es fácil:
            
            1. **Ve a la pestaña 💬 Chat con Agente**
            2. **Escribe tu pregunta naturalmente**
            3. **El sistema detectará automáticamente tu tema**
            4. **Recibe respuestas contextualizadas**
            
            ### 💬 Ejemplos de preguntas:
            - *"Formula el planteamiento sobre competencias digitales en entornos automatizados"*
            - *"Genera objetivos para investigación sobre IA en educación"*
            - *"Sugiere metodología para estudiar impacto de redes sociales"*
            
            ### 🗃️ Bases disponibles:
            ☑ Semantic Scholar  
            ☑ SciELO  
            ☑ Acceso gratuito  
            """)
        
        st.markdown("---")
        st.subheader("📊 Estadísticas de la sesión")
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Artículos encontrados", len(st.session_state.articulos))
        with col_stats2:
            st.metric("Consultas al agente", len(st.session_state.agente.obtener_memoria()))
        with col_stats3:
            st.metric("Mensajes en chat", len(st.session_state.chat_history))
    
    # Pestaña de Búsqueda Académica
    with tab2:
        st.markdown("### 🔍 Búsqueda en Bases Académicas")
        
        col_search1, col_search2 = st.columns([2, 1])
        
        with col_search1:
            consulta = st.text_input(
                "🔍 Tema de investigación:",
                placeholder="Ej: competencias digitales resiliencia entornos automatizados",
                help="Describe tu tema de investigación con palabras clave específicas"
            )
        
        with col_search2:
            contexto = st.text_input(
                "🎯 Contexto específico:",
                placeholder="Ej: educación superior América Latina",
                help="Especifica el contexto o enfoque particular"
            )
        
        # Selección de bases de datos
        st.subheader("Selecciona las bases de datos:")
        col_db1, col_db2 = st.columns(2)
        
        with col_db1:
            usar_semantic = st.checkbox("Semantic Scholar", value=True,
                                      help="Artículos en inglés e internacionales")
        with col_db2:
            usar_scielo = st.checkbox("SciELO", value=True,
                                    help="Revistas científicas de América Latina")
        
        if st.button("🔍 Ejecutar Búsqueda", type="primary", use_container_width=True):
            if not consulta:
                st.error("📌 Por favor ingresa un tema de investigación")
            else:
                with st.spinner("🔍 Buscando en bases académicas..."):
                    # Ejecutar búsquedas
                    articulos_encontrados = []
                    
                    if usar_semantic:
                        with st.expander("🌐 Semantic Scholar", expanded=True):
                            resultados_ss = buscar_semantic_scholar(consulta, 5)
                            articulos_encontrados.extend(resultados_ss)
                            st.success(f"📄 Encontrados: {len(resultados_ss)} artículos")
                            for art in resultados_ss:
                                st.write(f"- **{art['titulo']}**")
                    
                    if usar_scielo:
                        with st.expander("🌎 SciELO", expanded=True):
                            resultados_scielo = buscar_scielo(consulta, 5)
                            articulos_encontrados.extend(resultados_scielo)
                            st.success(f"📄 Encontrados: {len(resultados_scielo)} artículos")
                            for art in resultados_scielo:
                                st.write(f"- **{art['titulo']}**")
                    
                    # Guardar resultados
                    st.session_state.articulos = articulos_encontrados
                    st.session_state.consulta_actual = consulta
                    st.session_state.contexto_actual = contexto
                    
                    if articulos_encontrados:
                        st.success(f"✅ Búsqueda completada! Se encontraron {len(articulos_encontrados)} artículos")
                        
                        # Generar y mostrar resumen
                        with st.expander("🤖 Resumen y Análisis", expanded=True):
                            texto_articulos = preparar_texto_para_gemini(articulos_encontrados)
                            if texto_articulos.strip():
                                resumen = resumir_articulos_con_gemini(texto_articulos)
                                st.markdown(resumen)
                                st.session_state.resumen_actual = resumen
                    else:
                        st.warning("No se encontraron artículos con los criterios especificados.")
    
    # Pestaña de Chat con Agente
    with tab4:
        st.markdown("### 💬 Chat Inteligente con el Agente de Investigación")
        
        st.info("""
        🎯 **Pregunta naturalmente sobre:**
        - Planteamientos de problemas de investigación
        - Objetivos y metodologías
        - Análisis de datos y variables
        - Redacción académica y referencias
        
        💡 **Ejemplo:** *"Formula el planteamiento del problema sobre competencias digitales en entornos automatizados"*
        """)
        
        # Configuración de contexto
        contexto_actual = st.text_input(
            "🎯 Contexto de investigación (opcional):",
            placeholder="Ej: educación superior en Latinoamérica",
            help="Proporciona contexto para respuestas más precisas"
        )
        
        # Mostrar historial de chat
        for mensaje in st.session_state.chat_history:
            with st.chat_message(mensaje["role"]):
                st.markdown(mensaje["content"])
        
        # Input de chat
        if prompt := st.chat_input("Escribe tu pregunta sobre investigación..."):
            # Agregar mensaje del usuario
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Respuesta del agente MEJORADO
            with st.chat_message("assistant"):
                with st.spinner("🤔 Analizando tu consulta..."):
                    respuesta = chat_con_agente(
                        st.session_state.agente, 
                        prompt, 
                        contexto_actual
                    )
                    st.markdown(respuesta)
            
            # Agregar respuesta al historial
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        
        # Botones de acción
        col_chat1, col_chat2 = st.columns(2)
        with col_chat1:
            if st.button("🗑️ Limpiar Conversación", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.agente.limpiar_memoria()
                st.rerun()
        
        with col_chat2:
            if st.button("💡 Ejemplo de Planteamiento", use_container_width=True):
                ejemplo = "Formula el planteamiento del problema sobre competencias digitales para la resiliencia en entornos automatizados con IA"
                st.session_state.chat_history.append({"role": "user", "content": ejemplo})
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Generando ejemplo..."):
                        respuesta = chat_con_agente(
                            st.session_state.agente, 
                            ejemplo, 
                            "entornos laborales digitalizados"
                        )
                        st.markdown(respuesta)
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
    
    # Pestaña de Exportar Resultados
    with tab3:
        st.markdown("### 📤 Exportar Resultados de Investigación")
        
        if not st.session_state.articulos:
            st.warning("📌 No hay resultados para exportar. Realiza primero una búsqueda.")
        else:
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                st.subheader("📚 Artículos Encontrados")
                
                # Exportar CSV
                campos_csv = ["titulo", "autor", "año", "publicacion", "fuente", "url"]
                articulos_exportar = []
                
                for art in st.session_state.articulos:
                    articulos_exportar.append({
                        "titulo": art.get("titulo", ""),
                        "autor": art.get("autor", ""),
                        "año": art.get("año", "s.f."),
                        "publicacion": art.get("publicacion", ""),
                        "fuente": art.get("fuente", ""),
                        "url": art.get("url", "")
                    })
                
                # Crear CSV en memoria
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=campos_csv)
                writer.writeheader()
                for item in articulos_exportar:
                    writer.writerow(item)
                csv_data = output.getvalue()
                
                st.download_button(
                    label="📥 Descargar Artículos (CSV)",
                    data=csv_data,
                    file_name=f"articulos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_exp2:
                st.subheader("📖 Bibliografía")
                
                # Generar bibliografía
                referencias = []
                for art in st.session_state.articulos:
                    ref = {
                        "autor": art["autor"],
                        "año": art["año"] if art["año"] else "s.f.",
                        "titulo": art["titulo"],
                        "publicacion": art["publicacion"],
                        "url": art["url"],
                    }
                    referencias.append(ref)
                
                bibliografia_apa = generar_bibliografia(referencias, estilo="APA")
                
                st.download_button(
                    label="📚 Bibliografia APA (TXT)",
                    data=bibliografia_apa,
                    file_name="bibliografia_APA.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown("---")
            st.subheader("📊 Estadísticas de Exportación")
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            
            with col_stats1:
                st.metric("Artículos", len(st.session_state.articulos))
            
            with col_stats2:
                fuentes = set(art['fuente'] for art in st.session_state.articulos)
                st.metric("Fuentes", len(fuentes))
            
            with col_stats3:
                st.metric("Formatos", "CSV, TXT")

if __name__ == "__main__":
    main()
