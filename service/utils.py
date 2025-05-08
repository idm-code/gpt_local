import streamlit as st
import json
import os
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import pytesseract
from PIL import Image

# Ruta para guardar las conversaciones
CONVERSATIONS_FILE = "resources/conversations.json"
# Ruta para guardar el contexto del sistema en un archivo
CONTEXT_FILE = "resources/context.txt"

# Leer el contexto del sistema desde el archivo
def cargar_contexto():
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# Función para guardar todas las conversaciones en un archivo
def guardar_todas_conversaciones(conversaciones):
    with open(CONVERSATIONS_FILE, "w") as file:
        json.dump(conversaciones, file)

# Función para cargar todas las conversaciones desde un archivo
def cargar_todas_conversaciones():
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    return {} 
            except json.JSONDecodeError:
                return {}
    return {}

# Función para procesar documentos cargados
def procesar_documento(file):
    if file.name.endswith(".pdf"):
        pdf_reader = PdfReader(file)
        texto = ""
        for page in pdf_reader.pages:
            texto += page.extract_text()
        return texto
    elif file.name.endswith(".docx"):
        doc = Document(file)
        texto = ""
        for paragraph in doc.paragraphs:
            texto += paragraph.text + "\n"
        return texto
    elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
        df = pd.read_excel(file)
        return df.to_string()
    elif file.name.endswith(".csv"):
        try:
            df = pd.read_csv(file)
            return df.to_string()
        except Exception as e:
            st.error(f"Error al procesar el archivo CSV: {e}")
            return None
    elif file.name.endswith(".png") or file.name.endswith(".jpg") or file.name.endswith(".jpeg"):
        image = Image.open(file)
        texto = pytesseract.image_to_string(image)
        return texto
    elif file.name.endswith(".py") or file.name.endswith(".java") or file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        st.error("Formato de archivo no soportado. Por favor, sube un archivo PDF, Word, Excel, CSV o imagen.")
        return None