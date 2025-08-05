from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.sicario import Sicario
from schemas.sicario import SicarioCreate, SicarioOut
from typing import List, Optional

router = APIRouter(prefix="/sicario", tags=["sicario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[SicarioOut])
def list_sicarios(available: Optional[int] = 1, db: Session = Depends(get_db)):
    query = db.query(Sicario)
    if available is not None:
        query = query.filter(Sicario.is_available == available)
    return query.all()

@router.post("/", response_model=SicarioOut)
def create_sicario(sicario: SicarioCreate, db: Session = Depends(get_db)):
    db_sicario = Sicario(**sicario.dict())
    db.add(db_sicario)
    db.commit()
    db.refresh(db_sicario)
    return db_sicario

@router.put("/{sicario_id}", response_model=SicarioOut)
def update_sicario(sicario_id: int, sicario: SicarioCreate, db: Session = Depends(get_db)):
    db_sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not db_sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    for key, value in sicario.dict().items():
        setattr(db_sicario, key, value)
    db.commit()
    db.refresh(db_sicario)
    return db_sicario

@router.post("/{sicario_id}/hire")
def hire_sicario(sicario_id: int, db: Session = Depends(get_db)):
    db_sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not db_sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    db_sicario.is_available = 0
    db.commit()
    db.refresh(db_sicario)
    return db_sicario

@router.post("/{sicario_id}/release")
def release_sicario(sicario_id: int, db: Session = Depends(get_db)):
    db_sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not db_sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    db_sicario.is_available = 1
    db.commit()
    db.refresh(db_sicario)
    return db_sicario
