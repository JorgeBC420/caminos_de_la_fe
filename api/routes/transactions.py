from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models.transaction import Transaction
from api.routes.dependencies import get_db

router = APIRouter()

@router.get('/transactions/{player_id}')
def get_transactions(player_id: int, db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter(Transaction.player_id == player_id).all()
    return [
        {'item_id': tx.item_id, 'item_name': tx.item_name, 'item_type': tx.item_type, 'price': tx.price, 'quantity': tx.quantity, 'type': tx.transaction_type, 'timestamp': tx.timestamp}
        for tx in txs
    ]

@router.post('/transactions')
def create_transaction(tx: dict, db: Session = Depends(get_db)):
    db_tx = Transaction(
        player_id=tx['player_id'],
        item_id=tx['item_id'],
        item_name=tx['item_name'],
        item_type=tx['item_type'],
        price=tx['price'],
        quantity=tx.get('quantity', 1),
        transaction_type=tx['transaction_type']
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return {'status': 'ok', 'transaction': {'id': db_tx.id}}
