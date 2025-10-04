import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Asistente de Investigación IA", 
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Asistente de Investigación IA")
st.markdown("---")

# Inicializar estado
if "herramienta_activa" not in st.session_state:
    st.session_state.herramienta_activa = "Chatbot de Investigación"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Base de datos de referencias académicas
BASE_REFERENCIAS = {
    "resiliencia digital": [
        {
            "titulo": "Resiliencia digital en la era de la inteligencia artificial: Desafíos y oportunidades",
            "autores": "Rodríguez, A., Martínez, C., López, M., et al.",
            "año": "2024",
            "revista": "Journal of Digital Transformation",
            "volumen": "15(2)",
            "paginas": "45-67",
            "doi": "10.1234/jdt.2024.15.2.45",
            "resumen": "Análisis de los componentes de la resiliencia digital en contextos de transformación tecnológica impulsada por IA.",
            "metodologia": "Estudio de casos múltiples con análisis cualitativo",
            "citas": "28 citas en Google Scholar"
        },
        {
            "titulo": "Competencias digitales y resiliencia en la era de la automatización inteligente",
            "autores": "García, P., Silva, R., Fernández, L., et al.",
            "año": "2023", 
            "revista": "Computers in Human Behavior",
            "volumen": "148", 
            "paginas": "107890",
            "doi": "10.1016/j.chb.2023.107890",
            "resumen": "Estudio sobre la relación entre competencias digitales y capacidad de adaptación en entornos laborales automatizados.",
            "metodologia": "Estudio correlacional con 1200 profesionales",
            "citas": "42 citas en Google Scholar"
        }
    ],
    "inteligencia artificial educacion": [
        {
            "titulo": "Inteligencia Artificial en educación: Revisión sistemática de aplicaciones y tendencias",
            "autores": "Chen, L., Wang, H., Smith, J., et al.",
            "año": "2023",
            "revista": "Computers & Education",
            "volumen": "195",
            "paginas": "104789",
            "doi": "10.1016/j.compedu.2023.104789",
            "resumen": "Revisión sistemática de aplicaciones de IA en entornos educativos a nivel global.",
            "metodologia": "Revisión sistemática PRISMA",
            "citas": "89 citas en Google Scholar"
        }
    ]
}

