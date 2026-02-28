import os
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def procesar_txt(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def generar_vectores(chunks):
    embeddings = model.encode(chunks)
    return embeddings

def compare(lista):
    vectors = np.array([i for i in lista])
    similarity_matrix = cosine_similarity(vectors)
    print(similarity_matrix)