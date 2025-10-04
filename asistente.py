import os
import streamlit as st
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.utilities import SerpAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import numpy as np
import re
from datetime import date
from docx import Document
from docx.shared import Pt, Inches
from io import BytesIO
import requests

# Configuración de la página
st.set_page_config(
    page_title="Agente de IA para Investigación Académica",
    page_icon="📚",
    layout="wide"
)

# Inicializar el modelo OpenAI
try:
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        openai_api_key=st.secrets.get("OPENAI_API_KEY", "")
    )
    st.write("✅ Conexión con OpenAI exitosa")
except Exception as e:
    st.error(f"❌ Error al conectar con OpenAI: {str(e)}")
    st.stop()

# Configurar la herramienta de búsqueda general
try:
    search = SerpAPIWrapper()
    search_tool = Tool(
        name="Academic_Search",
        func=lambda x: "\n".join([f"{i+1}. {item.strip('[]')}" for i, item in enumerate(search.run(x+" after:2023").split(","))]) if "año" in x.lower() else "\n".join([f"{i+1}. {item.strip('[]')}" for i, item in enumerate(search.run(x).split(","))]),
        description="Busca en Google Scholar artículos académicos. Añade 'año' para filtrar desde 2023."
    )
    st.write("✅ Herramienta de búsqueda general configurada")
except Exception as e:
    st.error(f"❌ Error al configurar búsqueda general: {str(e)}")
    st.stop()

# Configurar la herramienta de búsqueda UPEL
try:
    upel_search = SerpAPIWrapper()
    upel_search_tool = Tool(
        name="UPEL_Search",
        func=lambda x: "\n".join([f"{i+1}. {item.strip('[]')}" for i, item in enumerate(upel_search.run(x+" site:*.upel.edu.ve").split(","))]),
        description="Busca artículos académicos relacionados con la UPEL (Universidad Pedagógica Experimental Libertador)."
    )
    st.write("✅ Herramienta de búsqueda UPEL configurada")
except Exception as e:
    st.error(f"❌ Error al configurar búsqueda UPEL: {str(e)}")
    st.stop()

# Configurar la herramienta matemática
def math_calculator(expression: str) -> str:
    """Calcula expresiones matemáticas, incluyendo media y desviación estándar"""
    try:
        if 'media' in expression.lower() or 'média' in expression.lower() or 'moyenne' in expression.lower():
            nums = eval(expression.split('de')[-1].strip() if 'de' in expression else expression.split('of')[-1].strip() if 'of' in expression else expression.split('moyenne')[-1].strip())
            return str(np.mean(nums))
        elif 'desviación estándar' in expression.lower() or 'desvio padrão' in expression.lower() or 'écart-type' in expression.lower():
            nums = eval(expression.split('de')[-1].strip() if 'de' in expression else expression.split('of')[-1].strip() if 'of' in expression else expression.split('écart-type')[-1].strip())
            return str(np.std(nums))
        else:
            return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

# Configurar la herramienta de resumen simple
def summarize_article(text: str, language: str = "Español") -> str:
    """Genera un resumen breve del texto proporcionado en el idioma especificado."""
    try:
        prompt_templates = {
            "Español": f"Resume el siguiente texto en no más de 50 palabras: {text}",
            "Inglés": f"Summarize the following text in no more than 50 words: {text}",
            "Portugués": f"Resuma o seguinte texto em no máximo 50 palavras: {text}",
            "Francés": f"Résumez le texte suivant en 50 mots maximum : {text}"
        }
        summary = llm.invoke(prompt_templates[language])
        return summary.content.strip()
    except Exception as e:
        return f"Error al resumir: {str(e)}"

