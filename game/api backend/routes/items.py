from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemSchema
from core.database import get_db

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=list[ItemSchema])
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [ItemSchema(
        id=i.id,
        name=i.name,
        type=i.type,
        rarity=i.rarity,
        description=i.description,
        stats=i.stats,
        effects=i.effects
    ) for i in items]
