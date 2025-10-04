# HERRAMIENTAS QUE FALTAN - IMPLEMENTACIÓN COMPLETA

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import google.generativeai as genai
from google.generativeai import types
import io
import csv
from docx import Document
from semantic_scholar import SemanticScholar  # Asegurar que esta librería esté disponible

# Función de búsqueda en Semantic Scholar - COMPLETAR
def buscar_semantic_scholar(query, max_results=5):
    """Búsqueda gratuita en Semantic Scholar"""
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
    return articulos

# Función de búsqueda en SciELO - COMPLETAR
def buscar_scielo(query, max_results=5):
    """Búsqueda gratuita en SciELO"""
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
    return articulos

# Función para generar planteamiento del problema - CORREGIR NOMBRE
def generar_planteamiento_problema(texto_resumen, contexto_usuario):
    try:
        client = genai.Client()
        prompt = (
            f"Con base en la siguiente síntesis de literatura científica:\n{texto_resumen}\n\n"
            f"Considerando que el investigador se interesa en: {contexto_usuario}\n"
            "Genera un planteamiento del problema estructurado para un proyecto de investigación que incluya:\n"
            ". Descripción clara del problema\n"
            ". Justificación de la investigación\n"
            ". Delimitación del campo o población\n"
            ". Preguntas de investigación bien formuladas\n"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text
    except Exception as e:
        return f"Error al generar planteamiento: {e}"

# Función para generar objetivos de investigación - CORREGIR NOMBRE
def generar_objetivos_investigacion(texto_resumen, contexto_usuario):
    try:
        client = genai.Client()
        prompt = (
            f"Con base en la siguiente síntesis de literatura científica y el contexto del investigador:\n{texto_resumen}\n\n"
            f"Considerando que el investigador desea enfocarse en: {contexto_usuario}\n"
            "Genera los objetivos de investigación para un proyecto académico que incluyan:\n"
            "- Un objetivo general\n"
            "- Tres a cinco objetivos específicos coherentes con el problema y la justificación\n"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text
    except Exception as e:
        return f"Error al generar objetivos: {e}"

# Función para generar bibliografía - COMPLETAR Y CORREGIR
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
        elif estilo.upper() == "UPEL":
            partes = []
            partes.append(f"{autor}. ({año}).")
            if titulo:
                partes.append(f"{titulo}.")
            if publicacion:
                partes.append(f"{publicacion}.")
            cita = " ".join(partes)
            if url:
                cita += f" Disponible en: {url}"
        else:
            cita = f"{autor}, {año}, {titulo}"
        return " ".join(cita.split())

    bibliografia = [formatear_cita(ref) for ref in referencias]
    return "\n\n".join(bibliografia)

