from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("")
def get_items():
    # TODO: Implement items retrieval
    return {"items": []}