# Configurar la herramienta de resumen estructurado
def generate_structured_summary(query: str) -> str:
    """Genera un resumen estructurado (Introducción, Objetivos, Metodología, Resultados, Conclusiones) en el idioma especificado."""
    try:
        language = st.session_state.get("language", "Español")
        text_match = re.search(r"para el primero", query.lower())
        search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
        
        search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
        article = search_results.split("', ")[0].strip('[]') if text_match else query

        prompt_templates = {
            "Español": f"Genera un resumen estructurado del siguiente artículo en español, con las secciones Introducción, Objetivos, Metodología, Resultados y Conclusiones, con un máximo de 150 palabras en total: {article}",
            "Inglés": f"Generate a structured summary of the following article in English, with sections Introduction, Objectives, Methodology, Results, and Conclusions, with a maximum of 150 words in total: {article}",
            "Portugués": f"Gere um resumo estruturado do seguinte artigo em português, com as seções Introdução, Objetivos, Metodologia, Resultados e Conclusões, com um máximo de 150 palavras no total: {article}",
            "Francés": f"Générez un résumé structuré de l'article suivant en français, avec les sections Introduction, Objectifs, Méthodologie, Résultats et Conclusions, avec un maximum de 150 mots au total : {article}"
        }
        
        summary = llm.invoke(prompt_templates[language])
        return summary.content.strip()
    except Exception as e:
        return f"Error al generar resumen estructurado: {str(e)}"

# Configurar la herramienta de citas APA
def generate_apa_citation(text: str, language: str = "Español") -> str:
    """Genera una cita en formato APA en el idioma especificado."""
    try:
        title_match = re.search(r"^(.*?)\\.", text)
        title = title_match.group(1) if title_match else "Título no disponible"
        
        authors_match = re.search(r"\\s*([A-Za-z\\s\\.]+)\\.", text)
        authors = authors_match.group(1) if authors_match else "Autor no disponible"
        
        year_match = re.search(r"\((\d{4})\)", text)
        year = year_match.group(1) if year_match else "s.f."
        
        citation_templates = {
            "Español": f"{authors}. ({year}). {title}. Recuperado de Google Scholar.",
            "Inglés": f"{authors}. ({year}). {title}. Retrieved from Google Scholar.",
            "Portugués": f"{authors}. ({year}). {title}. Recuperado do Google Scholar.",
            "Francés": f"{authors}. ({year}). {title}. Récupéré de Google Scholar."
        }
        
        return citation_templates[language]
    except Exception as e:
        return f"Error al generar cita APA: {str(e)}"

# Configurar la herramienta de citas UPEL
def generate_upel_citation(text: str, work_type: str = "Tesis", language: str = "Español") -> str:
    """Genera una cita según el Manual de Trabajo de Grado, Especialización, Maestría y Tesis Doctorales de la UPEL."""
    try:
        today = date.today().strftime("%d/%m/%Y")
        title_match = re.search(r"^(.*?)\\.", text)
        title = title_match.group(1) if title_match else "Título no disponible"
        
        authors_match = re.search(r"\\s*([A-Za-z,\\s\\.]+)\\.", text)
        authors = authors_match.group(1) if authors_match else "Autor no disponible"
        
        year_match = re.search(r"\((\d{4})\)", text)
        year = year_match.group(1) if year_match else "s.f."
        
        citation_templates = {
            "Español": f"{authors}. ({year}). {title}. {work_type}. Universidad Pedagógica Experimental Libertador. Recuperado el {today} de Google Scholar.",
            "Inglés": f"{authors}. ({year}). {title}. {work_type}. Universidad Pedagógica Experimental Libertador. Retrieved on {today} from Google Scholar.",
            "Portugués": f"{authors}. ({year}). {title}. {work_type}. Universidad Pedagógica Experimental Libertador. Recuperado em {today} do Google Scholar.",
            "Francés": f"{authors}. ({year}). {title}. {work_type}. Universidad Pedagógica Experimental Libertador. Récupéré le {today} de Google Scholar."
        }
        
        return citation_templates[language]
    except Exception as e:
        return f"Error al generar cita UPEL: {str(e)}"

# Herramienta de citas UPEL con lógica para tipo de trabajo
def generate_upel_citation_tool(query: str) -> str:
    """Herramienta que genera una cita UPEL, seleccionando el tipo de trabajo e idioma."""
    try:
        work_type = st.session_state.get("upel_work_type", "Tesis")
        language = st.session_state.get("language", "Español")
        
        if "trabajo de grado" in query.lower():
            work_type = "Trabajo de Grado"
        elif "tesis de maestría" in query.lower():
            work_type = "Tesis de Maestría"
        elif "tesis doctoral" in query.lower():
            work_type = "Tesis Doctoral"
            
        text_match = re.search(r"para el primero", query.lower())
        search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
        
        search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
        first_result = search_results.split("', ")[0].strip('[]') if text_match else query
        
        return generate_upel_citation(first_result, work_type, language)
    except Exception as e:
        return f"Error al generar cita UPEL: {str(e)}"

