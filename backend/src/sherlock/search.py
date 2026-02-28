from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/search")
def search(query: str = Query(..., min_length=1, description="Search text")):
    return {
        "ok": True,
        "query": query
    }