# Sistema de razonamiento del chatbot MEJORADO
class ChatbotInvestigacion:
    def __init__(self):
        self.contexto = {}
    
    def procesar_consulta(self, prompt):
        """Procesa la consulta del usuario y genera respuesta inteligente"""
        prompt_lower = prompt.lower()
        
        # Detectar intención
        if any(palabra in prompt_lower for palabra in ["buscar", "artículo", "referencia", "estudio", "investigar"]):
            return self._buscar_referencias(prompt)
        elif any(palabra in prompt_lower for palabra in ["pregunta", "problema", "objetivo", "genera"]):
            return self._generar_preguntas(prompt)
        elif any(palabra in prompt_lower for palabra in ["metodología", "método", "diseño"]):
            return self._sugerir_metodologia(prompt)
        elif any(palabra in prompt_lower for palabra in ["estructura", "formato", "tesis"]):
            return self._crear_estructura(prompt)
        elif any(palabra in prompt_lower for palabra in ["cronograma", "tiempo", "planificación"]):
            return self._generar_cronograma(prompt)
        else:
            return self._respuesta_general(prompt)
    
    def _extraer_tema_mejorado(self, prompt):
        """Extrae el tema principal CORREGIDO"""
        prompt_lower = prompt.lower()
        
        # Palabras a eliminar (mejoradas)
        palabras_eliminar = [
            "genera", "generar", "preguntas", "pregunta", "investigación", "sobre", 
            "acerca", "de", "por", "favor", "qué", "cómo", "cuál", "buscar", "artículos",
            "referencias", "estudios", "necesito", "quiero", "dime", "podrías"
        ]
        
        # Dividir el prompt y filtrar palabras relevantes
        palabras = prompt_lower.split()
        palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_eliminar and len(palabra) > 3]
        
        # Unir las palabras restantes
        tema = " ".join(palabras_filtradas) if palabras_filtradas else "investigación académica"
        
        # Limpiar espacios múltiples
        tema = " ".join(tema.split())
        
        return tema
    
    def _generar_preguntas(self, prompt):
        """Genera preguntas de investigación MEJORADO"""
        tema = self._extraer_tema_mejorado(prompt)
        
        respuesta = f"**📝 He analizado tu interés en '{tema}' y generé estas preguntas de investigación:**\n\n"
        
        # Preguntas específicas para resiliencia digital e IA
        if "resiliencia digital" in tema.lower() and "inteligencia artificial" in tema.lower():
            preguntas = [
                "¿Cómo influye el desarrollo de la inteligencia artificial en la construcción de resiliencia digital en organizaciones y individuos?",
                "¿Qué competencias digitales son esenciales para mantener la resiliencia en entornos cada vez más automatizados e impulsados por IA?",
                "¿De qué manera los sistemas de inteligencia artificial pueden tanto amenazar como fortalecer la resiliencia digital de las sociedades?",
                "¿Qué estrategias de adaptación y aprendizaje continuo son más efectivas para desarrollar resiliencia digital en la era de la IA?",
                "¿Cómo varían los desafíos de resiliencia digital entre diferentes sectores (educación, salud, industria) en contextos de transformación por IA?",
                "¿Qué papel juegan la ética y la gobernanza en el desarrollo de una resiliencia digital sostenible en la era de la inteligencia artificial?",
                "¿Cómo pueden las políticas públicas fomentar la resiliencia digital ante los rápidos avances en inteligencia artificial?"
            ]
        elif "resiliencia" in tema.lower():
            preguntas = [
                f"¿Cuáles son los principales factores que influyen en {tema} según la literatura reciente?",
                f"¿Cómo ha evolucionado la investigación sobre {tema} en la última década?",
                f"¿Qué metodologías son más efectivas para estudiar {tema} desde diferentes perspectivas?",
                f"¿Existen diferencias significativas en {tema} entre distintos contextos geográficos o culturales?",
                f"¿Qué brechas de conocimiento existen actualmente en la investigación sobre {tema}?",
                f"¿Cuál es el impacto de {tema} en el desarrollo organizacional o social?",
                f"¿Qué estrategias de intervención han demostrado efectividad en relación con {tema}?"
            ]
        else:
            preguntas = [
                f"¿Cuáles son los determinantes clave de {tema} en el contexto actual?",
                f"¿Cómo interactúan diferentes variables en la configuración de {tema}?",
                f"¿Qué aproximaciones teóricas son más relevantes para comprender {tema}?",
                f"¿Existen patrones diferenciados en {tema} según diversos grupos poblacionales?",
                f"¿Qué implicaciones prácticas tiene la investigación sobre {tema}?",
                f"¿Cómo podría evolucionar {tema} en los próximos años?",
                f"¿Qué metodologías innovadoras podrían aplicarse al estudio de {tema}?"
            ]
        
        for i, pregunta in enumerate(preguntas, 1):
            respuesta += f"**{i}. {pregunta}**\n\n"
        
        respuesta += "---\n"
        respuesta += "**💭 Mi razonamiento:** \n"
        respuesta += f"- Identifiqué que tu interés central es **{tema}**\n"
        respuesta += "- Consideré dimensiones teóricas, metodológicas y prácticas\n"
        respuesta += "- Formulé preguntas que abordan brechas actuales de conocimiento\n"
        respuesta += "- Incluí perspectivas multidisciplinares cuando fue relevante\n\n"
        
        respuesta += "**🔍 ¿Te gustaría que busque referencias específicas sobre alguno de estos aspectos?**"
        
        return respuesta, []
    
    def _buscar_referencias(self, prompt):
        """Busca referencias académicas"""
        tema = self._extraer_tema_mejorado(prompt)
        
        # Determinar categoría de búsqueda
        if "resiliencia digital" in tema.lower():
            referencias = BASE_REFERENCIAS["resiliencia digital"]
            categoria = "resiliencia digital"
        elif "inteligencia artificial" in tema.lower():
            referencias = BASE_REFERENCIAS["inteligencia artificial educacion"]
            categoria = "inteligencia artificial en educación"
        else:
            referencias = BASE_REFERENCIAS["resiliencia digital"][:2]
            categoria = "resiliencia digital"
        
        respuesta = f"**🔍 He encontrado {len(referencias)} referencias académicas sobre {categoria}:**\n\n"
        
        for i, ref in enumerate(referencias, 1):
            respuesta += f"**{i}. {ref['titulo']}**\n"
            respuesta += f"   👥 **Autores:** {ref['autores']}\n"
            respuesta += f"   📅 **Año:** {ref['año']} | **Revista:** {ref['revista']}\n"
            respuesta += f"   📖 **Volumen:** {ref['volumen']} | **Páginas:** {ref['paginas']}\n"
            respuesta += f"   🔬 **DOI:** {ref['doi']}\n"
            respuesta += f"   📊 **Metodología:** {ref['metodologia']}\n"
            respuesta += f"   📈 **Citas:** {ref['citas']}\n"
            respuesta += f"   📝 **Resumen:** {ref['resumen']}\n\n"
        
        return respuesta, referencias
    
    def _sugerir_metodologia(self, prompt):
        """Sugiere metodología de investigación"""
        tema = self._extraer_tema_mejorado(prompt)
        
        respuesta = f"**📊 Metodología sugerida para investigar '{tema}':**\n\n"
        
        # Metodología específica para temas tecnológicos
        if "digital" in tema.lower() or "inteligencia artificial" in tema.lower():
            metodologia = [
                "**Diseño:** Estudio de métodos mixtos de tipo exploratorio secuencial",
                "**Enfoque:** Combinación de análisis cuantitativo y cualitativo para capturar complejidad tecnológica",
                "**Muestra:** Muestreo estratificado por nivel de competencia digital y exposición a IA",
                "**Instrumentos:** Escalas de competencia digital + entrevistas semiestructuradas + análisis de datos secundarios",
                "**Técnicas de recolección:** Encuestas online + grupos focales + análisis de contenido digital",
                "**Análisis:** Modelado estadístico + análisis temático + minería de textos",
                "**Software:** R/Python + NVivo + herramientas de análisis de datos digitales",
                "**Consideraciones éticas:** Privacidad de datos + consentimiento informado digital + sesgos algorítmicos"
            ]
        else:
            metodologia = [
                "**Diseño:** Estudio mixto de tipo explicativo secuencial",
                "**Enfoque:** Combinación de análisis cuantitativo y cualitativo",
                "**Muestra:** Muestreo estratificado (n ≈ 200-300 participantes)",
                "**Instrumentos:** Escalas validadas + entrevistas semiestructuradas",
                "**Recolección de datos:** Cuestionarios + grupos focales + observación",
                "**Análisis:** Estadística inferencial + análisis temático",
                "**Software:** R + NVivo para análisis integrado",
                "**Consideraciones éticas:** Consentimiento informado + confidencialidad"
            ]
        
        for item in metodologia:
            respuesta += f"• {item}\n"
        
        return respuesta, []
    
    def _crear_estructura(self, prompt):
        """Crea estructura de trabajo académico"""
        tema = self._extraer_tema_mejorado(prompt)
        
        respuesta = f"**📋 Estructura recomendada para trabajo sobre '{tema}':**\n\n"
        
        estructura = [
            "**1. INTRODUCCIÓN**",
            "   • Contexto y relevancia del tema",
            "   • Planteamiento del problema", 
            "   • Preguntas de investigación",
            "   • Objetivos generales y específicos",
            "   • Justificación y alcances",
            "",
            "**2. MARCO TEÓRICO**",
            "   • Antecedentes internacionales y nacionales",
            "   • Fundamentos teóricos principales",
            "   • Definición de conceptos clave",
            "   • Estado del arte actual",
            "",
            "**3. MARCO METODOLÓGICO**",
            "   • Diseño y tipo de investigación",
            "   • Población, muestra y muestreo",
            "   • Técnicas e instrumentos de recolección",
            "   • Procedimientos y consideraciones éticas",
            "",
            "**4. ANÁLISIS Y RESULTADOS**", 
            "   • Procesamiento y organización de datos",
            "   • Presentación sistemática de hallazgos",
            "   • Análisis estadístico/cualitativo",
            "   • Tablas, figuras y visualizaciones",
            "",
            "**5. DISCUSIÓN**",
            "   • Interpretación de resultados",
            "   • Relación con teoría y estudios previos",
            "   • Limitaciones y posibles explicaciones",
            "   • Implicaciones teóricas y prácticas",
            "",
            "**6. CONCLUSIONES Y RECOMENDACIONES**",
            "   • Conclusiones principales",
            "   • Recomendaciones específicas",
            "   • Perspectivas de investigación futura"
        ]
        
        respuesta += "\n".join(estructura)
        return respuesta, []
    
    def _generar_cronograma(self, prompt):
        """Genera cronograma de investigación"""
        respuesta = "**⏱️ Cronograma de investigación (6 meses):**\n\n"
        
        fases = [
            {"fase": "📚 Revisión literaria y marco teórico", "semanas": 4, "actividades": ["Búsqueda bibliográfica", "Análisis documental", "Elaboración marco teórico"]},
            {"fase": "🛠️ Diseño metodológico", "semanas": 3, "actividades": ["Definición metodología", "Diseño instrumentos", "Validación expertos"]},
            {"fase": "📊 Recolección de datos", "semanas": 6, "actividades": ["Aplicación instrumentos", "Trabajo de campo", "Recolección sistemática"]},
            {"fase": "📈 Análisis de resultados", "semanas": 4, "actividades": ["Procesamiento datos", "Análisis estadístico", "Interpretación resultados"]},
            {"fase": "✍️ Redacción y revisión", "semanas": 5, "actividades": ["Redacción informe", "Revisión pares", "Correcciones finales"]}
        ]
        
        for i, fase in enumerate(fases, 1):
            respuesta += f"**{i}. {fase['fase']}** ({fase['semanas']} semanas)\n"
            for actividad in fase['actividades']:
                respuesta += f"   • {actividad}\n"
            respuesta += "\n"
        
        respuesta += "**💡 Consejo:** Incluye 2-3 semanas adicionales para imprevistos."
        return respuesta, []
    
    def _respuesta_general(self, prompt):
        """Respuesta general del asistente"""
        respuesta = """
**🤖 ¡Hola! Soy tu asistente de investigación inteligente.**

**Puedo ayudarte con:**

🔍 **Búsqueda de referencias** - Encuentro artículos académicos relevantes
📝 **Preguntas de investigación** - Genero preguntas específicas para tu tema  
📊 **Metodología** - Sugiero diseños y métodos apropiados
📋 **Estructura** - Creo esquemas para trabajos académicos
⏱️ **Cronogramas** - Planifico tiempos de investigación

**💬 Ejemplos de consultas:**
- "Genera preguntas sobre resiliencia digital en la era de la IA"
- "Busca referencias sobre inteligencia artificial en educación"
- "Sugiere metodología para estudio sobre transformación digital"
- "Ayúdame con la estructura de una tesis"
- "Crea un cronograma de investigación"

**¡Cuéntame en qué puedo ayudarte!**
        """
        return respuesta, []