# Herramienta para generar bibliografía
def generate_bibliography(query: str) -> str:
    """Genera una lista de referencias ordenada alfabéticamente en el formato especificado."""
    try:
        language = st.session_state.get("language", "Español")
        citation_format = st.session_state.get("citation_format", "APA")
        work_type = st.session_state.get("upel_work_type", "Tesis") if citation_format == "UPEL" else None
        
        search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
        search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
        
        articles = [item.strip('[]') for item in search_results.split("', ")[:5]]
        citations = []
        
        for article in articles:
            if citation_format == "APA":
                citation = generate_apa_citation(article, language)
            else:
                citation = generate_upel_citation(article, work_type, language)
            
            if "Error" not in citation:
                citations.append(citation)
        
        citations.sort()
        
        bibliography_title = {
            "Español": "Referencias",
            "Inglés": "References",
            "Portugués": "Referências",
            "Francés": "Références"
        }[language]
        
        return f"{bibliography_title}:\n" + "\n".join(citations) if citations else "No se encontraron artículos válidos."
    except Exception as e:
        return f"Error al generar bibliografía: {str(e)}"

# Herramienta para generar tabla comparativa
def generate_comparison_table(query: str) -> str:
    """Genera una tabla comparativa de hasta 3 artículos con Autor, Título, Año, Metodología, Hallazgos."""
    language = st.session_state.get("language", "Español")
    
    search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
    search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
    
    articles = [item.strip('[]') for item in search_results.split("', ")[:3]]
    table_rows = []
    
    for article in articles:
        title_match = re.search(r"^(.*?)\\.", article)
        title = title_match.group(1) if title_match else "Título no disponible"
        
        authors_match = re.search(r"\\.\\s*([A-Za-z,\\s\\.]+)\\.", article)
        authors = authors_match.group(1) if authors_match else "Autor no disponible"
        
        year_match = re.search(r"\((\d{4})\)", article)
        year = year_match.group(1) if year_match else "s.f."
        
        prompt_templates = {
            "Español": f"Describe brevemente la metodología (máximo 20 palabras) y hallazgos principales (máximo 30 palabras) del artículo: {article}",
            "Inglés": f"Briefly describe the methodology (max 20 words) and main findings (max 30 words) of the article: {article}",
            "Portugués": f"Descreva brevemente a metodologia (máximo 20 palavras) e os principais achados (máximo 30 palavras) do artigo: {article}",
            "Francés": f"Décrivez brièvement la méthodologie (max 20 mots) et les principaux résultats (max 30 mots) de l'article : {article}"
        }
        
        analysis = llm.invoke(prompt_templates[language]).content.strip().split("\n")
        methodology = analysis[0] if len(analysis) > 0 else "Metodología no disponible"
        findings = analysis[1] if len(analysis) > 1 else "Hallazgos no disponibles"
        
        table_rows.append([authors, title, year, methodology, findings])
    
    headers = {
        "Español": ["Autor", "Título", "Año", "Metodología", "Hallazgos Principales"], 
        "Inglés": ["Author", "Title", "Year", "Methodology", "Main Findings"], 
        "Portugués": ["Autor", "Título", "Ano", "Metodologia", "Principais Achados"], 
        "Francés": ["Auteur", "Titre", "Année", "Méthodologie", "Résultats Principaux"] 
    }[language]
    
    table = f"{headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} | {headers[4]}\n"
    table += "--- | --- | --- | --- | ---\n"
    
    for row in table_rows:
        table += f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n"
    
    table_title = {
        "Español": "Tabla Comparativa",
        "Inglés": "Comparison Table",
        "Portugués": "Tabela Comparativa",
        "Francés": "Tableau Comparatif"
    }[language]
    
    return f"{table_title}:\n{table}"

