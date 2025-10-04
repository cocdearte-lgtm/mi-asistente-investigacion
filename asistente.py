import streamlit as st
import time
import random

st.set_page_config(
    page_title="Chatbot de Investigación AI", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Chatbot Asistente de Investigación")
st.markdown("---")

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente de investigación. ¿En qué tema necesitas ayuda?"}
    ]

# Sidebar con herramientas
with st.sidebar:
    st.header("🛠️ Herramientas de Investigación")
    
    area_investigacion = st.selectbox(
        "Área de tu investigación:",
        ["Ciencias", "Tecnología", "Humanidades", "Salud", "Sociales", "Educación", "Negocios", "Ingeniería"]
    )
    
    st.markdown("---")
    st.subheader("💡 Consultas Sugeridas")
    
    sugerencias = [
        "¿Cómo formular mi pregunta de investigación?",
        "Necesito metodologías para mi proyecto",
        "¿Dónde buscar literatura académica?",
        "Ayúdame con el marco teórico",
        "¿Cómo estructurar mi trabajo?"
    ]
    
    for sugerencia in sugerencias:
        if st.button(sugerencia, key=sugerencia, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": sugerencia})
            # Simular respuesta
            with st.spinner("Pensando..."):
                time.sleep(1)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": generar_respuesta(sugerencia, area_investigacion)
                })
            st.rerun()
    
    st.markdown("---")
    if st.button("🧹 Limpiar Conversación", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola! Soy tu asistente de investigación. ¿En qué tema necesitas ayuda?"}
        ]
        st.rerun()

