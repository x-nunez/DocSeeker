import src.conexions.config as config
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

qdrant_client = config.qdrant_client
model = config.model

def embedding_texto(texto):
    return model.encode(texto).tolist()

def crearCollection():
    # Fix: extraer nombres antes de comparar
    #qdrant_client.delete_collection(collection_name="documentos")
    existing = [c.name for c in qdrant_client.get_collections().collections]
    collection_name = "documentos"

    if collection_name not in existing:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,  # dimensión de all-MiniLM
                distance=Distance.COSINE
            )
        )

def insertarPostgreSQL(documento):
    """
    Inserta un documento en PostgreSQL y devuelve su ID.
    """
    postgres_connection = config.get_postgres_connection()
    with postgres_connection.cursor() as cursor:
        query = "INSERT INTO documentos (nombre, path, extension) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query, (documento.name, documento.path, documento.extension))
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

def vectorSearch(query_texto):
    vector = embedding_texto(query_texto)

    results = qdrant_client.query_points(
        collection_name="documentos",
        query=vector,
        limit=10,
        with_payload=True
    )

    vistos = {}
    for result in results.points:
        # Fix: result es una tupla, el payload está en result[1]
        payload = result[1] if isinstance(result, tuple) else result.payload
        doc_id = payload.get("documento_id")
        nombre = payload.get("nombre_documento")
        if doc_id and doc_id not in vistos:
            print(f"Documento ID: {doc_id}, Nombre: {nombre}")
            vistos[doc_id] = nombre

    return [{"documento_id": doc_id, "nombre_documento": nombre} for doc_id, nombre in vistos.items()]