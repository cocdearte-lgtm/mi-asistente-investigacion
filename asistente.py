import streamlit as st
import time
import pandas as pd
import requests
import json

st.set_page_config(
    page_title="Chatbot Académico - Buscador de Investigación", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Chatbot Buscador de Artículos Académicos")
st.markdown("---")

# Inicializar estado del chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "busquedas_realizadas" not in st.session_state:
    st.session_state.busquedas_realizadas = []

# Función para buscar artículos en APIs académicas (simulada)
def buscar_articulos_academicos(tema, area_estudio=None, max_resultados=8):
    """
    Simula búsqueda en bases de datos académicas
    En una implementación real, conectarías con APIs reales
    """
    
    # Base de datos por área de estudio
    bases_datos = {
        "Ciencias de la Salud": [
            "PubMed (pubmed.ncbi.nlm.nih.gov)",
            "SciELO (scielo.org)", 
            "ScienceDirect",
            "MEDLINE",
            "Cochrane Library"
        ],
        "Ingeniería y Tecnología": [
            "IEEE Xplore (ieeexplore.ieee.org)",
            "ACM Digital Library",
            "SpringerLink",
            "Google Scholar",
            "ResearchGate"
        ],
        "Ciencias Sociales": [
            "JSTOR (jstor.org)",
            "PsycINFO",
            "Scopus",
            "Redalyc",
            "Dialnet"
        ],
        "Humanidades": [
            "Project MUSE",
            "Arts & Humanities Citation Index",
            "PhilPapers",
            "Persée",
            "DOAJ"
        ],
        "Ciencias Naturales": [
            "Nature Portfolio",
            "Science Magazine",
            "PLOS ONE",
            "BioMed Central",
            "ACS Publications"
        ]
    }
    
    # Artículos simulados por área
    articulos_por_area = {
        "Ciencias de la Salud": [
            f"Estudio clínico: '{tema}' - resultados preliminares 2024",
            f"Revisión sistemática: Efectividad de intervenciones en {tema}",
            f"Meta-análisis: {tema} y sus correlaciones epidemiológicas",
            f"Investigación traslacional: Aplicaciones prácticas de {tema}",
            f"Estudio observacional: Prevalencia de {tema} en población general",
            f"Ensayo controlado aleatorizado: {tema} vs tratamiento estándar",
            f"Estudio de cohorte: Factores de riesgo en {tema}",
            f"Investigación cualitativa: Experiencias de pacientes con {tema}"
        ],
        "Ingeniería y Tecnología": [
            f"Paper técnico: Implementación de algoritmos para {tema}",
            f"Estudio comparativo: Métodos de optimización en {tema}",
            f"Investigación aplicada: {tema} en sistemas industriales",
            f"Desarrollo experimental: Prototipo para {tema}",
            f"Análisis computacional: Simulaciones de {tema}",
            f"Revisión de estado del arte: Tendencias en {tema}",
            f"Estudio de caso: Aplicación de {tema} en contexto real",
            f"Investigación teórica: Fundamentos matemáticos de {tema}"
        ],
        "Ciencias Sociales": [
            f"Estudio cualitativo: Percepciones sobre {tema}",
            f"Investigación cuantitativa: Correlaciones en {tema}",
            f"Análisis de políticas: Impacto de {tema} en sociedad",
            f"Estudio longitudinal: Evolución de {tema} (2010-2024)",
            f"Investigación-acción: Intervenciones comunitarias en {tema}",
            f"Análisis discursivo: Representaciones sociales de {tema}",
            f"Estudio comparativo: {tema} en diferentes contextos culturales",
            f"Metodología mixta: Integración de perspectivas sobre {tema}"
        ]
    }
    
    # Seleccionar artículos según el área
    area = area_estudio if area_estudio in articulos_por_area else "Ciencias Sociales"
    articulos = articulos_por_area.get(area, articulos_por_area["Ciencias Sociales"])
    
    return {
        "bases_datos": bases_datos.get(area, bases_datos["Ciencias Sociales"]),
        "articulos": articulos[:max_resultados],
        "total_encontrado": f"~{len(articulos)*15} resultados en bases académicas"
    }

# Función para detectar área de estudio del texto
def detectar_area_estudio(texto):
    texto = texto.lower()
    areas = {
        "Ciencias de la Salud": ["medicina", "salud", "clínico", "hospital", "enfermedad", "tratamiento", "paciente", "fármaco"],
        "Ingeniería y Tecnología": ["ingeniería", "tecnología", "software", "hardware", "algoritmo", "programación", "sistema", "digital"],
        "Ciencias Sociales": ["social", "sociedad", "educación", "política", "cultura", "comportamiento", "comunidad", "psicología"],
        "Humanidades": ["literatura", "filosofía", "historia", "arte", "lingüística", "cultural", "humanidades"],
        "Ciencias Naturales": ["biología", "química", "física", "ambiente", "ecología", "naturaleza", "científico"]
    }
    
    for area, palabras_clave in areas.items():
        if any(palabra in texto for palabra in palabras_clave):
            return area
    return "General"

# Sidebar con información y ejemplos
with st.sidebar:
    st.header("🎯 Cómo usar el chatbot")
    
    st.markdown("""
    **💬 Ejemplos de búsquedas:**
    - "Busca artículos sobre machine learning en medicina"
    - "Encuentra estudios recientes sobre cambio climático"
    - "Artículos sobre inteligencia artificial en educación 2023"
    - "Investiga sobre energías renovables en América Latina"
    - "Búsqueda de papers sobre blockchain en finanzas"
    """)
    
    st.markdown("---")
    st.header("🔍 Áreas de Especialización")
    
    areas = [
        "🏥 Ciencias de la Salud",
        "⚙️ Ingeniería y Tecnología", 
        "👥 Ciencias Sociales",
        "📚 Humanidades",
        "🔬 Ciencias Naturales"
    ]
    
    for area in areas:
        st.write(f"• {area}")
    
    st.markdown("---")
    
    # Estadísticas de búsqueda
    if st.session_state.busquedas_realizadas:
        st.header("📊 Tus Búsquedas")
        for i, busqueda in enumerate(st.session_state.busquedas_realizadas[-5:], 1):
            st.write(f"{i}. {busqueda[:30]}...")
    
    # Botón para limpiar historial
    if st.button("🧹 Limpiar Todo el Historial"):
        st.session_state.chat_history = []
        st.session_state.busquedas_realizadas = []
        st.rerun()

# Área principal del chatbot
col1, col2 = st.columns([2, 1])

with col1:
    # Historial de chat
    st.subheader("💬 Conversación")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Mostrar metadatos si existen
            if "metadata" in message:
                with st.expander("📊 Detalles de la búsqueda"):
                    if "area_detectada" in message["metadata"]:
                        st.write(f"**Área detectada:** {message['metadata']['area_detectada']}")
                    if "total_resultados" in message["metadata"]:
                        st.write(f"**Resultados estimados:** {message['metadata']['total_resultados']}")
                    if "bases_recomendadas" in message["metadata"]:
                        st.write("**Bases de datos recomendadas:**")
                        for base in message["metadata"]["bases_recomendadas"][:3]:
                            st.write(f"• {base}")

    # Input del usuario
    if prompt := st.chat_input("Escribe tu solicitud de búsqueda (ej: 'artículos sobre machine learning')..."):
        # Agregar a historial de búsquedas
        st.session_state.busquedas_realizadas.append(prompt)
        
        # Agregar mensaje del usuario al historial
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar la solicitud y buscar artículos
        with st.chat_message("assistant"):
            with st.spinner("🔍 Buscando en bases de datos académicas..."):
                time.sleep(2)  # Simular tiempo de búsqueda
                
                # Detectar área de estudio
                area_detectada = detectar_area_estudio(prompt)
                
                # Realizar búsqueda
                resultados = buscar_articulos_academicos(prompt, area_detectada)
                
                # Construir respuesta
                respuesta = f"**🔍 Resultados de búsqueda para: '{prompt}'**\n\n"
                respuesta += f"*Área detectada: {area_detectada}*\n\n"
                
                respuesta += f"**📊 {resultados['total_encontrado']}**\n\n"
                
                respuesta += "**📚 Artículos académicos encontrados:**\n"
                for i, articulo in enumerate(resultados["articulos"][:6], 1):
                    respuesta += f"{i}. {articulo}\n"
                
                respuesta += "\n**🏛️ Bases de datos académicas recomendadas:**\n"
                for i, base in enumerate(resultados["bases_datos"][:4], 1):
                    respuesta += f"{i}. {base}\n"
                
                respuesta += "\n---\n"
                respuesta += """
                **💡 Sugerencias para refinar tu búsqueda:**
                - Especifica el año de publicación (ej: "2023-2024")
                - Agrega el nombre de autores relevantes
                - Indica el tipo de estudio que buscas (revisión, experimental, etc.)
                - Especifica el ámbito geográfico o población de interés
                - Usa comillas para búsquedas exactas: "aprendizaje automático"
                """
                
                st.markdown(respuesta)
                
                # Guardar mensaje con metadatos
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": respuesta,
                    "metadata": {
                        "area_detectada": area_detectada,
                        "total_resultados": resultados["total_encontrado"],
                        "bases_recomendadas": resultados["bases_datos"]
                    }
                })