# Herramienta para generar esquema de investigación
def generate_research_outline(query: str) -> str:
    """Genera un esquema de investigación con Introducción, Marco Teórico, Metodología, Resultados Esperados, Conclusiones."""
    language = st.session_state.get("language", "Español")
    
    prompt_templates = {
        "Español": f"Genera un esquema de investigación en español para un estudio sobre {query}, con las secciones Introducción, Marco Teórico, Metodología, Resultados Esperados y Conclusiones, con un máximo de 200 palabras en total.",
        "Inglés": f"Generate a research outline in English for a study on {query}, with sections Introduction, Theoretical Framework, Methodology, Expected Results, and Conclusions, with a maximum of 200 words in total.",
        "Portugués": f"Gere um esboço de pesquisa em português para um estudo sobre {query}, com as seções Introdução, Quadro Teórico, Metodologia, Resultados Esperados e Conclusões, com um máximo de 200 palavras no total.",
        "Francés": f"Générez un plan de recherche en français pour une étude sur {query}, avec les sections Introduction, Cadre Théorique, Méthodologie, Résultats Attendus et Conclusions, avec un maximum de 200 mots au total."
    }
    
    outline = llm.invoke(prompt_templates[language]).content.strip()
    
    outline_title = {
        "Español": "Esquema de Investigación",
        "Inglés": "Research Outline",
        "Portugués": "Esboço de Pesquisa",
        "Francés": "Plan de Recherche"
    }[language]
    
    return f"{outline_title}:\n{outline}"

# Herramienta para generar propuestas de títulos
def generate_research_titles(query: str) -> str:
    """Genera hasta 5 propuestas de títulos académicos para un tema de investigación."""
    language = st.session_state.get("language", "Español")
    
    search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
    search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
    
    context = "\n".join([item.strip('[]') for item in search_results.split("', ")[:3]])
    
    prompt_templates = {
        "Español": f"Basándote en el siguiente contexto, genera 5 propuestas de títulos académicos en español para un estudio sobre {query}, cada uno con un máximo de 20 palabras:\nContexto: {context}",
        "Inglés": f"Based on the following context, generate 5 academic title proposals in English for a study on {query}, each up to 20 words:\nContext: {context}",
        "Portugués": f"Com base no seguinte contexto, gere 5 propostas de títulos académicos em português para um estudo sobre {query}, cada um com até 20 palavras:\nContexto: {context}",
        "Francés": f"En vous basant sur le contexte suivant, générez 5 propositions de titres académiques en français pour une étude sur {query}, chacun jusqu'à 20 mots :\nContexte : {context}"
    }
    
    titles = llm.invoke(prompt_templates[language]).content.strip()
    titles_list = [line.strip() for line in titles.split("\n") if line.strip()][:5]
    titles_formatted = "\n".join([f"{i+1}. {title}" for i, title in enumerate(titles_list)])
    
    titles_title = {
        "Español": "Propuestas de Títulos de Investigación",
        "Inglés": "Research Title Proposals",
        "Portugués": "Propostas de Títulos de Pesquisa",
        "Francés": "Propositions de Titres de Recherche"
    }[language]
    
    return f"{titles_title}:\n{titles_formatted}"

# Herramienta para generar mapa conceptual
def generate_concept_map(query: str) -> str:
    """Genera un mapa conceptual en formato texto con nodos principales y secundarios."""
    language = st.session_state.get("language", "Español")
    
    search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
    search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
    
    context = "\n".join([item.strip('[]') for item in search_results.split("', ")[:3]])
    
    prompt_templates = {
        "Español": f"Basándote en el siguiente contexto, genera un mapa conceptual en español para un estudio sobre {query}, en formato de lista jerárquica con 3 nodos principales y hasta 3 nodos secundarios por cada uno, con un máximo de 150 palabras en total:\nContexto: {context}",
        "Inglés": f"Based on the following context, generate a concept map in English for a study on {query}, in a hierarchical list format with 3 main nodes and up to 3 secondary nodes each, with a maximum of 150 words in total:\nContext: {context}",
        "Portugués": f"Com base no seguinte contexto, gere um mapa conceitual em português para um estudo sobre {query}, em formato de lista hierárquica com 3 nós principais e até 3 nós secundários por cada um, com um máximo de 150 palavras no total:\nContexto: {context}",
        "Francés": f"En vous basant sur le contexte suivant, générez une carte conceptuelle en français pour une étude sur {query}, sous forme de liste hiérarchique avec 3 nœuds principaux et jusqu'à 3 nœuds secondaires chacun, avec un maximum de 150 mots au total : \nContexte : {context}"
    }
    
    concept_map = llm.invoke(prompt_templates[language]).content.strip()
    
    concept_map_title = {
        "Español": "Mapa Conceptual",
        "Inglés": "Concept Map",
        "Portugués": "Mapa Conceitual",
        "Francés": "Carte Conceptuelle"
    }[language]
    
    return f"{concept_map_title}:\n{concept_map}"

