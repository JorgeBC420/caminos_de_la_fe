from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from core.auth import get_current_user
from core.database import get_db
from models.brotherhood import Brotherhood

router = APIRouter(prefix="/brotherhood", tags=["brotherhood"])

from models.brotherhood import Brotherhood
@router.post("/invite")
from schemas.brotherhood import BrotherhoodCreate, BrotherhoodOut
    target_id: int,
    db: Session = Depends(get_db),
router = APIRouter(prefix="/brotherhood", tags=["brotherhood"])
):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.general_id == user_id.id or user_id.id in Brotherhood.guardian_ids).first()
    if not brotherhood:
        raise HTTPException(status_code=403, detail="No tienes permisos para invitar")
    if target_id in brotherhood.members or target_id in brotherhood.pending_invitations:
        raise HTTPException(status_code=400, detail="Ya es miembro o está invitado")
    brotherhood.pending_invitations.append(target_id)
    db.commit()
@router.get("/", response_model=List[BrotherhoodOut])
def list_brotherhoods(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    brotherhoods = db.query(Brotherhood).offset(skip).limit(limit).all()
    return brotherhoods
    db: Session = Depends(get_db),
@router.get("/search", response_model=List[BrotherhoodOut])
def search_brotherhoods(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Brotherhood)
    if not brotherhood:
        query = query.filter(Brotherhood.name.ilike(f"%{name}%"))
    brotherhood.pending_invitations.remove(user_id.id)
    brotherhood.members.append(user_id.id)
@router.get("/{brotherhood_id}", response_model=BrotherhoodOut)
def get_brotherhood(brotherhood_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    return brotherhood
    user_id: int = Depends(get_current_user)
@router.post("/", response_model=BrotherhoodOut)
def create_brotherhood(brotherhood: BrotherhoodCreate, db: Session = Depends(get_db), leader_id: Optional[int] = None):
    db_brotherhood = Brotherhood(
        raise HTTPException(status_code=404, detail="No tienes invitación pendiente")
    brotherhood.pending_invitations.remove(user_id.id)
    db.commit()
    return {"success": True}

@router.post("/expel_member")
def expel_member(
    target_id: int,
    db.add(db_brotherhood)
    db.commit()
    db.refresh(db_brotherhood)
    return db_brotherhood
    if not brotherhood:
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
):
@router.post("/{brotherhood_id}/transfer_leader", response_model=BrotherhoodOut)
def transfer_leader(brotherhood_id: int, new_leader_id: int, db: Session = Depends(get_db)):
    db_brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not db_brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    db_brotherhood.leader_id = new_leader_id
    db.commit()
    db.refresh(db_brotherhood)
    return db_brotherhood
    else:
@router.delete("/{brotherhood_id}")
def delete_brotherhood(brotherhood_id: int, db: Session = Depends(get_db)):
    db_brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not db_brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    db.delete(db_brotherhood)
    db.commit()
    return {"detail": "Brotherhood deleted"}
    db: Session = Depends(get_db)
@router.post("/{brotherhood_id}/invite_member")
def invite_member(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    logs = [
        f"Miembros: {brotherhood.members}",
    if hasattr(brotherhood, 'pending_invitations'):
        if member_id not in brotherhood.pending_invitations:
            brotherhood.pending_invitations.append(member_id)
            db.commit()
        f"Sicarios: {brotherhood.hired_sicarios}",
        f"Recursos robados: {brotherhood.stolen_resources}"
@router.post("/{brotherhood_id}/accept_invite")
def accept_invite(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
def donate_to_treasury(
    amount: int,
        if member_id in brotherhood.pending_invitations:
            brotherhood.pending_invitations.remove(member_id)
            brotherhood.members.append(member_id)
            db.commit()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="No perteneces a una hermandad")
@router.post("/{brotherhood_id}/reject_invite")
def reject_invite(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
@router.post("/return_donation")
def return_donation(
    amount: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
@router.post("/{brotherhood_id}/expel_member")
def expel_member(brotherhood_id: int, member_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
    brotherhood.treasury -= amount
    brotherhood.returned_history.append(amount)
    db.commit()
    return {"success": True, "new_treasury": brotherhood.treasury}

@router.post("/expand_fortress")
@router.post("/{brotherhood_id}/set_guardians")
def set_guardians(brotherhood_id: int, guardian_ids: List[int], db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.general_id == user_id.id).first()
    if not brotherhood:
        raise HTTPException(status_code=403, detail="Solo el general puede expandir la fortaleza")
    if cost > brotherhood.treasury:
@router.post("/{brotherhood_id}/hire_sicario")
def hire_sicario(brotherhood_id: int, sicario_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")

@router.post("/steal_resources")
def steal_resources(
    target_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    target = db.query(Brotherhood).filter(Brotherhood.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Hermandad objetivo no encontrada")
    stolen = int(target.treasury * 0.5)
    target.treasury -= stolen
    target.stolen_resources += stolen
    db.commit()
    return {"success": True, "stolen": stolen, "target_treasury": target.treasury}

@router.post("/{brotherhood_id}/release_sicario")
def release_sicario(brotherhood_id: int, sicario_id: int, db: Session = Depends(get_db)):
    brotherhood = db.query(Brotherhood).filter(Brotherhood.id == brotherhood_id).first()
    sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not brotherhood:
        raise HTTPException(status_code=404, detail="Brotherhood not found")
