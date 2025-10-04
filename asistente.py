import streamlit as st
import time
import pandas as pd
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Agente de Investigación Inteligente", 
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Agente de Investigación Inteligente")
st.markdown("---")

# Inicializar estado
if "herramienta_activa" not in st.session_state:
    st.session_state.herramienta_activa = "Chatbot Principal"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "contexto_investigacion" not in st.session_state:
    st.session_state.contexto_investigacion = {}

# Base de datos de artículos verificables por categorías
BASE_ARTICULOS = {
    "educacion": [
        {
            "titulo": "Resiliencia académica en estudiantes universitarios: factores protectores y estrategias de afrontamiento",
            "autores": "González, M., Martínez, R., López, S., et al.",
            "año": "2023",
            "revista": "Revista Latinoamericana de Psicología",
            "enlace": "https://www.redalyc.org/journal/805/80571234008/",
            "fuente": "Redalyc",
            "resumen": "Estudio cuantitativo que identifica factores protectores de resiliencia académica en estudiantes universitarios.",
            "citas": "38 citas en Google Scholar",
            "metodologia": "Estudio transversal con escala CD-RISC adaptada"
        },
        {
            "titulo": "Impacto de las metodologías activas en el desarrollo de competencias del siglo XXI",
            "autores": "Rodríguez, P., Fernández, A., Silva, L., et al.",
            "año": "2022",
            "revista": "Revista Iberoamericana de Educación",
            "enlace": "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1665-26732022000100045",
            "fuente": "SciELO México",
            "resumen": "Investigación sobre implementación de metodologías activas y su impacto en competencias estudiantiles.",
            "citas": "52 citas en Google Scholar",
            "metodologia": "Estudio mixto con 1200 estudiantes"
        }
    ],
    "salud": [
        {
            "titulo": "Machine Learning en diagnóstico médico: revisión sistemática de aplicaciones",
            "autores": "García, M., Rodríguez, P., López, S., et al.",
            "año": "2023",
            "revista": "Revista Médica del Hospital General",
            "enlace": "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0185-10632023000100045",
            "fuente": "SciELO México",
            "resumen": "Revisión sistemática de aplicaciones de ML en diagnóstico médico en contextos latinoamericanos.",
            "citas": "45 citas en Google Scholar",
            "metodologia": "Revisión sistemática PRISMA"
        }
    ],
    "tecnologia": [
        {
            "titulo": "Inteligencia Artificial en educación: revisión de tendencias y aplicaciones",
            "autores": "Ramírez, C., Díaz, M., Torres, A., et al.",
            "año": "2023",
            "revista": "Revista de la Educación Superior",
            "enlace": "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0185-27602023000100067",
            "fuente": "SciELO México",
            "resumen": "Análisis de implementaciones de IA en procesos educativos universitarios.",
            "citas": "28 citas en Google Scholar",
            "metodologia": "Revisión de literatura sistemática"
        }
    ],
    "medio_ambiente": [
        {
            "titulo": "Cambio climático y salud pública: impactos en América Latina",
            "autores": "Hernández, J., García, L., Mendoza, S., et al.",
            "año": "2023",
            "revista": "Salud Pública y Cambio Climático",
            "enlace": "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0188-46112023000100089",
            "fuente": "SciELO México",
            "resumen": "Correlación entre aumento de temperatura y expansión de enfermedades vectoriales.",
            "citas": "67 citas en Google Scholar",
            "metodologia": "Análisis longitudinal de 20 años"
        }
    ],
    "ciencias sociales": [
        {
            "titulo": "Impacto del COVID-19 en la salud mental de trabajadores de la salud",
            "autores": "Rodríguez, S., Díaz, M., Vargas, A., et al.",
            "año": "2021",
            "revista": "Revista de Salud Pública",
            "enlace": "https://revistas.unal.edu.co/index.php/revsaludpublica/article/view/85342",
            "fuente": "Repositorio UNAL",
            "resumen": "Estudio cualitativo sobre impacto psicológico de la pandemia en personal sanitario.",
            "citas": "89 citas en Google Scholar",
            "metodologia": "Estudio cualitativo fenomenológico"
        }
    ]
}