# Herramienta para generar preguntas de investigación
def generate_research_questions(query: str) -> str:
    """Genera hasta 5 preguntas de investigación para un tema de investigación."""
    language = st.session_state.get("language", "Español")
    
    search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
    search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
    
    context = "\n".join([item.strip('[]') for item in search_results.split("', ")[:3]])
    
    prompt_templates = {
        "Español": f"Basándote en el siguiente contexto, genera 5 preguntas de investigación en español para un estudio sobre {query}, cada una con un máximo de 20 palabras:\nContexto: {context}",
        "Inglés": f"Based on the following context, generate 5 research questions in English for a study on {query}, each up to 20 words:\nContext: {context}",
        "Portugués": f"Com base no seguinte contexto, gere 5 perguntas de pesquisa em português para um estudo sobre {query}, cada uma com até 20 palavras:\nContexto: {context}",
        "Francés": f"En vous basant sur le contexte suivant, générez 5 questions de recherche en français pour une étude sur {query}, chacune jusqu'à 20 mots :\nContexte : {context}"
    }
    
    questions = llm.invoke(prompt_templates[language]).content.strip()
    questions_list = [line.strip() for line in questions.split("\n") if line.strip()][:5]
    questions_formatted = "\n".join([f"{i+1}. {question}" for i, question in enumerate(questions_list)])
    
    questions_title = {
        "Español": "Preguntas de Investigación",
        "Inglés": "Research Questions",
        "Portugués": "Perguntas de Pesquisa",
        "Francés": "Questions de Recherche"
    }[language]
    
    return f"{questions_title}:\n{questions_formatted}"

# Herramienta para generar objetivos de investigación
def generate_research_objectives(query: str) -> str:
    """Genera un objetivo general y hasta 3 objetivos específicos para un tema de investigación."""
    language = st.session_state.get("language", "Español")
    
    search_query = query + (" site:*.upel.edu.ve" if "repositorio upel" in query.lower() else " after:2023" if "año" in query.lower() else "")
    search_results = upel_search.run(search_query) if "repositorio upel" in query.lower() else search.run(search_query)
    
    context = "\n".join([item.strip('[]') for item in search_results.split("', ")[:3]])
    
    prompt_templates = {
        "Español": f"Basándote en el siguiente contexto, genera un objetivo general y 3 objetivos específicos en español para un estudio sobre {query}, cada uno con un máximo de 20 palabras:\nContexto: {context}",
        "Inglés": f"Based on the following context, generate one general objective and 3 specific objectives in English for a study on {query}, each up to 20 words:\nContext: {context}",
        "Portugués": f"Com base no seguinte contexto, gere um objetivo geral e 3 objetivos específicos em português para um estudio sobre {query}, cada um com até 20 palavras:\nContexto: {context}",
        "Francés": f"En vous basant sur le contexte suivant, générez un objectif général et 3 objectifs spécifiques en français pour une étude sur {query}, chacun jusqu'à 20 mots :\nContexte : {context}"
    }
    
    objectives = llm.invoke(prompt_templates[language]).content.strip()
    objectives_list = [line.strip() for line in objectives.split("\n") if line.strip()][:4]
    
    objectives_formatted = ""
    if objectives_list:
        if language == "Español":
            objectives_formatted += f"Objetivo General:\n{objectives_list[0]}\n\nObjetivos Específicos:\n"
        elif language == "Inglés":
            objectives_formatted += f"General Objective:\n{objectives_list[0]}\n\nSpecific Objectives:\n"
        elif language == "Portugués":
            objectives_formatted += f"Objetivo Geral:\n{objectives_list[0]}\n\nObjetivos Específicos:\n"
        else:  # Francés
            objectives_formatted += f"Objectif Général:\n{objectives_list[0]}\n\nObjectifs Spécifiques:\n"
        
        objectives_formatted += "\n".join([f"{i}. {obj}" for i, obj in enumerate(objectives_list[1:], 1)])
    
    objectives_title = {
        "Español": "Objetivos de Investigación",
        "Inglés": "Research Objectives",
        "Portugués": "Objetivos de Pesquisa",
        "Francés": "Objectifs de Recherche"
    }[language]
    
    return f"{objectives_title}:\n{objectives_formatted}"

