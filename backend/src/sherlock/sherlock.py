from src.db import interfazDB
from fastapi import APIRouter
from .search import router as search_router

router = APIRouter()
router.include_router(search_router)

@router.get("/busquedaExacta")
def busquedaExacta(string):
    """
    Searches for files using a description.


    Returns:
        list: A list of records matching the regex pattern. Returns an empty list if no matches are found.
    """
    documents = interfazDB.patternSearch(string)

@router.get("/busquedaVectorial")
def busquedaVectorial(vector):
    """
    Searches for files using a vector representation of the query.

    Returns:
        list: A list of records matching the vector query. Returns an empty list if no matches are found.
    """
    documents = interfazDB.vectorSearch(vector)


