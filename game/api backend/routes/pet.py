
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.pet import Pet
from schemas.pet import PetSchema

router = APIRouter(prefix="/pet", tags=["pet"])

# Listar mascotas del usuario
@router.get("/", response_model=list[PetSchema])
def list_pets(user_id: int, db: Session = Depends(get_db)):
    pets = db.query(Pet).filter(Pet.owner_id == user_id).all()
    return pets

# Activar mascota
@router.post("/activate")
def activate_pet(user_id: int, pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == user_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    # Aquí podrías guardar el estado de mascota activa en el usuario
    return {"success": True, "active_pet": pet_id}

# Enviar mascota a guardería
@router.post("/nursery/send")
def send_to_nursery(user_id: int, pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == user_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    pet.in_nursery = 1
    # pet.shelter_timestamp = int(time.time()) # Si usas timestamp
    db.commit()
    return {"success": True, "pet_id": pet_id, "in_nursery": True}

# Subir de nivel mascota (ejemplo)
@router.post("/levelup")
def level_up_pet(user_id: int, pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == user_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    pet.level += 1
    pet.exp = 0
    pet.exp_to_next = int(pet.exp_to_next * 1.5)
    db.commit()
    return {"success": True, "pet_id": pet_id, "new_level": pet.level}