# Generar documento Word
def generate_word_document(content: str, language: str = "Español", is_summary: bool = False, 
                         is_table: bool = False, is_outline: bool = False, is_titles: bool = False, 
                         is_concept_map: bool = False, is_questions: bool = False, 
                         is_objectives: bool = False) -> BytesIO:
    """Genera un documento Word con el contenido en formato académico."""
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
    
    title_texts = {
        "Español": ("Objetivos de Investigación" if is_objectives else
                   "Preguntas de Investigación" if is_questions else
                   "Mapa Conceptual" if is_concept_map else
                   "Propuestas de Títulos de Investigación" if is_titles else
                   "Esquema de Investigación" if is_outline else
                   "Tabla Comparativa" if is_table else
                   "Resumen Estructurado" if is_summary else
                   ("Referencias" if "\n" in content and not content.startswith("Autor |") else "Cita Generada")),
        "Inglés": ("Research Objectives" if is_objectives else
                  "Research Questions" if is_questions else
                  "Concept Map" if is_concept_map else
                  "Research Title Proposals" if is_titles else
                  "Research Outline" if is_outline else
                  "Comparison Table" if is_table else
                  "Structured Summary" if is_summary else
                  ("References" if "\n" in content and not content.startswith("Author |") else "Generated Citation")),
        "Portugués": ("Objetivos de Pesquisa" if is_objectives else
                     "Perguntas de Pesquisa" if is_questions else
                     "Mapa Conceitual" if is_concept_map else
                     "Propostas de Títulos de Pesquisa" if is_titles else
                     "Esboço de Pesquisa" if is_outline else
                     "Tabela Comparativa" if is_table else
                     "Resumo Estruturado" if is_summary else
                     ("Referências" if "\n" in content and not content.startswith("Autor |") else "Citação Gerada")),
        "Francés": ("Objectifs de Recherche" if is_objectives else
                   "Questions de Recherche" if is_questions else
                   "Carte Conceptuelle" if is_concept_map else
                   "Propositions de Titres de Recherche" if is_titles else
                   "Plan de Recherche" if is_outline else
                   "Tableau Comparatif" if is_table else
                   "Résumé Structuré" if is_summary else
                   ("Références" if "\n" in content and not content.startswith("Auteur |") else "Citation Générée"))
    }
    
    title = doc.add_heading(title_texts[language], level=1)
    title.style.font.name = "Times New Roman"
    title.style.font.size = Pt(12)

    if is_table:
        lines = content.split("\n")[1:]
        headers = [h.strip() for h in lines[0].split("|")]
        rows = [[cell.strip() for cell in line.split("|")] for line in lines[2:] if line.strip()]
        
        table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.style = "Table Grid"
        
        for i, header in enumerate(headers):
            cell = table.cell(0, i)
            cell.text = header
            cell.paragraphs[0].style.font.name = "Times New Roman"
            cell.paragraphs[0].style.font.size = Pt(12)
            cell.paragraphs[0].style.font.bold = True
        
        for i, row in enumerate(rows):
            for j, cell_content in enumerate(row):
                cell = table.cell(i + 1, j)
                cell.text = cell_content
                cell.paragraphs[0].style.font.name = "Times New Roman"
                cell.paragraphs[0].style.font.size = Pt(12)
    else:
        for line in content.split("\n"):
            p = doc.add_paragraph(line)
            p.style.font.name = "Times New Roman"
            p.style.font.size = Pt(12)
            p.paragraph_format.line_spacing = 1.5
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Definir todas las herramientas
tools = [
    search_tool,
    upel_search_tool,
    Tool(
        name="Math_Calculator",
        func=math_calculator,
        description="Calcula expresiones matemáticas, incluyendo media y desviación estándar."
    ),
    Tool(
        name="Summarize_Article",
        func=lambda x: summarize_article(x, st.session_state.get("language", "Español")),
        description="Genera un resumen breve de un texto o artículo en el idioma seleccionado."
    ),
    Tool(
        name="Generate_Structured_Summary",
        func=generate_structured_summary,
        description="Genera un resumen estructurado (Introducción, Objetivos, Metodología, Resultados, Conclusiones) de un artículo en el idioma seleccionado."
    ),
    Tool(
        name="Generate_APA_Citation",
        func=lambda x: generate_apa_citation(x, st.session_state.get("language", "Español")),
        description="Genera una cita en formato APA en el idioma seleccionado."
    ),
    Tool(
        name="Generate_UPEL_Citation",
        func=generate_upel_citation_tool,
        description="Genera una cita según el Manual de Trabajo de Grado, Especialización, Maestría y Tesis Doctorales de la UPEL, usando el tipo de trabajo e idioma seleccionados."
    ),
    Tool(
        name="Generate_Bibliography",
        func=generate_bibliography,
        description="Genera una lista de referencias ordenada alfabéticamente en formato APA o UPEL."
    ),
    Tool(
        name="Generate_Comparison_Table",
        func=generate_comparison_table,
        description="Genera una tabla comparativa de hasta 3 artículos con Autor, Título, Año, Metodología y Hallazgos Principales."
    ),
    Tool(
        name="Generate_Research_Outline",
        func=generate_research_outline,
        description="Genera un esquema de investigación con Introducción, Marco Teórico, Metodología, Resultados Esperados y Conclusiones."
    ),
    Tool(
        name="Generate_Research_Titles",
        func=generate_research_titles,
        description="Genera hasta 5 propuestas de títulos académicos para un tema de investigación."
    ),
    Tool(
        name="Generate_Concept_Map",
        func=generate_concept_map,
        description="Genera un mapa conceptual en formato texto con nodos principales y secundarios para un tema de investigación."
    ),
    Tool(
        name="Generate_Research_Questions",
        func=generate_research_questions,
        description="Genera hasta 5 preguntas de investigación para un tema de investigación."
    ),
    Tool(
        name="Generate_Research_Objectives",
        func=generate_research_objectives,
        description="Genera un objetivo general y hasta 3 objetivos específicos para un tema de investigación."
    )
]

