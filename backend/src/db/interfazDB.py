from main import qdrant_client, postgres_connection
from qdrant_client.models import VectorParams, Distance

def crearCollection():
    collections = qdrant_client.get_collections().collections
    collection_name = "documents"
    vector_size = 128  # Tamaño del vector de características

    if collection_name not in collections:
        qdrant_client.create_collection(
                                        collection_name=collection_name,
                                        vectors_config=VectorParams(
                                                                    size=vector_size,
                                                                    distance=Distance.COSINE
                                                                    )
                                        )

def insertarDocumento(document):
    # Implementación de la inserción de un documento en la base de datos
    qdrant_client.upsert(
                        collection_name="documents",
                        points=[
                            {
                                "id": document.path,  # Asegúrate de que el documento tenga un ID único
                                "vector": document.vector,  # El vector de características del documento
                                "payload": {
                                    "name": document.name,
                                    "extension": document.extension,
                                }
                            }
                        ]
                    )

# Returns a list of Document elements
def patternSearch(name_pattern):

    with postgres_connection.cursor() as cursor:
        query = "SELECT * FROM documents WHERE name LIKE %s"
        cursor.execute(query, (name_pattern))
        results = cursor.fetchall()
        # Aquí puedes convertir los resultados a objetos Document si es necesario
        return results


def vectorSearch(vector):
    # Implementación de la búsqueda vectorial
    results = qdrant_client.search(collection_name="documents",
                                    query_vector=vector,
                                    limit=10,
                                    with_payload=True)
    return results