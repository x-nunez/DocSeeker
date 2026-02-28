# src/config.py
from qdrant_client import QdrantClient
import psycopg2
from sentence_transformers import SentenceTransformer

qdrant_client = QdrantClient(host="localhost", port=6333)
postgres_connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="merlin",
        user="postgres",
        password="postgres"
    )
model = SentenceTransformer("all-MiniLM-L6-v2")