# Inicializar el agente con memoria
try:
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True
    )
    st.write("✅ Agente inicializado correctamente")
except Exception as e:
    st.error(f"❌ Error al inicializar el agente: {str(e)}")
    st.stop()

# Interfaz de chat mejorada
st.title("🤖 Agente de IA para Investigación Académica")
st.markdown("---")

# Configuración en sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    search_type = st.selectbox("Tipo de búsqueda:", ["Google Scholar", "Repositorio UPEL"])
    language = st.selectbox("Idioma:", ["Español", "Inglés", "Portugués", "Francés"])
    citation_format = st.selectbox("Formato de cita:", ["APA", "UPEL"])
    
    if citation_format == "UPEL":
        upel_work_type = st.selectbox("Tipo de trabajo UPEL:", 
                                    ["Tesis", "Trabajo de Grado", "Tesis de Maestría", "Tesis Doctoral"])
        st.session_state.upel_work_type = upel_work_type
    
    st.session_state.language = language
    st.session_state.citation_format = citation_format
    
    st.markdown("---")
    st.header("🛠️ Herramientas Disponibles")
    st.markdown("""
    - 🔍 Búsqueda académica
    - 📊 Calculadora matemática
    - 📝 Resumen de artículos
    - 🏛️ Citas APA/UPEL
    - 📚 Bibliografías
    - 📋 Tablas comparativas
    - 📄 Esquemas de investigación
    - 🎯 Títulos de investigación
    - 🗺️ Mapas conceptuales
    - ❓ Preguntas de investigación
    - 🎯 Objetivos de investigación
    """)

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de chat
query = st.chat_input("Escribe tu consulta de investigación...")

