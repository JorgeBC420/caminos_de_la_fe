from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.item import InventorySchema, ItemSchema
from models.item import Item
from core.database import get_db
from core.auth import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("", response_model=InventorySchema)
def get_inventory(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = []
    for item_name in user.inventory:
        # Buscar el item por nombre
        item = db.query(Item).filter_by(name=item_name).first()
        if item:
            items.append(ItemSchema(
                id=item.id,
                name=item.name,
                type=item.type,
                rarity=item.rarity,
                description=item.description,
                stats=item.stats,
                effects=item.effects
            ))
    return InventorySchema(user_id=user.id, items=items)
