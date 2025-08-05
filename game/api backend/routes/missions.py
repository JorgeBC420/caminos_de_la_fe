from fastapi import APIRouter

router = APIRouter(prefix="/missions", tags=["missions"])

@router.get("")
def get_missions():
    # TODO: Implement missions retrieval
    return {"missions": []}
