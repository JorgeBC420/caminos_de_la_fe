from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.brotherhood import Brotherhood
from models.sicario import Sicario
from schemas.brotherhood import BrotherhoodCreate, BrotherhoodOut
from typing import List, Optional

router = APIRouter(prefix="/brotherhood", tags=["brotherhood"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[BrotherhoodOut])
def list_brotherhoods(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    brotherhoods = db.query(Brotherhood).offset(skip).limit(limit).all()
    return brotherhoods

@router.get("/search", response_model=List[BrotherhoodOut])
def search_brotherhoods(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Brotherhood)
    if name:
        query = query.filter(Brotherhood.name.ilike(f"%{name}%"))
    return query.all()

@router.get("/{brotherhood_id}", response_model=BrotherhoodOut)
def get_brotherhood(brotherhood_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    return brotherhood

@router.post("/", response_model=BrotherhoodOut)
def create_brotherhood(brotherhood: BrotherhoodCreate, db: Session = Depends(get_db), leader_id: Optional[int] = None):
    db_brotherhood = Brotherhood(
        name=brotherhood.name,
        description=brotherhood.description,
        leader_id=leader_id,
        general_id=brotherhood.general_id,
        guardian_ids=brotherhood.guardian_ids[:5] if brotherhood.guardian_ids else [],
        legendary_item=brotherhood.legendary_item,
        legendary_weapon=brotherhood.legendary_weapon
    )
    db.add(db_brotherhood)
    db.commit()
    db.refresh(db_brotherhood)
    return db_brotherhood

@router.put("/{brotherhood_id}", response_model=BrotherhoodOut)
def update_brotherhood(brotherhood_id: int, brotherhood: BrotherhoodCreate, db: Session = Depends(get_db)):
    db_brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not db_brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    db_brotherhood.name = brotherhood.name
    db_brotherhood.description = brotherhood.description
    db_brotherhood.general_id = brotherhood.general_id
    db_brotherhood.guardian_ids = brotherhood.guardian_ids[:5] if brotherhood.guardian_ids else []
    db_brotherhood.legendary_item = brotherhood.legendary_item
    db_brotherhood.legendary_weapon = brotherhood.legendary_weapon
    db.commit()
    db.refresh(db_brotherhood)
    return db_brotherhood

@router.post("/{brotherhood_id}/transfer_leader", response_model=BrotherhoodOut)
def transfer_leader(brotherhood_id: int, new_leader_id: int, db: Session = Depends(get_db)):
    db_brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not db_brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    db_brotherhood.leader_id = new_leader_id
    db.commit()
    db.refresh(db_brotherhood)
    return db_brotherhood

@router.delete("/{clan_id}")
def delete_brotherhood(brotherhood_id: int, db: Session = Depends(get_db)):
    db_brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not db_brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    db.delete(db_brotherhood)
    db.commit()
    return {"detail": "Brotherhood deleted"}

@router.post("/{clan_id}/invite_member")
def invite_member(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    if hasattr(brotherhood, 'pending_invitations'):
        if member_id not in brotherhood.pending_invitations:
            brotherhood.pending_invitations.append(member_id)
            db.commit()
    return {"detail": "Invitation sent"}

@router.post("/{clan_id}/accept_invite")
def accept_invite(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    if hasattr(brotherhood, 'pending_invitations') and hasattr(brotherhood, 'members'):
        if member_id in brotherhood.pending_invitations:
            brotherhood.pending_invitations.remove(member_id)
            brotherhood.members.append(member_id)
            db.commit()
    return {"detail": "Member joined brotherhood"}

@router.post("/{clan_id}/reject_invite")
def reject_invite(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    if hasattr(brotherhood, 'pending_invitations'):
        if member_id in brotherhood.pending_invitations:
            brotherhood.pending_invitations.remove(member_id)
            db.commit()
    return {"detail": "Invitation rejected"}

@router.post("/{clan_id}/expel_member")
def expel_member(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    if hasattr(brotherhood, 'members'):
        if member_id in brotherhood.members:
            brotherhood.members.remove(member_id)
            db.commit()
    return {"detail": "Member expelled"}

@router.post("/{clan_id}/set_guardians")
def set_guardians(brotherhood_id: int, guardian_ids: List[int], db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    brotherhood.guardian_ids = guardian_ids[:3]  # Máximo 3 guardianes
    db.commit()
    db.refresh(brotherhood)
    return brotherhood

@router.post("/{clan_id}/hire_sicario")
def hire_sicario(brotherhood_id: int, sicario_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    if not sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    if sicario.is_available != 1:
        raise HTTPException(status_code=400, detail="Sicario is not available")
    if hasattr(brotherhood, 'treasury') and brotherhood.treasury < sicario.price:
        raise HTTPException(status_code=400, detail="Not enough treasury to hire sicario")
    if hasattr(brotherhood, 'treasury'):
        brotherhood.treasury -= sicario.price
    sicario.is_available = 0
    db.commit()
    db.refresh(brotherhood)
    db.refresh(sicario)
    return {"detail": "Sicario hired", "sicario_id": sicario_id, "brotherhood_id": brotherhood_id}

@router.post("/{clan_id}/release_sicario")
def release_sicario(brotherhood_id: int, sicario_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    if not sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    sicario.is_available = 1
    db.commit()
    db.refresh(sicario)
    return {"detail": "Sicario released", "sicario_id": sicario_id, "brotherhood_id": brotherhood_id}