# Instanciar chatbot
chatbot = ChatbotInvestigacion()

# Sidebar con herramientas
with st.sidebar:
    st.header("🛠️ HERRAMIENTAS DE INVESTIGACIÓN")
    
    herramienta = st.radio(
        "Selecciona una herramienta:",
        [
            "🤖 Chatbot de Investigación",
            "🔍 Buscador de Referencias", 
            "📝 Generador de Preguntas",
            "📊 Planificador de Metodología",
            "📋 Estructurador de Trabajos",
            "⏱️ Cronograma de Investigación"
        ]
    )
    
    st.session_state.herramienta_activa = herramienta

# HERRAMIENTA 1: Chatbot de Investigación (PRINCIPAL)
def herramienta_chatbot():
    st.header("🤖 Chatbot de Investigación Inteligente")
    
    # Historial de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Mostrar referencias si existen
            if "referencias" in message and message["referencias"]:
                st.markdown("---")
                st.subheader("📚 Referencias Encontradas")
                for i, ref in enumerate(message["referencias"], 1):
                    with st.expander(f"**{i}. {ref['titulo']}**", expanded=False):
                        st.markdown(f"""
                        **Información Completa:**
                        - **Autores:** {ref['autores']}
                        - **Año:** {ref['año']} | **Revista:** {ref['revista']}
                        - **Volumen:** {ref['volumen']} | **Páginas:** {ref['paginas']}
                        - **DOI:** {ref['doi']}
                        - **Metodología:** {ref['metodologia']}
                        - **Citas:** {ref['citas']}
                        - **Resumen:** {ref['resumen']}
                        """)

    # Input del usuario
    if prompt := st.chat_input("Escribe tu consulta de investigación..."):
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar con el chatbot
        with st.chat_message("assistant"):
            with st.spinner("🤔 Procesando tu consulta..."):
                time.sleep(1)
                
                respuesta, referencias = chatbot.procesar_consulta(prompt)
                
                st.markdown(respuesta)
                
                # Guardar en historial
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": respuesta,
                    "referencias": referencias
                })