if query:
    # Preprocesar consulta
    processed_query = query
    
    if search_type == "Repositorio UPEL" and "repositorio upel" not in processed_query.lower():
        processed_query = processed_query + " en el repositorio UPEL"
    
    # Añadir idioma si no está especificado
    language_tags = {
        "Inglés": " en inglés",
        "Portugués": " em português", 
        "Francés": " en français",
        "Español": ""
    }
    if not any(tag in processed_query for tag in ["en inglés", "em português", "en français"]):
        processed_query += language_tags[language]
    
    # Añadir formato de cita si es relevante
    if any(keyword in processed_query.lower() for keyword in ["cita", "citation", "cite"]) and not any(format_keyword in processed_query.lower() for format_keyword in ["apa", "upel"]):
        processed_query += f" en formato {citation_format}"

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(query)
    
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Procesar con el agente
    with st.chat_message("assistant"):
        with st.spinner("Analizando y generando respuesta..."):
            try:
                response = agent.invoke({"input": processed_query})["output"]
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Botones de descarga
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Descargar respuesta (Texto)",
                        data=response,
                        file_name="respuesta_investigacion.txt",
                        mime="text/plain"
                    )
                
                # Detectar tipo de contenido para exportación Word
                content_types = {
                    "Resumen Estructurado": ["Resumen Estructurado:", "Structured Summary:", "Resumo Estruturado:", "Résumé Structuré:"],
                    "Tabla Comparativa": ["Tabla Comparativa:", "Comparison Table:", "Tabela Comparativa:", "Tableau Comparatif:"],
                    "Esquema": ["Esquema de Investigación:", "Research Outline:", "Esboço de Pesquisa:", "Plan de Recherche:"],
                    "Títulos": ["Propuestas de Títulos:", "Research Title Proposals:", "Propostas de Títulos:", "Propositions de Titres:"],
                    "Mapa Conceptual": ["Mapa Conceptual:", "Concept Map:", "Mapa Conceitual:", "Carte Conceptuelle:"],
                    "Preguntas": ["Preguntas de Investigación:", "Research Questions:", "Perguntas de Pesquisa:", "Questions de Recherche:"],
                    "Objetivos": ["Objetivos de Investigación:", "Research Objectives:", "Objetivos de Pesquisa:", "Objectifs de Recherche:"],
                    "Referencias": ["Referencias:", "References:", "Referências:", "Références:"]
                }
                
                detected_type = None
                content_for_doc = response
                
                for content_type, keywords in content_types.items():
                    if any(keyword in response for keyword in keywords):
                        detected_type = content_type
                        # Extraer contenido después del título
                        for keyword in keywords:
                            if keyword in response:
                                content_for_doc = response.split(keyword)[-1].strip()
                                break
                        break
                
                if detected_type:
                    with col2:
                        doc_buffer = generate_word_document(
                            content_for_doc, 
                            language,
                            is_summary=detected_type == "Resumen Estructurado",
                            is_table=detected_type == "Tabla Comparativa", 
                            is_outline=detected_type == "Esquema",
                            is_titles=detected_type == "Títulos",
                            is_concept_map=detected_type == "Mapa Conceptual",
                            is_questions=detected_type == "Preguntas",
                            is_objectives=detected_type == "Objetivos"
                        )
                        
                        file_names = {
                            "Resumen Estructurado": "resumen_estructurado.docx",
                            "Tabla Comparativa": "tabla_comparativa.docx", 
                            "Esquema": "esquema_investigacion.docx",
                            "Títulos": "titulos_investigacion.docx",
                            "Mapa Conceptual": "mapa_conceptual.docx",
                            "Preguntas": "preguntas_investigacion.docx",
                            "Objetivos": "objetivos_investigacion.docx",
                            "Referencias": "referencias_bibliograficas.docx"
                        }
                        
                        st.download_button(
                            label=f"📄 Descargar {detected_type} (Word)",
                            data=doc_buffer,
                            file_name=file_names.get(detected_type, "documento.docx"),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        
            except Exception as e:
                error_msg = f"❌ Error al procesar la consulta: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Gestión del historial en el sidebar
with st.sidebar:
    st.markdown("---")
    st.header("💾 Gestión del Historial")
    
    if st.session_state.messages:
        history_text = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
        
        st.download_button(
            label="📋 Descargar historial completo",
            data=history_text,
            file_name="historial_conversacion.txt",
            mime="text/plain"
        )
        
        if st.button("🗑️ Limpiar historial", type="secondary"):
            st.session_state.messages = []
            memory.clear()
            st.rerun()

# Información de ayuda
with st.sidebar:
    st.markdown("---")
    st.header("ℹ️ Ejemplos de consultas")
    st.markdown("""
    - *"Busca artículos sobre inteligencia artificial en educación después de 2020"*
    - *"Genera un resumen estructurado del primer artículo sobre machine learning"*  
    - *"Crea una bibliografía en formato APA sobre cambio climático"*
    - *"Genera 5 preguntas de investigación sobre educación virtual"*
    - *"Dame un esquema de investigación sobre sostenibilidad ambiental"*
    """)