# Función para generar respuestas contextuales
def generar_respuesta(pregunta, area):
    pregunta = pregunta.lower()
    
    respuestas_base = {
        "metodologías": [
            f"Para {area}, te recomiendo:\n\n• **Investigación cuantitativa**: Encuestas, experimentos controlados\n• **Investigación cualitativa**: Entrevistas, estudios de caso, observación participante\n• **Metodología mixta**: Combina ambos enfoques\n\n¿Sobre qué aspecto específico necesitas ayuda?",
            f"En el área de {area}, las metodologías comunes incluyen:\n\n📊 **Análisis estadístico** para datos numéricos\n📝 **Análisis de contenido** para texto\n🔍 **Estudios longitudinales** para seguimiento en el tiempo\n\nCuéntame más sobre tu proyecto."
        ],
        "literatura": [
            f"Para buscar literatura en {area}:\n\n📚 **Bases de datos académicas**:\n- Google Scholar\n- PubMed (si es salud)\n- IEEE Xplore (tecnología)\n- JSTOR (humanidades)\n- ScienceDirect\n\n🔍 **Estrategias de búsqueda**:\n- Usa palabras clave específicas\n- Combina términos con operadores booleanos (AND, OR)\n- Revisa las referencias de artículos clave",
            f"Encontrar literatura para {area}:\n\n• Revisa las revistas indexadas más importantes de tu área\n• Busca por autores reconocidos\n• Consulta revisiones sistemáticas\n• No olvides las tesis doctorales\n\n¿Qué tema específico estás investigando?"
        ],
        "pregunta de investigación": [
            f"Para formular una buena pregunta en {area}:\n\n🎯 **Características de una buena pregunta**:\n- Clara y específica\n- Medible y alcanzable\n- Relevante para el campo\n- Original o con nuevo enfoque\n\n📝 **Ejemplo de estructura**:\n'¿Cuál es el impacto de [variable] en [resultado] bajo [condiciones]?'\n\n¿Ya tienes algún tema en mente?",
            f"Formular preguntas en {area}:\n\n• Parte de un problema observable\n• Revisa qué se ha investigado antes\n• Identifica gaps en el conocimiento\n• Asegúrate que sea investigable\n\n¿Quieres que te ayude a refinar tu pregunta?"
        ],
        "marco teórico": [
            f"Para el marco teórico en {area}:\n\n📖 **Pasos a seguir**:\n1. Identifica las teorías principales\n2. Revisa conceptos clave\n3. Analiza estudios previos\n4. Establece relaciones entre conceptos\n5. Justifica tu enfoque teórico\n\n💡 En {area}, considera teorías recientes y clásicas.",
            f"Construir marco teórico para {area}:\n\n• Comienza con una revisión exhaustiva\n• Organiza por temas o cronológicamente\n• Critica y compara diferentes enfoques\n• Relaciona con tu pregunta de investigación\n\n¿Tienes alguna teoría específica en mente?"
        ],
        "estructura": [
            f"Estructura típica para trabajos en {area}:\n\n1. **Introducción** (planteamiento del problema)\n2. **Marco teórico** \n3. **Metodología**\n4. **Resultados**\n5. **Discusión**\n6. **Conclusiones**\n7. **Referencias**\n\n🔧 Ajusta según los requisitos de tu institución.",
            f"Para organizar tu trabajo en {area}:\n\n📋 **Estructura recomendada**:\n- Portada y resumen\n- Índice\n- Introducción contextualizada\n- Desarrollo por capítulos\n- Conclusiones y recomendaciones\n- Bibliografía\n- Anexos\n\n¿Es para tesis, artículo o proyecto de curso?"
        ]
    }
    
    # Detectar tipo de pregunta
    if any(palabra in pregunta for palabra in ["metodolog", "método", "cómo investigar"]):
        return random.choice(respuestas_base["metodologías"])
    elif any(palabra in pregunta for palabra in ["literatura", "buscar", "fuentes", "artículos"]):
        return random.choice(respuestas_base["literatura"])
    elif any(palabra in pregunta for palabra in ["pregunta", "formular", "tema", "problema"]):
        return random.choice(respuestas_base["pregunta de investigación"])
    elif any(palabra in pregunta for palabra in ["marco teórico", "teoría", "conceptual"]):
        return random.choice(respuestas_base["marco teórico"])
    elif any(palabra in pregunta for palabra in ["estructura", "organizar", "esquema"]):
        return random.choice(respuestas_base["estructura"])
    else:
        respuestas_genericas = [
            f"Interesante pregunta sobre {area}. Para darte una mejor respuesta, ¿podrías contarme más detalles sobre tu proyecto de investigación?",
            f"En el área de {area}, ese tema es muy relevante. Te sugiero:\n\n• Revisar literatura reciente\n• Identificar autores clave\n• Considerar el contexto específico\n\n¿Qué aspecto te gustaría profundizar?",
            f"Buena consulta sobre {area}. Para ayudarte mejor:\n\n🔍 ¿Ya has revisado algún material?\n🎯 ¿Tienes algún objetivo específico?\n⏱️ ¿Cuál es tu plazo de entrega?\n\nCon más contexto puedo darte consejos más precisos."
        ]
        return random.choice(respuestas_genericas)

# Área principal del chat
col_chat, col_ayuda = st.columns([3, 1])

with col_chat:
    # Mostrar historial del chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu pregunta de investigación aquí..."):
        # Añadir mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar y mostrar respuesta
        with st.chat_message("assistant"):
            with st.spinner("🔍 Consultando bases de conocimiento..."):
                time.sleep(1.5)
                respuesta = generar_respuesta(prompt, area_investigacion)
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})

with col_ayuda:
    st.subheader("🎯 Tipos de Ayuda")
    
    st.info("""
    **Puedo ayudarte con:**
    
    • 📋 Diseño de investigación
    • 🔍 Búsqueda de literatura  
    • 📊 Metodologías
    • 📝 Estructura del trabajo
    • 🎯 Preguntas de investigación
    • 📖 Marco teórico
    • ⏱️ Planificación
    """)
    
    st.markdown("---")
    st.subheader("💬 Ejemplos de Consultas")
    st.write("""
    "¿Cómo inicio mi investigación?"
    "Necesito metodologías para..."
    "¿Dónde buscar información?"
    "Ayuda con el marco teórico"
    "¿Cómo estructurar mi tesis?"
    """)

# Pie de página
st.markdown("---")
st.caption("🤖 Chatbot de Investigación AI v2.0 | Conversacional | Basado en mejores prácticas académicas")
