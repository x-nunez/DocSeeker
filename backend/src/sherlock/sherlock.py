from src.db import interfazDB
from fastapi import APIRouter
from .search import router as search_router
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()
router.include_router(search_router)

class FiltrosBusqueda(BaseModel):
    nombre: Optional[str] = None
    path: Optional[str] = None
    extension: Optional[str] = None
    size_min: Optional[int] = None
    size_max: Optional[int] = None
    date_min: Optional[datetime] = None
    date_max: Optional[datetime] = None

@router.post("/busquedaExacta")  # Fix: cambiado a POST para recibir body JSON
def busquedaExacta(filtros: FiltrosBusqueda):
    """
    Searches for files using filters received from a React form as JSON.
    Returns:
        list: A list of records matching the filters.
    """
    results = []

    if filtros.nombre:
        results = interfazDB.patternSearchByName(f"%{filtros.nombre}%")

    if filtros.path:
        by_path = interfazDB.patternSearchByPath(f"%{filtros.path}%")
        results = by_path if not results else [r for r in results if r in by_path]

    if filtros.extension:
        by_extension = interfazDB.patternSearchByExtension(f"%{filtros.extension}%")
        results = by_extension if not results else [r for r in results if r in by_extension]

    if filtros.size_min is not None or filtros.size_max is not None:
        by_size = interfazDB.patternSearchBySize(filtros.size_min, filtros.size_max)
        results = by_size if not results else [r for r in results if r in by_size]

    if filtros.date_min is not None or filtros.date_max is not None:
        by_date = interfazDB.patternSearchByCreationDate(filtros.date_min, filtros.date_max)
        results = by_date if not results else [r for r in results if r in by_date]

    return results

@router.get("/busquedaVectorial")
def busquedaVectorial(string):
    """
    Searches for files using a vector representation of the query.

    Returns:
        list: A list of records matching the vector query. Returns an empty list if no matches are found.
    """
    documents = interfazDB.vectorSearch(string)
    return documents