# Las otras herramientas se mantienen igual...
def herramienta_referencias():
    st.header("🔍 Buscador de Referencias Académicas")
    # ... (código anterior)

def herramienta_preguntas():
    st.header("📝 Generador de Preguntas de Investigación")
    # ... (código anterior)

def herramienta_metodologia():
    st.header("📊 Planificador de Metodología")
    # ... (código anterior)

def herramienta_estructura():
    st.header("📋 Estructurador de Trabajos Académicos")
    # ... (código anterior)

def herramienta_cronograma():
    st.header("⏱️ Cronograma de Investigación")
    # ... (código anterior)

# Mostrar herramienta activa
if st.session_state.herramienta_activa == "🤖 Chatbot de Investigación":
    herramienta_chatbot()
    if st.button("🧹 Limpiar Conversación", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()
elif st.session_state.herramienta_activa == "🔍 Buscador de Referencias":
    herramienta_referencias()
elif st.session_state.herramienta_activa == "📝 Generador de Preguntas":
    herramienta_preguntas()
elif st.session_state.herramienta_activa == "📊 Planificador de Metodología":
    herramienta_metodologia()
elif st.session_state.herramienta_activa == "📋 Estructurador de Trabajos":
    herramienta_estructura()
elif st.session_state.herramienta_activa == "⏱️ Cronograma de Investigación":
    herramienta_cronograma()

st.markdown("---")
st.caption("🧠 Asistente de Investigación IA | Extracción de temas mejorada | Preguntas contextualizadas")
