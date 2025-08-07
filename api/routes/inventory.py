from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models.inventory import Inventory, InventoryItem
from api.models.player import Player
from api.routes.dependencies import get_db

router = APIRouter()

@router.get('/inventory/{player_id}')
def get_inventory(player_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.player_id == player_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail='Inventory not found')
    return {
        'player_id': player_id,
        'items': [
            {'item_id': item.item_id, 'name': item.name, 'item_type': item.item_type, 'quantity': item.quantity}
            for item in inventory.items
        ]
    }

@router.post('/inventory/{player_id}/add')
def add_item(player_id: int, item: dict, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.player_id == player_id).first()
    if not inventory:
        inventory = Inventory(player_id=player_id)
        db.add(inventory)
        db.commit()
        db.refresh(inventory)
    inv_item = InventoryItem(
        inventory_id=inventory.id,
        item_id=item['item_id'],
        name=item['name'],
        item_type=item['item_type'],
        quantity=item.get('quantity', 1)
    )
    db.add(inv_item)
    db.commit()
    db.refresh(inv_item)
    return {'status': 'ok', 'item': {'item_id': inv_item.item_id, 'name': inv_item.name, 'item_type': inv_item.item_type, 'quantity': inv_item.quantity}}

@router.delete('/inventory/{player_id}/remove')
def remove_item(player_id: int, item_id: str, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.player_id == player_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail='Inventory not found')
    inv_item = db.query(InventoryItem).filter(InventoryItem.inventory_id == inventory.id, InventoryItem.item_id == item_id).first()
    if not inv_item:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(inv_item)
    db.commit()
    return {'status': 'ok'}
