from fastapi import APIRouter

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("")
def get_inventory():
    # TODO: Implement inventory retrieval
    return {"inventory": []}
