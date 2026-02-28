import src.conexions.config as config
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
import time
from google.genai import types

qdrant_client = config.qdrant_client
client = config.client

def embedding_texto(texto):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texto,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY",
            output_dimensionality=1536
            )
    )
    return response.embeddings[0].values

def crearCollection():
    # Fix: extraer nombres antes de comparar
    #qdrant_client.delete_collection(collection_name="documentos")
    existing = []
    last_error = None
    for _ in range(10):
        try:
            existing = [c.name for c in qdrant_client.get_collections().collections]
            last_error = None
            break
        except Exception as error:
            last_error = error
            time.sleep(1)

    if last_error is not None:
        raise last_error

    collection_name = "documentos"

    if collection_name not in existing:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )

def insertarPostgreSQL(documento):
    """
    Inserta un documento en PostgreSQL y devuelve su ID.
    """
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        query = "INSERT INTO documentos (nombre, path, extension, modified_time, creation_time, size, link) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"
        cursor.execute(query, (documento.name, documento.path, documento.extension, documento.modified_time, documento.creation_time, documento.size, documento.link))
        documento_id = cursor.fetchone()[0]
        postgres_connection.commit()
        return documento_id

def insertarDocumento(documento_id, chunks, filename):
    """
    Recibe el UUID del documento (ya insertado en PostgreSQL)
    y la lista de chunks de texto. Genera embeddings y los sube a Qdrant.
    """
    puntos = []
    for i, chunk in enumerate(chunks):  # Fix: i viene del enumerate
        vector = embedding_texto(chunk)
        puntos.append(
            PointStruct(
                id=str(uuid.uuid4()),  # Fix: UUID válido para Qdrant
                vector=vector,
                payload={
                    "documento_id": str(documento_id),  # FK a PostgreSQL
                    "chunk_index": i,
                    "nombre_documento": filename,
                    "texto": chunk
                }
            )
        )

    qdrant_client.upsert(collection_name="documentos", points=puntos)

# Returns a list of Document elements
def patternSearchByName(name_pattern):
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        query = "SELECT * FROM documentos WHERE name LIKE %s"
        cursor.execute(query, (name_pattern,))
        results = cursor.fetchall()
        # Aquí puedes convertir los resultados a objetos Document si es necesario
        return results

def patternSearchBySize(size_max, size_min):
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        query = "SELECT * FROM documentos WHERE size <= %s AND size >= %s"
        cursor.execute(query, (size_max, size_min))
        results = cursor.fetchall()
        # Aquí puedes convertir los resultados a objetos Document si es necesario
        return results

def patternSearchByExtension(extension):
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        query = "SELECT * FROM documentos WHERE extension = %s"
        cursor.execute(query, (extension,))
        results = cursor.fetchall()
        # Aquí puedes convertir los resultados a objetos Document si es necesario
        return results

def patternSearchByCreationDate(date_min, date_max):
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        # Fix: el orden estaba invertido, date_min va con >= y date_max con <=
        query = """
            SELECT id, nombre, path, extension, creation_time, modified_time, size, link
            FROM documentos
            WHERE creation_time >= %s AND creation_time <= %s
        """
        cursor.execute(query, (date_min, date_max))
        return cursor.fetchall()

def patternSearchByPath(path_pattern):
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        query = "SELECT * FROM documentos WHERE path = %s"
        cursor.execute(query, (path_pattern,))
        results = cursor.fetchall()
        # Aquí puedes convertir los resultados a objetos Document si es necesario
        return results

def vectorSearch(query_texto):
    vector = embedding_texto(query_texto)

    results = qdrant_client.query_points(
        collection_name="documentos",
        query=vector,
        limit=10,
        score_threshold=0.4,
        with_payload=True
    )

    vistos = {}
    fragmentos = {}  # guarda el chunk más relevante por documento (el primero = mayor score)
    for result in results.points:
        payload = result[1] if isinstance(result, tuple) else result.payload
        doc_id = payload.get("documento_id")
        nombre = payload.get("nombre_documento")
        texto = payload.get("texto", "")
        if doc_id and doc_id not in vistos:
            vistos[doc_id] = nombre
            fragmentos[doc_id] = texto  # el primero en aparecer es el de mayor score

    return [
        {
            "documento_id": doc_id,
            "nombre_documento": nombre,
            "fragmento": fragmentos[doc_id]  # chunk más relevante del documento
        }
        for doc_id, nombre in vistos.items()
    ]