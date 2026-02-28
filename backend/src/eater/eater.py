import re
from src.classes.document import Document
import src.db.interfazDB as interfazDB
import os
import PyPDF2
import docx
from fastapi import APIRouter
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

router = APIRouter()

def leer_pdf(path):
    texto = ""
    with open(path, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

def leer_txt(path):
    texto = ""
    with open(path, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    # Check if text has been read
    if texto and len(texto.strip()) >= 30:
        return texto
    
    texto_ocr = ""
    paginas = convert_from_path(path)
    
    for pagina in paginas:
        texto_ocr += pytesseract.image_to_string(pagina, lang="spa+eng") + "\n"
    
    return texto_ocr
    
def leer_imagen(path):
    try:
        imagen = Image.open(path)
        texto = pytesseract.image_to_string(imagen, lang="spa+eng")
        imagen.c
        return texto.strip()
    except Exception as e:
        return ""

def leer_docx(path):
    """Lee un archivo .docx con python-docx y devuelve el texto completo."""
    documento = docx.Document(path)
    parrafos = [p.text for p in documento.paragraphs if p.text.strip()]
    return "\n".join(parrafos)

def leer_documento(path):
    """
    Función unificada: detecta la extensión y usa el lector adecuado.
    Soporta .pdf, .docx y .doc
    """
    extension = os.path.splitext(path)[1].lower()
    if extension == ".pdf":
        return leer_pdf(path)
    elif extension == ".docx":
        return leer_docx(path)
    else:
        raise ValueError(f"Extensión no soportada: {extension}")

def limpiar_texto(texto):
    texto = re.sub(r"\n+", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r"\bPágina \d+\b", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"[^\x20-\x7EáéíóúÁÉÍÓÚñÑ]", "", texto)
    texto = texto.strip()
    return texto

def dividir_en_chunks(texto, palabras_por_chunk=250, overlap=25):
    """
    Divide el texto en chunks de palabras_por_chunk con un overlap entre chunks.

    Args:
        texto (str): texto completo
        palabras_por_chunk (int): tamaño de cada chunk en palabras
        overlap (int): número de palabras que se repiten entre chunks consecutivos

    Returns:
        List[str]: lista de chunks
    """
    palabras = texto.split()
    chunks = []
    i = 0

    while i < len(palabras):
        chunk = palabras[i:i + palabras_por_chunk]
        chunks.append(" ".join(chunk))
        i += palabras_por_chunk - overlap

    return chunks

def recibir_documento(documento):
    texto = ""
    if documento.extension == "pdf":
        texto = leer_pdf(documento.path)
    elif documento.extension == "png":
        texto = leer_imagen(documento.path)
    elif documento.extension == "txt":
        texto = leer_txt(documento.path)

    if(texto != ""):
        texto_limpio = limpiar_texto(texto)
        chunks = dividir_en_chunks(texto_limpio)
        for i in chunks:
            print(i + "\n")
            print("Tamaño: " + str(len(i.split(" "))))

        print("Divido")

        documento_id = interfazDB.insertarPostgreSQL(documento)
        print("Insertado en Postgre con ID: " + str(documento_id))
        interfazDB.insertarDocumento(documento_id, chunks, documento.path)
        print("Insertado en Qdrant")


#recibir_documento("tmp/hola.txt")
