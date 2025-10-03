import streamlit as st
import time
import pandas as pd

st.set_page_config(
    page_title="Asistente de Investigación AI", 
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Asistente de Investigación AI")
st.markdown("---")

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración del Proyecto")
    
    tema_investigacion = st.selectbox(
        "Área de investigación:", 
        ["Ciencias", "Tecnología", "Humanidades", "Salud", "Sociales", "Educación", "Negocios"]
    )
    
    nivel_academico = st.selectbox(
        "Nivel académico:",
        ["Pregrado", "Maestría", "Doctorado", "Investigación profesional"]
    )
    
    tipo_investigacion = st.selectbox(
        "Tipo de investigación:",
        ["Revisión literaria", "Estudio de caso", "Investigación experimental", "Análisis de datos"]
    )
    
    st.markdown("---")
    st.success("✅ Sistema listo")
    st.info("Complete el formulario para comenzar")

# Área principal de la aplicación
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Formulario de Investigación")
    
    with st.form("formulario_investigacion"):
        titulo_proyecto = st.text_input("Título del proyecto:")
        pregunta_principal = st.text_area(
            "Pregunta de investigación principal:",
            placeholder="Ej: ¿Cuál es el impacto de X en Y bajo condiciones Z?",
            height=80
        )
        
        objetivos = st.text_area(
            "Objetivos específicos:",
            placeholder="• Analizar...\n• Comparar...\n• Evaluar...",
            height=100
        )
        
        palabras_clave = st.text_input("Palabras clave (separadas por comas):")
        
        # Botón de envío
        submitted = st.form_submit_button("🚀 Iniciar Análisis de Investigación", type="primary")
        
        if submitted:
            if pregunta_principal and objetivos:
                with st.spinner(f"🔍 Analizando proyecto de {tema_investigacion}..."):
                    # Simulación de procesamiento
                    time.sleep(3)
                    
                    st.success("✅ Análisis completado!")
                    
                    # Resultados
                    st.subheader("📊 Plan de Investigación Generado")
                    
                    col_res1, col_res2 = st.columns(2)
                    
                    with col_res1:
                        st.info(f"""
                        **📋 METODOLOGÍA SUGERIDA:**
                        
                        • **Enfoque:** Investigación {tipo_investigacion.lower()}
                        • **Nivel:** {nivel_academico}
                        • **Área:** {tema_investigacion}
                        
                        **🔍 ESTRATEGIA DE BÚSQUEDA:**
                        - Bases de datos académicas especializadas
                        - Período: Últimos 5 años
                        - Criterios de inclusión/exclusión
                        """)
                    
                    with col_res2:
                        st.info(f"""
                        **📚 RECURSOS RECOMENDADOS:**
                        
                        • **Bases de datos:** 3 especializadas
                        • **Revistas:** 5 indexadas relevantes  
                        • **Metodologías:** 2 enfoques aplicables
                        • **Herramientas:** Software de análisis
                        """)
                    
                    # Timeline estimado
                    st.subheader("⏱️ Cronograma Estimado")
                    timeline_data = {
                        'Fase': ['Revisión literaria', 'Recolección datos', 'Análisis', 'Redacción'],
                        'Duración': ['2-3 semanas', '1-2 semanas', '1 semana', '2 semanas']
                    }
                    df_timeline = pd.DataFrame(timeline_data)
                    st.dataframe(df_timeline, use_container_width=True)
                    
            else:
                st.warning("⚠️ Complete la pregunta de investigación y los objetivos")

with col2:
    st.subheader("🛠️ Herramientas Disponibles")
    
    if st.button("📚 Buscar Literatura", use_container_width=True):
        st.info("🔍 Buscando en bases de datos académicas...")
        time.sleep(2)
        st.success("• 15 artículos relevantes encontrados\n• 3 revisiones sistemáticas\n• 5 estudios de caso")
    
    if st.button("📊 Analizar Datos", use_container_width=True):
        st.info("📈 Preparando herramientas de análisis...")
        time.sleep(2)
        st.success("Herramientas de estadística listas")
    
    if st.button("📝 Generar Reporte", use_container_width=True):
        st.info("🖋️ Generando estructura de reporte...")
        time.sleep(2)
        st.success("Plantilla de reporte creada")
    
    st.markdown("---")
    st.subheader("💡 Consejos")
    st.write("""
    • Sea específico en sus objetivos
    • Use palabras clave precisas
    • Defina claramente su metodología
    • Considere limitaciones desde el inicio
    """)

# Pie de página
st.markdown("---")
st.caption("🔍 Asistente de Investigación AI v2.0 | Desarrollado para apoyo académico | © 2024")