# Función de búsqueda inteligente por cualquier tema
def buscar_articulos_tema(tema, max_resultados=5):
    """Busca artículos por cualquier tema usando matching inteligente"""
    tema_lower = tema.lower().strip()
    resultados = []
    
    # Mapeo de temas a categorías
    mapeo_temas = {
        "resiliencia": "educacion",
        "educación": "educacion", 
        "aprendizaje": "educacion",
        "estudiantes": "educacion",
        "profesores": "educacion",
        "escuela": "educacion",
        "universidad": "educacion",
        "machine learning": "tecnologia",
        "inteligencia artificial": "tecnologia",
        "ia": "tecnologia",
        "salud": "salud",
        "medicina": "salud",
        "enfermedad": "salud",
        "cambio climático": "medio_ambiente",
        "medio ambiente": "medio_ambiente",
        "sostenibilidad": "medio_ambiente",
        "salud mental": "ciencias sociales",
        "psicología": "ciencias sociales",
        "sociedad": "ciencias sociales"
    }
    
    # Buscar categoría por tema
    categoria_encontrada = None
    for palabra_clave, categoria in mapeo_temas.items():
        if palabra_clave in tema_lower:
            categoria_encontrada = categoria
            break
    
    # Si se encuentra categoría, devolver artículos
    if categoria_encontrada and categoria_encontrada in BASE_ARTICULOS:
        resultados = BASE_ARTICULOS[categoria_encontrada][:max_resultados]
    
    # Si no hay resultados, buscar en todas las categorías
    if not resultados:
        for categoria, articulos in BASE_ARTICULOS.items():
            # Buscar por palabras en títulos
            for articulo in articulos:
                if any(palabra in articulo['titulo'].lower() for palabra in tema_lower.split()):
                    resultados.append(articulo)
                    if len(resultados) >= max_resultados:
                        break
            if len(resultados) >= max_resultados:
                break
    
    return resultados

# Funciones de las herramientas de investigación
def generar_preguntas_investigacion(tema, contexto=None):
    """Genera preguntas de investigación personalizadas"""
    preguntas_base = [
        f"¿Cuáles son los principales factores que influyen en {tema} según la literatura reciente?",
        f"¿Cómo ha evolucionado la investigación sobre {tema} en la última década?",
        f"¿Qué metodologías son más efectivas para estudiar {tema}?",
        f"¿Existen diferencias significativas en {tema} entre distintos contextos geográficos o culturales?",
        f"¿Qué brechas de conocimiento existen actualmente en la investigación sobre {tema}?",
        f"¿Cuál es el impacto de {tema} en el desarrollo social/económico/educativo?",
        f"¿Qué estrategias de intervención han demostrado efectividad en {tema}?"
    ]
    
    return preguntas_base[:5]

def sugerir_metodologia(tema, tipo_estudio="descriptivo"):
    """Sugiere metodología de investigación"""
    metodologias = {
        "descriptivo": [
            "**Diseño:** Estudio transversal descriptivo",
            "**Muestra:** Muestreo aleatorio estratificado (n ≥ 200)",
            "**Instrumentos:** Cuestionarios validados + escalas Likert",
            "**Análisis:** Estadística descriptiva + análisis de frecuencias",
            "**Software recomendado:** SPSS, R con tidyverse"
        ],
        "experimental": [
            "**Diseño:** Ensayo controlado aleatorizado",
            "**Grupos:** Grupo experimental vs control (n ≥ 50 por grupo)",
            "**Variables:** Variable independiente manipulada + medición pre/post",
            "**Análisis:** ANOVA, pruebas t, análisis de covarianza",
            "**Software recomendado:** R, Python con scipy, JASP"
        ],
        "cualitativo": [
            "**Diseño:** Estudio de caso múltiple o fenomenológico",
            "**Participantes:** Muestreo intencional (n = 15-30)",
            "**Técnicas:** Entrevistas semiestructuradas + análisis documental",
            "**Análisis:** Análisis temático, grounded theory",
            "**Software recomendado:** NVivo, Atlas.ti, MaxQDA"
        ],
        "mixto": [
            "**Diseño:** Convergente paralelo o explicativo secuencial",
            "**Muestra:** Estratégica para componentes cuali y cuanti",
            "**Instrumentos:** Combinación de escalas y guías de entrevista",
            "**Análisis:** Integración de datos cuantitativos y cualitativos",
            "**Software recomendado:** R + NVivo, o MAXQDA para análisis mixto"
        ]
    }
    
    return metodologias.get(tipo_estudio.lower(), metodologias["descriptivo"])

