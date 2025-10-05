import streamlit as st
import re

# Configuración básica
st.set_page_config(
    page_title="Asistente de Investigación",
    page_icon="🔬",
    layout="wide"
)

# Título principal
st.title("🔬 Asistente de Investigación Académica")
st.success("✅ **Sistema funcionando correctamente**")

# Función simple para generar respuestas
def generar_respuesta(tema, tipo):
    if tipo == "planteamiento":
        return f"""
## 🎯 PLANTEAMIENTO DEL PROBLEMA: {tema}

### 📝 Descripción
La rápida evolución tecnológica ha creado nuevos desafíos en {tema}. Existe una brecha entre las demandas actuales y las capacidades existentes.

### 🔍 Justificación
- **Relevancia actual**: Tema crucial en la transformación digital
- **Impacto social**: Afecta a diversos grupos y comunidades
- **Vacío investigativo**: Necesidad de estudios actualizados

### ❓ Preguntas de Investigación
1. ¿Qué factores influyen en {tema}?
2. ¿Qué impacto tiene {tema} en el contexto actual?
3. ¿Qué estrategias podrían optimizar {tema}?
"""
    elif tipo == "objetivos":
        return f"""
## 🎯 OBJETIVOS: {tema}

### Objetivo General
Analizar los aspectos de {tema} para proponer mejoras e innovaciones.

### Objetivos Específicos
1. Identificar componentes clave de {tema}
2. Diagnosticar el estado actual
3. Evaluar el impacto en diferentes contextos
4. Proponer estrategias de optimización
"""
    else:
        return f"""
## 💡 ASESORÍA: {tema}

### Enfoques Recomendados
- **Investigación exploratoria**: Para caracterizar el fenómeno
- **Investigación explicativa**: Para identificar relaciones
- **Investigación aplicada**: Para desarrollar soluciones

### Próximos Pasos
1. Búsqueda bibliográfica
2. Definir marco teórico  
3. Establecer preguntas de investigación
4. Seleccionar metodología
"""

# Chat principal
st.header("💬 Chat con el Asistente")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del chat
if prompt := st.chat_input("Escribe tu pregunta..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Determinar tipo de solicitud
    prompt_lower = prompt.lower()
    if any(palabra in prompt_lower for palabra in ['planteamiento', 'problema']):
        tipo = "planteamiento"
    elif any(palabra in prompt_lower for palabra in ['objetivos', 'metas']):
        tipo = "objetivos"
    else:
        tipo = "general"
    
    # Extraer tema
    tema = prompt
    for palabra in ['formula', 'planteamiento', 'problema', 'objetivos', 'genera', 'crea']:
        tema = tema.replace(palabra, '')
    tema = tema.strip()
    
    # Generar respuesta
    respuesta = generar_respuesta(tema, tipo)
    
    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

# Ejemplos rápidos
st.header("🚀 Ejemplos Rápidos")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧩 Planteamiento Ejemplo"):
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("🎯 Objetivos Ejemplo"):
        st.session_state.messages = []
        st.rerun()

with col3:
    if st.button("🔍 Metodología Ejemplo"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("🔬 **Asistente de Investigación** - Versión Simple y Funcional")
