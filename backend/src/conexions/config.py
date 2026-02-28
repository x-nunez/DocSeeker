# SPDX-License-Identifier: Apache-2.0

# src/config.py
import os
from qdrant_client import QdrantClient
import psycopg2

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "merlin")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

postgres_connection = None

def get_postgres_connection():
    global postgres_connection
    if postgres_connection is None:
        postgres_connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
    return postgres_connection

from google import genai
from google.genai import types

GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)
