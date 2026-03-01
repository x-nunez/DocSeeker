# SPDX-License-Identifier: Apache-2.0

from src.db import interfazDB
from fastapi import APIRouter
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.get("/busquedaExacta")
def busquedaExacta(
    nombre: Optional[str] = None,
    path: Optional[str] = None,
    extension: Optional[str] = None,
    size_min: Optional[int] = None,
    size_max: Optional[int] = None,
    date_min: Optional[datetime] = None,
    date_max: Optional[datetime] = None,
):
    """
    Searches for files using filters received from a React form as JSON.
    Returns:
        list: A list of records matching the filters.
    """
    results = []

    if nombre:
        results = interfazDB.patternSearchByName(nombre)

    if path:
        by_path = interfazDB.patternSearchByPath(path)
        results = by_path if not results else [r for r in results if r in by_path]

    if extension:
        by_extension = interfazDB.patternSearchByExtension(extension.split(".")[1])
        results = by_extension if not results else [r for r in results if r in by_extension]

    if size_min is not None or size_max is not None:
        by_size = interfazDB.patternSearchBySize(size_min, size_max)
        results = by_size if not results else [r for r in results if r in by_size]

    if date_min is not None or date_max is not None:
        by_date = interfazDB.patternSearchByCreationDate(date_min, date_max)
        results = by_date if not results else [r for r in results if r in by_date]

    return [
        {
            "nombre": i[1],
            "extension": i[3],
            "path": i[2],
            "link": i[8],
        }
        for i in results
    ]

@router.get("/busquedaVectorial")
def busquedaVectorial(string):
    """
    Searches for files using a vector representation of the query.

    Returns:
        list: A list of records matching the vector query. Returns an empty list if no matches are found.
    """
    print(string)
    documents = interfazDB.vectorSearch(string)
    print(f"Vector search results for query '{string}': {documents}")
    return documents