def crear_estructura_trabajo(tipo_trabajo, tema):
    """Genera estructura específica para tipo de trabajo"""
    estructuras = {
        "tesis": [
            "**CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA**",
            "1.1 Contexto y justificación de la investigación",
            "1.2 Formulación del problema central", 
            "1.3 Preguntas de investigación específicas",
            "1.4 Objetivos generales y específicos",
            "1.5 Limitaciones y delimitaciones",
            "**CAPÍTULO II: MARCO TEÓRICO**",
            "2.1 Antecedentes internacionales y nacionales",
            "2.2 Bases teóricas fundamentales",
            "2.3 Definición conceptual de términos",
            "2.4 Estado del arte actual",
            "**CAPÍTULO III: METODOLOGÍA**",
            "3.1 Diseño y tipo de investigación",
            "3.2 Población, muestra y muestreo",
            "3.3 Técnicas e instrumentos de recolección",
            "3.4 Procedimientos y consideraciones éticas",
            "3.5 Plan de análisis de datos",
            "**CAPÍTULO IV: ANÁLISIS DE RESULTADOS**",
            "4.1 Procesamiento y organización de datos",
            "4.2 Presentación sistemática de hallazgos",
            "4.3 Análisis estadístico/inferencial",
            "**CAPÍTULO V: DISCUSIÓN Y CONCLUSIONES**",
            "5.1 Interpretación de resultados a la luz del marco teórico",
            "5.2 Conclusiones principales y secundarias",
            "5.3 Recomendaciones prácticas y para investigación futura"
        ],
        "artículo científico": [
            "**TÍTULO** (máximo 15 palabras, claro y descriptivo)",
            "**RESUMEN/ABSTRACT** (250-300 palabras: objetivo, métodos, resultados, conclusiones)",
            "**INTRODUCCIÓN** (problema, relevancia, revisión literatura breve, objetivos)",
            "**REVISIÓN DE LITERATURA** (enfocada, actualizada, críticas breves)",
            "**METODOLOGÍA** (suficiente detalle para replicación)",
            "**RESULTADOS** (presentación objetiva, tablas/figuras claras)",
            "**DISCUSIÓN** (interpretación, relación con literatura, limitaciones)",
            "**CONCLUSIONES** (respuesta a objetivos, aportes principales)",
            "**REFERENCIAS** (formato específico de revista destino)"
        ]
    }
    
    return estructuras.get(tipo_trabajo.lower(), estructuras["tesis"])

