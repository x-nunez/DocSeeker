#!/usr/bin/env python3

from fastapi import FastAPI
from sherlock.sherlock import router as search_router
from eater.eater import router as eater_router
from cloud.googleDrive import router as cloud_router
from conexions.qdrant_client import get_qdrant_client
from conexions.pg_conn import get_postgres_connection

app = FastAPI(title="Mi App Vectorial")
qdrant_client = get_qdrant_client()
postgres_connection = get_postgres_connection()

@app.get("/")
def root():
	return {"message": "Hello World"}

app.include_router(search_router, prefix="/sherlock", tags=["sherlock"])
app.include_router(cloud_router, prefix="/cloud", tags=["cloud"])

if __name__ == "__main__":
	root()
