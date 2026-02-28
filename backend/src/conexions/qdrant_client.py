from qdrant_client import QdrantClient

def get_qdrant_client():
    """
    Initializes and returns a QdrantClient instance for connecting to the Qdrant vector database.

    Returns:
        QdrantClient: An instance of QdrantClient configured to connect to the specified Qdrant server.
    """
    return QdrantClient(host="localhost", port=6333)