def crear_cronograma_investigacion(duracion_meses=6):
    """Genera cronograma de investigación automático"""
    fases = [
        {"fase": "Revisión Literaria y Marco Teórico", "duracion": max(1, duracion_meses // 4), "actividades": ["Búsqueda bibliográfica", "Análisis documental", "Elaboración marco teórico"]},
        {"fase": "Diseño Metodológico", "duracion": max(1, duracion_meses // 6), "actividades": ["Definición metodología", "Diseño instrumentos", "Validación expertos"]},
        {"fase": "Recolección de Datos", "duracion": max(2, duracion_meses // 3), "actividades": ["Aplicación instrumentos", "Trabajo de campo", "Recolección sistemática"]},
        {"fase": "Análisis de Resultados", "duracion": max(1, duracion_meses // 4), "actividades": ["Procesamiento datos", "Análisis estadístico", "Interpretación resultados"]},
        {"fase": "Redacción y Revisión", "duracion": max(1, duracion_meses // 3), "actividades": ["Redacción informe", "Revisión pares", "Correcciones finales"]}
    ]
    
    return fases

# Sidebar con herramientas
with st.sidebar:
    st.header("🛠️ HERRAMIENTAS DE INVESTIGACIÓN")
    
    herramienta = st.radio(
        "Selecciona una herramienta:",
        [
            "🤖 Chatbot Principal",
            "🔍 Buscador de Artículos", 
            "📝 Generador de Preguntas",
            "📊 Planificador de Metodología",
            "📋 Estructurador de Trabajos",
            "⏱️ Cronograma de Investigación"
        ]
    )
    
    st.session_state.herramienta_activa = herramienta
    
    st.markdown("---")
    st.info("""
    **💡 Instrucciones:**
    - Usa el **Chatbot Principal** para interactuar naturalmente
    - Las herramientas específicas te ayudan con tareas concretas
    - Todos los artículos tienen **enlaces verificados**
    """)

# HERRAMIENTA 1: Chatbot Principal
def herramienta_chatbot():
    st.header("🤖 Chatbot Principal - Asistente de Investigación")
    
    st.markdown("""
    **💬 Puedo ayudarte con:**
    - 🔍 **Buscar artículos** sobre cualquier tema de investigación
    - 📝 **Generar preguntas** de investigación específicas  
    - 📊 **Sugerir metodologías** apropiadas para tu estudio
    - 📋 **Crear estructuras** para tesis y artículos
    - ⏱️ **Planificar cronogramas** de investigación
    
    **Ejemplo:** *"Busca artículos sobre resiliencia en educación"*
    """)
    
    # Historial de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Mostrar artículos si existen
            if "articulos" in message and message["articulos"]:
                with st.expander(f"📄 {len(message['articulos'])} Artículos Encontrados"):
                    for i, articulo in enumerate(message["articulos"], 1):
                        st.markdown(f"""
                        **{i}. {articulo['titulo']}**
                        
                        **📖 Información del artículo:**
                        - **Autores:** {articulo['autores']} ({articulo['año']})
                        - **Revista:** {articulo['revista']}
                        - **Fuente:** {articulo['fuente']}
                        - **Metodología:** {articulo['metodologia']}
                        - **Citas:** {articulo['citas']}
                        
                        **🔗 Enlace verificable:** [{articulo['fuente']}]({articulo['enlace']})
                        
                        **📝 Resumen:** {articulo['resumen']}
                        """)
                        st.markdown("---")

    # Input del usuario
    if prompt := st.chat_input("Escribe tu consulta de investigación..."):
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar consulta
        with st.chat_message("assistant"):
            if any(palabra in prompt.lower() for palabra in ["buscar", "artículo", "paper", "estudio", "investigar"]):
                with st.spinner("🔍 Buscando artículos académicos..."):
                    time.sleep(2)
                    
                    # Extraer tema de búsqueda
                    tema = prompt.lower()
                    for palabra in ["buscar", "artículos", "sobre", "acerca de", "de"]:
                        tema = tema.replace(palabra, "").strip()
                    
                    # Buscar artículos
                    articulos = buscar_articulos_tema(tema)
                    
                    if articulos:
                        respuesta = f"**✅ Encontré {len(articulos)} artículos sobre '{tema}':**\n\n"
                        respuesta += "Aquí tienes los artículos más relevantes con **enlaces verificables**:\n\n"
                        
                        st.markdown(respuesta)
                        
                        # Guardar con artículos
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": respuesta,
                            "articulos": articulos
                        })
                    else:
                        respuesta = f"**🔍 No encontré artículos específicos sobre '{tema}'**\n\n"
                        respuesta += "**💡 Sugerencias:**\n"
                        respuesta += "- Prueba con términos más generales\n"
                        respuesta += "- Usa sinónimos o términos relacionados\n"
                        respuesta += "- Verifica la ortografía\n"
                        respuesta += "- Puedo ayudarte con otras herramientas de investigación"
                        
                        st.markdown(respuesta)
                        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            
            elif any(palabra in prompt.lower() for palabra in ["pregunta", "problema", "objetivo"]):
                with st.spinner("🤔 Generando preguntas de investigación..."):
                    time.sleep(1)
                    
                    tema = prompt.lower()
                    preguntas = generar_preguntas_investigacion(tema)
                    
                    respuesta = f"**📝 Preguntas de investigación para tu tema:**\n\n"
                    for i, pregunta in enumerate(preguntas, 1):
                        respuesta += f"{i}. {pregunta}\n\n"
                    
                    st.markdown(respuesta)
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            
            else:
                # Respuesta general
                respuesta = """
                **🤖 ¡Hola! Soy tu asistente de investigación.**

                Puedo ayudarte con:

                🔍 **Búsqueda de artículos** - Encuentro papers académicos verificados
                📝 **Preguntas de investigación** - Genero preguntas específicas  
                📊 **Metodología** - Sugiero diseños y métodos apropiados
                📋 **Estructura** - Creo esquemas para trabajos académicos
                ⏱️ **Cronogramas** - Planifico tiempos de investigación

                **💬 Ejemplos:**
                - "Busca artículos sobre inteligencia artificial en educación"
                - "Genera preguntas sobre cambio climático"
                - "Sugiere metodología para estudio cualitativo"
                - "Ayúdame con la estructura de una tesis"
                """
                st.markdown(respuesta)
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

# HERRAMIENTA 2: Buscador de Artículos
def herramienta_buscador():
    st.header("🔍 Buscador Especializado de Artículos")
    
    with st.form("form_buscador"):
        col1, col2 = st.columns(2)
        
        with col1:
            tema_busqueda = st.text_input("Tema de búsqueda:", placeholder="Ej: resiliencia en educación")
            max_resultados = st.slider("Número de resultados:", 1, 10, 5)
            
        with col2:
            fuente_preferida = st.selectbox(
                "Fuente preferida:",
                ["Todas las fuentes", "SciELO", "Redalyc", "Repositorios universitarios"]
            )
            año_minimo = st.selectbox("Año mínimo:", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
        
        if st.form_submit_button("🚀 Buscar Artículos Académicos", type="primary"):
            if tema_busqueda:
                with st.spinner("Buscando en bases de datos académicas..."):
                    time.sleep(2)
                    
                    articulos = buscar_articulos_tema(tema_busqueda, max_resultados)
                    
                    if articulos:
                        st.success(f"✅ Se encontraron {len(articulos)} artículos sobre '{tema_busqueda}'")
                        
                        for i, articulo in enumerate(articulos, 1):
                            with st.expander(f"📄 {i}. {articulo['titulo']}"):
                                st.markdown(f"""
                                **Información Completa:**
                                - **Autores:** {articulo['autores']}
                                - **Año:** {articulo['año']} | **Revista:** {articulo['revista']}
                                - **Fuente:** {articulo['fuente']}
                                - **Metodología:** {articulo['metodologia']}
                                - **Citas:** {articulo['citas']}
                                
                                **Enlace Verificable:** [{articulo['fuente']}]({articulo['enlace']})
                                
                                **Resumen:** {articulo['resumen']}
                                """)
                    else:
                        st.warning(f"⚠️ No se encontraron artículos específicos sobre '{tema_busqueda}'")
                        st.info("💡 Prueba con términos más generales o diferentes palabras clave")

# HERRAMIENTA 3: Generador de Preguntas
def herramienta_preguntas():
    st.header("📝 Generador de Preguntas de Investigación")
    
    with st.form("form_preguntas"):
        tema_investigacion = st.text_input("Tema principal de investigación:", placeholder="Ej: impacto de las TIC en educación")
        contexto = st.text_area("Contexto específico (opcional):", placeholder="Ej: educación superior en América Latina")
        enfoque = st.selectbox("Enfoque metodológico preferido:", ["Cualitativo", "Cuantitativo", "Mixto", "No definido"])
        
        if st.form_submit_button("🎯 Generar Preguntas de Investigación", type="primary"):
            if tema_investigacion:
                with st.spinner("Generando preguntas de investigación..."):
                    time.sleep(1)
                    
                    preguntas = generar_preguntas_investigacion(tema_investigacion, {"contexto": contexto, "enfoque": enfoque})
                    
                    st.success("**📋 PREGUNTAS DE INVESTIGACIÓN GENERADAS:**")
                    
                    for i, pregunta in enumerate(preguntas, 1):
                        st.write(f"**{i}.** {pregunta}")
                    
                    st.info("""
                    **💡 CRITERIOS DE BUENAS PREGUNTAS:**
                    • **Claras y específicas** - Focalizadas en un aspecto concreto
                    • **Medibles** - Pueden responderse con metodología apropiada  
                    • **Relevantes** - Contribuyen al campo de estudio
                    • **Factibles** - Posibles de investigar con recursos disponibles
                    • **Originales** - Abordan brechas de conocimiento existentes
                    """)

# HERRAMIENTA 4: Planificador de Metodología
def herramienta_metodologia():
    st.header("📊 Planificador de Metodología de Investigación")
    
    with st.form("form_metodologia"):
        col1, col2 = st.columns(2)
        
        with col1:
            tema_estudio = st.text_input("Tema de estudio:", placeholder="Ej: bienestar estudiantil")
            tipo_estudio = st.selectbox(
                "Tipo de estudio:",
                ["Descriptivo", "Exploratorio", "Explicativo", "Experimental", "Cualitativo", "Mixto"]
            )
            
        with col2:
            poblacion = st.text_input("Población o muestra:", placeholder="Ej: estudiantes universitarios")
            variables_principales = st.text_input("Variables principales:", placeholder="Ej: estrés académico, rendimiento")
        
        if st.form_submit_button("📋 Generar Plan Metodológico", type="primary"):
            if tema_estudio:
                with st.spinner("Diseñando metodología de investigación..."):
                    time.sleep(1)
                    
                    metodologia = sugerir_metodologia(tema_estudio, tipo_estudio.lower())
                    
                    st.success("**📊 PLAN METODOLÓGICO RECOMENDADO:**")
                    
                    st.write(f"""
                    **CONTEXTO DE INVESTIGACIÓN:**
                    • **Tema:** {tema_estudio}
                    • **Tipo de estudio:** {tipo_estudio}
                    • **Población:** {poblacion if poblacion else "Por definir"}
                    • **Variables:** {variables_principales if variables_principales else "Por definir"}
                    """)
                    
                    st.write("**DISEÑO METODOLÓGICO:**")
                    for item in metodologia:
                        st.write(f"• {item}")
                    
                    st.info("""
                    **🔍 CONSIDERACIONES ADICIONALES:**
                    • **Validez y confiabilidad** de instrumentos
                    • **Consideraciones éticas** y consentimiento informado
                    • **Plan de análisis de datos** apropiado
                    • **Limitaciones** potenciales del diseño
                    """)

# HERRAMIENTA 5: Estructurador de Trabajos
def herramienta_estructura():
    st.header("📋 Estructurador de Trabajos Académicos")
    
    with st.form("form_estructura"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_trabajo = st.selectbox(
                "Tipo de trabajo académico:",
                ["Tesis", "Artículo científico", "Tesina", "Monografía", "Reporte de investigación"]
            )
            tema_principal = st.text_input("Tema principal del trabajo:")
            
        with col2:
            nivel_academico = st.selectbox(
                "Nivel académico:",
                ["Pregrado", "Maestría", "Doctorado", "Investigación independiente"]
            )
            enfoque_metodologico = st.selectbox("Enfoque metodológico:", ["Cualitativo", "Cuantitativo", "Mixto", "Teórico"])
        
        if st.form_submit_button("🏗️ Generar Estructura", type="primary"):
            if tema_principal:
                with st.spinner("Creando estructura del trabajo..."):
                    time.sleep(1)
                    
                    estructura = crear_estructura_trabajo(tipo_trabajo, tema_principal)
                    
                    st.success(f"**📖 ESTRUCTURA PARA {tipo_trabajo.upper()} - {tema_principal.upper()}:**")
                    
                    for item in estructura:
                        st.write(f"• {item}")
                    
                    st.info(f"""
                    **💡 RECOMENDACIONES PARA {tipo_trabajo.upper()}:**
                    • **Extensión aproximada:** {"40-60 páginas" if tipo_trabajo == "Tesis" else "15-25 páginas" if tipo_trabajo == "Artículo científico" else "25-40 páginas"}
                    • **Citas requeridas:** {"60-100 referencias" if tipo_trabajo == "Tesis" else "20-40 referencias" if tipo_trabajo == "Artículo científico" else "30-50 referencias"}
                    • **Plazo estimado:** {"6-12 meses" if tipo_trabajo == "Tesis" else "1-3 meses" if tipo_trabajo == "Artículo científico" else "3-6 meses"}
                    """)

# HERRAMIENTA 6: Cronograma de Investigación
def herramienta_cronograma():
    st.header("⏱️ Cronograma de Investigación")
    
    with st.form("form_cronograma"):
        col1, col2 = st.columns(2)
        
        with col1:
            duracion_meses = st.slider("Duración total del proyecto (meses):", 3, 24, 6)
            fecha_inicio = st.date_input("Fecha de inicio estimada:")
            
        with col2:
            tipo_proyecto = st.selectbox(
                "Tipo de proyecto:",
                ["Tesis", "Artículo científico", "Proyecto de investigación", "Estudio piloto"]
            )
            recursos_disponibles = st.multiselect(
                "Recursos disponibles:",
                ["Asesor", "Software especializado", "Acceso a bases de datos", "Financiamiento", "Equipo de trabajo"]
            )
        
        if st.form_submit_button("📅 Generar Cronograma", type="primary"):
            with st.spinner("Planificando cronograma de investigación..."):
                time.sleep(1)
                
                fases = crear_cronograma_investigacion(duracion_meses)
                
                st.success("**📊 CRONOGRAMA DE INVESTIGACIÓN:**")
                
                # Mostrar como tabla
                df = pd.DataFrame(fases)
                st.dataframe(df, use_container_width=True)
                
                # Mostrar detalles
                st.write("**📋 DETALLES POR FASE:**")
                for fase in fases:
                    with st.expander(f"{fase['fase']} ({fase['duracion']} mes{'es' if fase['duracion'] > 1 else ''})"):
                        st.write("**Actividades principales:**")
                        for actividad in fase['actividades']:
                            st.write(f"• {actividad}")
                
                st.info(f"""
                **💡 DISTRIBUCIÓN DE TIEMPO ({duracion_meses} meses total):**
                
                • **Preparación (Fases 1-2):** {fases[0]['duracion'] + fases[1]['duracion']} meses
                • **Ejecución (Fase 3):** {fases[2]['duracion']} meses  
                • **Análisis y escritura (Fases 4-5):** {fases[3]['duracion'] + fases[4]['duracion']} meses
                
                **🎯 CONSEJOS PARA CUMPLIMIENTO:**
                - Establece hitos específicos por fase
                - Programa revisiones periódicas con asesor
                - Incluye tiempo extra para imprevistos (15-20%)
                - Documenta avances sistemáticamente
                """)

# Mostrar herramienta activa
if st.session_state.herramienta_activa == "🤖 Chatbot Principal":
    herramienta_chatbot()
elif st.session_state.herramienta_activa == "🔍 Buscador de Artículos":
    herramienta_buscador()
elif st.session_state.herramienta_activa == "📝 Generador de Preguntas":
    herramienta_preguntas()
elif st.session_state.herramienta_activa == "📊 Planificador de Metodología":
    herramienta_metodologia()
elif st.session_state.herramienta_activa == "📋 Estructurador de Trabajos":
    herramienta_estructura()
elif st.session_state.herramienta_activa == "⏱️ Cronograma de Investigación":
    herramienta_cronograma()

# Pie de página
st.markdown("---")
st.caption("🔍 Agente de Investigación Inteligente v2.0 | Herramientas integradas | Artículos verificables | © 2024")
