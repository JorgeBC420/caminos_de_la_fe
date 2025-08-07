from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models.item import Item
from api.routes.dependencies import get_db

router = APIRouter()

@router.get('/items')
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [
        {'item_id': item.item_id, 'name': item.name, 'item_type': item.item_type, 'rarity': item.rarity, 'description': item.description}
        for item in items
    ]

@router.post('/items')
def create_item(item: dict, db: Session = Depends(get_db)):
    db_item = Item(
        item_id=item['item_id'],
        name=item['name'],
        item_type=item.get('item_type', ''),
        rarity=item.get('rarity', ''),
        description=item.get('description', '')
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {'status': 'ok', 'item': {'item_id': db_item.item_id, 'name': db_item.name}}

@router.delete('/items/{item_id}')
def delete_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(item)
    db.commit()
    return {'status': 'ok'}