with col2:
    st.subheader("🚀 Búsqueda Rápida")
    
    # Búsquedas predefinidas
    busquedas_rapidas = [
        "Machine Learning en salud",
        "Cambio climático 2024",
        "Inteligencia artificial educación",
        "Blockchain aplicaciones",
        "Energías renovables",
        "Psicología positiva",
        "Economía circular"
    ]
    
    for busqueda in busquedas_rapidas:
        if st.button(f"🔍 {busqueda}", key=busqueda):
            # Simular click en chat input
            st.session_state.busquedas_realizadas.append(busqueda)
            st.session_state.chat_history.append({"role": "user", "content": busqueda})
            st.rerun()
    
    st.markdown("---")
    st.subheader("📈 Estadísticas")
    
    st.metric(
        label="Búsquedas Realizadas", 
        value=len(st.session_state.busquedas_realizadas)
    )
    
    if st.session_state.busquedas_realizadas:
        areas_detectadas = [
            detectar_area_estudio(busqueda) 
            for busqueda in st.session_state.busquedas_realizadas
        ]
        area_comun = max(set(areas_detectadas), key=areas_detectadas.count)
        st.metric("Área más consultada", area_comun)

# Pie de página
st.markdown("---")
st.caption("🤖 Chatbot Académico v2.0 | Búsqueda inteligente en tiempo real | © 2024")
