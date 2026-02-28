import PyPDF2
import re

def leer_pdf(path):
    texto=""
    with open(path, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

def limpiar_texto(texto):
    # 1. Quitar saltos de línea excesivos
    texto = re.sub(r"\n+", " ", texto)

    # 2. Quitar espacios múltiples
    texto = re.sub(r"\s+", " ", texto)

    # 3. Quitar números de página típicos (opcional)
    texto = re.sub(r"\bPágina \d+\b", "", texto, flags=re.IGNORECASE)

    # 4. Quitar caracteres no imprimibles
    texto = re.sub(r"[^\x20-\x7EáéíóúÁÉÍÓÚñÑ]", "", texto)

    # 5. Strip final
    texto = texto.strip()

    return texto

def dividir_en_chunks(texto, palabras_por_chunk=750, overlap=75):
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
        # Definir el chunk
        chunk = palabras[i:i+palabras_por_chunk]
        chunks.append(" ".join(chunk))

        # Avanzar el índice, pero retroceder `overlap` palabras
        i += palabras_por_chunk - overlap

    #Añadir el resto de texto sin procesar si queda algo
    if i < len(palabras):
        chunks.append(" ".join(palabras[i:]))

    return chunks