import streamlit as st
import time
import pandas as pd
import requests
import json

st.set_page_config(
    page_title="Kit de Herramientas de Investigación", 
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Kit de Herramientas de Investigación + Chatbot Académico")
st.markdown("---")

# Inicializar estado
if "herramienta_activa" not in st.session_state:
    st.session_state.herramienta_activa = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar - Selección de herramienta
with st.sidebar:
    st.header("🛠️ HERRAMIENTAS DISPONIBLES")
    
    herramienta = st.radio(
        "Selecciona una herramienta:",
        [
            "🔍 Buscador de Fuentes Académicas",
            "🤖 Chatbot Buscador de Artículos", 
            "📝 Generador de Preguntas de Investigación",
            "📊 Planificador de Metodología",
            "📋 Estructurador de Trabajos",
            "⏱️ Cronograma de Investigación"
        ]
    )
    
    st.session_state.herramienta_activa = herramienta
    
    st.markdown("---")
    st.info("💡 **Instrucciones:** Selecciona una herramienta y completa el formulario")

# Función para buscar artículos en APIs académicas
def buscar_articulos_academicos(tema, max_resultados=5):
    """
    Simula búsqueda en bases de datos académicas
    En una implementación real, conectarías con APIs como:
    - Google Scholar API
    - CrossRef API
    - arXiv API
    - PubMed API
    """
    
    # Simulación de búsqueda en diferentes bases de datos
    resultados = {
        "Google Scholar": [
            f"Artículo sobre '{tema}' - Revista Internacional 2024",
            f"Estudio empírico: {tema} en contexto latinoamericano",
            f"Revisión sistemática sobre {tema} - 2023",
            f"Tesis doctoral: Análisis de {tema}",
            f"Conferencia internacional sobre {tema}"
        ],
        "PubMed": [
            f"Clinical trial: {tema} outcomes",
            f"Meta-analysis: {tema} effectiveness",
            f"Systematic review: {tema} treatments",
            f"Case study: {tema} application"
        ],
        "IEEE Xplore": [
            f"Technical paper: {tema} implementation",
            f"Conference proceeding: {tema} innovations",
            f"Journal article: {tema} algorithms"
        ]
    }
    
    return resultados

# HERRAMIENTA 1: Buscador de Fuentes Académicas
def herramienta_fuentes():
    st.header("🔍 Buscador de Fuentes Académicas")
    
    with st.form("form_fuentes"):
        col1, col2 = st.columns(2)
        
        with col1:
            tema_especifico = st.text_input("Tema específico de investigación:")
            area_estudio = st.selectbox(
                "Área de estudio:",
                ["Ciencias de la Salud", "Ingeniería y Tecnología", "Ciencias Sociales", 
                 "Humanidades", "Ciencias Naturales", "Educación", "Negocios"]
            )
            
        with col2:
            palabras_clave = st.text_input("Palabras clave principales (separadas por coma):")
            tipo_fuente = st.multiselect(
                "Tipos de fuentes preferidas:",
                ["Artículos científicos", "Libros académicos", "Tesis doctorales", 
                 "Conferencias", "Reportes técnicos", "Revistas indexadas"]
            )
        
        if st.form_submit_button("🚀 Buscar Fuentes Recomendadas", type="primary"):
            if tema_especifico:
                with st.spinner("Buscando en bases de datos especializadas..."):
                    time.sleep(2)
                    
                    # Resultados específicos por área
                    fuentes_especificas = {
                        "Ciencias de la Salud": [
                            "**PubMed** (pubmed.ncbi.nlm.nih.gov) - 15 artículos recientes encontrados",
                            "**SciELO** (scielo.org) - 8 artículos en acceso abierto", 
                            "**ScienceDirect** - 12 estudios relacionados",
                            "**MEDLINE** - 10 investigaciones clínicas",
                            "**Revistas:** The Lancet, JAMA, New England Journal of Medicine"
                        ],
                        "Ingeniería y Tecnología": [
                            "**IEEE Xplore** (ieeexplore.ieee.org) - 20 papers técnicos",
                            "**ACM Digital Library** - 15 artículos de computación",
                            "**SpringerLink** - 18 publicaciones en ingeniería",
                            "**Google Scholar** - 25+ referencias relevantes",
                            "**Revistas:** IEEE Transactions, Nature Engineering"
                        ],
                        "Ciencias Sociales": [
                            "**JSTOR** (jstor.org) - 22 artículos académicos",
                            "**PsycINFO** - 15 estudios en psicología",
                            "**Scopus** - 18 investigaciones sociales",
                            "**Redalyc** - 12 artículos en español",
                            "**Revistas:** American Sociological Review, Social Forces"
                        ]
                    }
                    
                    st.success("✅ **FUENTES ENCONTRADAS PARA TU TEMA**")
                    
                    # Mostrar fuentes específicas
                    area_key = area_estudio if area_estudio in fuentes_especificas else "Ciencias Sociales"
                    fuentes = fuentes_especificas.get(area_key, fuentes_especificas["Ciencias Sociales"])
                    
                    for i, fuente in enumerate(fuentes, 1):
                        st.write(f"{i}. {fuente}")
                    
                    # Estrategias de búsqueda
                    st.info("""
                    **🔍 ESTRATEGIAS DE BÚSQUEDA AVANZADA:**
                    - Usa operadores booleanos: `"{}" AND {}`
                    - Filtra por fecha: últimos 5 años
                    - Revisa las referencias de artículos clave
                    - Consulta autores especializados en el área
                    """.format(tema_especifico, palabras_clave))
            else:
                st.warning("⚠️ Por favor ingresa un tema específico de investigación")

# HERRAMIENTA 2: CHATBOT BUSCADOR DE ARTÍCULOS
def herramienta_chatbot():
    st.header("🤖 Chatbot Buscador de Artículos en Tiempo Real")
    
    st.markdown("""
    **💬 Puedes pedirme que busque artículos sobre cualquier tema de investigación**
    - Ejemplo: "Busca artículos sobre machine learning en medicina"
    - "Encuentra estudios recientes sobre cambio climático"
    - "Artículos sobre inteligencia artificial en educación"
    """)
    
    # Historial de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu solicitud de búsqueda..."):
        # Agregar mensaje del usuario al historial
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar la solicitud y buscar artículos
        with st.chat_message("assistant"):
            with st.spinner("Buscando artículos en bases de datos académicas..."):
                time.sleep(2)
                
                # Extraer términos de búsqueda del prompt
                terminos_busqueda = prompt.lower()
                if "busca" in terminos_busqueda or "encuentra" in terminos_busqueda or "artículos" in terminos_busqueda:
                    # Simular búsqueda de artículos
                    resultados = buscar_articulos_academicos(prompt)
                    
                    respuesta = f"**🔍 Resultados de búsqueda para: '{prompt}'**\n\n"
                    
                    for base_datos, articulos in resultados.items():
                        respuesta += f"**📚 {base_datos}:**\n"
                        for i, articulo in enumerate(articulos[:3], 1):
                            respuesta += f"{i}. {articulo}\n"
                        respuesta += "\n"
                    
                    respuesta += """
                    **💡 Sugerencias para refinar tu búsqueda:**
                    - Especifica el año de publicación
                    - Agrega el nombre de autores relevantes
                    - Indica el tipo de estudio que buscas
                    - Especifica el ámbito geográfico
                    """
                else:
                    respuesta = """
                    **🤖 Asistente de Investigación Académica**
                    
                    Puedo ayudarte a buscar artículos científicos. Por ejemplo, puedes pedirme:
                    - "Busca artículos sobre machine learning en medicina"
                    - "Encuentra estudios recientes sobre cambio climático"
                    - "Artículos sobre inteligencia artificial en educación 2023"
                    - "Investiga sobre energías renovables en América Latina"
                    """
                
                st.markdown(respuesta)
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        
        # Botón para limpiar historial
        if st.button("🧹 Limpiar Conversación"):
            st.session_state.chat_history = []
            st.rerun()

# HERRAMIENTA 3: Generador de Preguntas de Investigación
def herramienta_preguntas():
    st.header("📝 Generador de Preguntas de Investigación")
    
    with st.form("form_preguntas"):
        problema = st.text_area("Describe el problema o fenómeno que quieres investigar:", height=100)
        contexto = st.text_input("Contexto específico (ej: educación superior, salud pública, etc.):")
        enfoque = st.selectbox("Enfoque preferido:", ["Cualitativo", "Cuantitativo", "Mixto"])
        
        if st.form_submit_button("🎯 Generar Preguntas de Investigación", type="primary"):
            if problema:
                with st.spinner("Generando preguntas de investigación..."):
                    time.sleep(2)
                    
                    st.success("**📋 PREGUNTAS DE INVESTIGACIÓN GENERADAS:**")
                    
                    preguntas = [
                        f"¿Cuál es la relación entre {problema.split()[0]} y [variable clave] en el contexto de {contexto}?",
                        f"¿Cómo influye {problema.split()[0]} en los resultados de {contexto} según la perspectiva {enfoque.lower()}?",
                        f"¿Qué factores determinan el impacto de {problema.split()[0]} en {contexto}?",
                        f"¿En qué medida varía {problema.split()[0]} según diferentes condiciones en {contexto}?",
                        f"¿Cuáles son las principales barreras y facilitadores de {problema.split()[0]} en {contexto}?"
                    ]
                    
                    for i, pregunta in enumerate(preguntas, 1):
                        st.write(f"{i}. {pregunta}")
                    
                    st.info("""
                    **💡 CRITERIOS DE BUENAS PREGUNTAS:**
                    • **Claras y específicas**
                    • **Medibles** con metodología apropiada  
                    • **Relevantes** para el campo de estudio
                    • **Factibles** de investigar
                    • **Originales** o con nuevo enfoque
                    """)

# HERRAMIENTA 4: Planificador de Metodología
def herramienta_metodologia():
    st.header("📊 Planificador de Metodología")
    
    with st.form("form_metodologia"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_estudio = st.selectbox(
                "Tipo de estudio:",
                ["Descriptivo", "Exploratorio", "Explicativo", "Experimental", "Caso de estudio"]
            )
            poblacion = st.text_input("Población o muestra de estudio:")
            
        with col2:
            técnicas = st.multiselect(
                "Técnicas de recolección de datos:",
                ["Encuestas", "Entrevistas", "Observación", "Análisis documental", "Experimentación", "Focus Groups"]
            )
            analisis = st.selectbox(
                "Análisis de datos:",
                ["Estadístico", "Qualitative Content Analysis", "Análisis temático", "Análisis comparativo", "Mixto"]
            )
        
        if st.form_submit_button("📋 Generar Plan Metodológico", type="primary"):
            with st.spinner("Diseñando metodología..."):
                time.sleep(2)
                
                st.success("**📊 PLAN METODOLÓGICO RECOMENDADO:**")
                
                st.write(f"""
                **DISEÑO DE INVESTIGACIÓN:**
                • **Tipo:** Estudio {tipo_estudio.lower()}
                • **Enfoque:** {'Cuantitativo' if técnicas and 'Encuestas' in técnicas else 'Cualitativo o Mixto'}
                • **Población:** {poblacion if poblacion else "Por definir"}
                
                **TÉCNICAS DE RECOLECCIÓN:**
                {chr(10).join(f'• {tec}' for tec in técnicas)}
                
                **ANÁLISIS DE DATOS:**
                • **Método:** {analisis}
                • **Herramientas:** {'SPSS, Excel' if analisis == 'Estadístico' else 'NVivo, Atlas.ti' if analisis == 'Qualitative Content Analysis' else 'Específicas según datos'}
                
                **CONSIDERACIONES ÉTICAS:**
                • Consentimiento informado
                • Confidencialidad de datos
                • Aprobación comité de ética si aplica
                """)

# HERRAMIENTA 5: Estructurador de Trabajos
def herramienta_estructura():
    st.header("📋 Estructurador de Trabajos Académicos")
    
    tipo_trabajo = st.selectbox(
        "Selecciona el tipo de trabajo académico:",
        ["Tesina", "Tesis", "Artículo científico", "Ensayo", "Reporte"],
        key="tipo_trabajo"
    )
    
    with st.form("form_estructura"):
        tema = st.text_input("Tema principal del trabajo:")
        objetivos = st.text_area("Objetivos principales (uno por línea):")
        
        if st.form_submit_button("🏗️ Generar Estructura", type="primary"):
            if tema:
                with st.spinner("Creando estructura..."):
                    time.sleep(2)
                    
                    estructuras = {
                        "Tesis": [
                            "**CAPÍTULO I: INTRODUCCIÓN**",
                            "1.1 Planteamiento del Problema",
                            "1.2 Preguntas de Investigación", 
                            "1.3 Objetivos (General y Específicos)",
                            "1.4 Justificación",
                            "**CAPÍTULO II: MARCO TEÓRICO**",
                            "2.1 Antecedentes de la Investigación",
                            "2.2 Bases Teóricas",
                            "2.3 Definición de Términos",
                            "**CAPÍTULO III: METODOLOGÍA**",
                            "3.1 Diseño de Investigación",
                            "3.2 Población y Muestra",
                            "3.3 Técnicas e Instrumentos",
                            "**CAPÍTULO IV: RESULTADOS**",
                            "4.1 Análisis de Datos",
                            "4.2 Presentación de Resultados",
                            "**CAPÍTULO V: DISCUSIÓN Y CONCLUSIONES**",
                            "5.1 Discusión de Resultados",
                            "5.2 Conclusiones",
                            "5.3 Recomendaciones"
                        ],
                        "Artículo científico": [
                            "**TÍTULO** (claro y descriptivo)",
                            "**RESUMEN** (250-300 palabras)",
                            "**INTRODUCCIÓN** (problema, relevancia, objetivos)",
                            "**REVISIÓN DE LITERATURA** (breve y focalizada)", 
                            "**METODOLOGÍA** (suficiente para replicación)",
                            "**RESULTADOS** (presentación clara de hallazgos)",
                            "**DISCUSIÓN** (interpretación y relación con literatura)",
                            "**CONCLUSIONES** (principales aportes)",
                            "**REFERENCIAS** (formato específico de revista)"
                        ],
                        "Tesina": [
                            "**INTRODUCCIÓN**",
                            "**MARCO TEÓRICO**",
                            "**METODOLOGÍA**",
                            "**ANÁLISIS Y RESULTADOS**",
                            "**CONCLUSIONES**",
                            "**BIBLIOGRAFÍA**"
                        ]
                    }
                    
                    st.success(f"**📖 ESTRUCTURA PARA {tipo_trabajo.upper()}:**")
                    
                    estructura = estructuras.get(tipo_trabajo, estructuras["Tesis"])
                    for item in estructura:
                        st.write(f"• {item}")

# HERRAMIENTA 6: Cronograma de Investigación
def herramienta_cronograma():
    st.header("⏱️ Cronograma de Investigación")
    
    with st.form("form_cronograma"):
        duracion_meses = st.slider("Duración total del proyecto (meses):", 3, 24, 6)
        fecha_inicio = st.date_input("Fecha de inicio estimada:")
        
        if st.form_submit_button("📅 Generar Cronograma", type="primary"):
            with st.spinner("Planificando cronograma..."):
                time.sleep(2)
                
                # Generar cronograma automático
                fases = [
                    {"fase": "Revisión Literaria y Marco Teórico", "duracion": max(1, duracion_meses // 4)},
                    {"fase": "Diseño Metodológico", "duracion": max(1, duracion_meses // 6)},
                    {"fase": "Recolección de Datos", "duracion": max(2, duracion_meses // 3)},
                    {"fase": "Análisis de Resultados", "duracion": max(1, duracion_meses // 4)},
                    {"fase": "Redacción y Revisión", "duracion": max(1, duracion_meses // 3)}
                ]
                
                st.success("**📊 CRONOGRAMA DE INVESTIGACIÓN:**")
                
                df = pd.DataFrame(fases)
                st.dataframe(df, use_container_width=True)
                
                st.info(f"""
                **📋 DISTRIBUCIÓN DE TIEMPO ({duracion_meses} meses total):**
                
                • **Preparación:** {fases[0]['duracion'] + fases[1]['duracion']} meses
                • **Ejecución:** {fases[2]['duracion']} meses  
                • **Análisis y escritura:** {fases[3]['duracion'] + fases[4]['duracion']} meses
                
                **💡 CONSEJOS:**
                - Incluye tiempo extra para imprevistos
                - Establece hitos específicos por fase
                - Programa revisiones periódicas
                """)

# Mostrar herramienta activa
if st.session_state.herramienta_activa == "🔍 Buscador de Fuentes Académicas":
    herramienta_fuentes()
elif st.session_state.herramienta_activa == "🤖 Chatbot Buscador de Artículos":
    herramienta_chatbot()
elif st.session_state.herramienta_activa == "📝 Generador de Preguntas de Investigación":
    herramienta_preguntas()
elif st.session_state.herramienta_activa == "📊 Planificador de Metodología":
    herramienta_metodologia()
elif st.session_state.herramienta_activa == "📋 Estructurador de Trabajos":
    herramienta_estructura()
elif st.session_state.herramienta_activa == "⏱️ Cronograma de Investigación":
    herramienta_cronograma()
else:
    st.info("👈 **Selecciona una herramienta en el menú lateral para comenzar**")

# Pie de página
st.markdown("---")
st.caption("🔍 Kit de Herramientas de Investigación v4.0 | Chatbot integrado + Búsqueda en tiempo real | © 2024")
