
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models.pet import Pet as PetPydantic
from api.models.player_sql import Player
from api.models.base import Base
from api.models import Pet as PetSQL
from api.routes.dependencies import get_db

router = APIRouter()

# CRUD real para mascotas
@router.get("/pets/{player_id}")
def get_pets(player_id: int, db: Session = Depends(get_db)):
    pets = db.query(PetSQL).filter(PetSQL.owner_id == player_id).all()
    return {"player_id": player_id, "pets": [
        {"id": p.id, "pet_type": p.pet_type, "tier": p.tier, "level": p.level, "exp": p.exp, "stats": p.stats} for p in pets
    ]}

@router.post("/pets/{player_id}")
def create_pet(player_id: int, pet: dict, db: Session = Depends(get_db)):
    db_pet = PetSQL(
        owner_id=player_id,
        pet_type=pet['pet_type'],
        tier=pet.get('tier', 'comun'),
        level=pet.get('level', 1),
        exp=pet.get('exp', 0),
        stats=pet.get('stats', {})
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return {"status": "ok", "pet": {"id": db_pet.id, "pet_type": db_pet.pet_type}}

@router.delete("/pets/{player_id}/{pet_id}")
def delete_pet(player_id: int, pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetSQL).filter(PetSQL.owner_id == player_id, PetSQL.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"status": "ok"}

@router.post("/pets/{player_id}/activate")
def activate_pet(player_id: int, pet_id: int, db: Session = Depends(get_db)):
    # Lógica para activar mascota (ejemplo: marcar como activa en el jugador)
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    # Aquí podrías guardar el id de la mascota activa en el modelo Player
    # player.active_pet_id = pet_id
    # db.commit()
    return {"status": "activated", "player_id": player_id, "pet_id": pet_id}
