from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.clan import Clan
from models.sicario import Sicario
from schemas.clan import ClanCreate, ClanOut
from typing import List, Optional

router = APIRouter(prefix="/clan", tags=["clan"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ClanOut])
def list_clans(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    clans = db.query(Clan).offset(skip).limit(limit).all()
    return clans

@router.get("/search", response_model=List[ClanOut])
def search_clans(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Clan)
    if name:
        query = query.filter(Clan.name.ilike(f"%{name}%"))
    return query.all()

@router.get("/{clan_id}", response_model=ClanOut)
def get_clan(clan_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    return clan

@router.post("/", response_model=ClanOut)
def create_clan(clan: ClanCreate, db: Session = Depends(get_db), leader_id: Optional[int] = None):
    db_clan = Clan(
        name=clan.name,
        description=clan.description,
        leader_id=leader_id,
        general_id=clan.general_id,
        guardian_ids=clan.guardian_ids[:5] if clan.guardian_ids else [],
        legendary_item=clan.legendary_item,
        legendary_weapon=clan.legendary_weapon
    )
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    return db_clan

@router.put("/{clan_id}", response_model=ClanOut)
def update_clan(clan_id: int, clan: ClanCreate, db: Session = Depends(get_db)):
    db_clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not db_clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    db_clan.name = clan.name
    db_clan.description = clan.description
    db_clan.general_id = clan.general_id
    db_clan.guardian_ids = clan.guardian_ids[:5] if clan.guardian_ids else []
    db_clan.legendary_item = clan.legendary_item
    db_clan.legendary_weapon = clan.legendary_weapon
    db.commit()
    db.refresh(db_clan)
    return db_clan

@router.post("/{clan_id}/transfer_leader", response_model=ClanOut)
def transfer_leader(clan_id: int, new_leader_id: int, db: Session = Depends(get_db)):
    db_clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not db_clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    db_clan.leader_id = new_leader_id
    db.commit()
    db.refresh(db_clan)
    return db_clan

@router.delete("/{clan_id}")
def delete_clan(clan_id: int, db: Session = Depends(get_db)):
    db_clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not db_clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    db.delete(db_clan)
    db.commit()
    return {"detail": "Clan deleted"}

@router.post("/{clan_id}/invite_member")
def invite_member(clan_id: int, member_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    # Implement logic to add member_id to pending invitations (requires model update)
    # For now, assume clan.pending_invitations exists
    if hasattr(clan, 'pending_invitations'):
        if member_id not in clan.pending_invitations:
            clan.pending_invitations.append(member_id)
            db.commit()
    return {"detail": "Invitation sent"}

@router.post("/{clan_id}/accept_invite")
def accept_invite(clan_id: int, member_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    # Move member from pending_invitations to members (requires model update)
    if hasattr(clan, 'pending_invitations') and hasattr(clan, 'members'):
        if member_id in clan.pending_invitations:
            clan.pending_invitations.remove(member_id)
            clan.members.append(member_id)
            db.commit()
    return {"detail": "Member joined clan"}

@router.post("/{clan_id}/reject_invite")
def reject_invite(clan_id: int, member_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    if hasattr(clan, 'pending_invitations'):
        if member_id in clan.pending_invitations:
            clan.pending_invitations.remove(member_id)
            db.commit()
    return {"detail": "Invitation rejected"}

@router.post("/{clan_id}/expel_member")
def expel_member(clan_id: int, member_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    if hasattr(clan, 'members'):
        if member_id in clan.members:
            clan.members.remove(member_id)
            db.commit()
    return {"detail": "Member expelled"}

@router.post("/{clan_id}/set_guardians")
def set_guardians(clan_id: int, guardian_ids: List[int], db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    clan.guardian_ids = guardian_ids[:3]  # Máximo 3 guardianes
    db.commit()
    db.refresh(clan)
    return clan

@router.post("/{clan_id}/hire_sicario")
def hire_sicario(clan_id: int, sicario_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    if not sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    if sicario.is_available != 1:
        raise HTTPException(status_code=400, detail="Sicario is not available")
    # Check clan treasury (assume clan.treasury exists)
    if hasattr(clan, 'treasury') and clan.treasury < sicario.price:
        raise HTTPException(status_code=400, detail="Not enough treasury to hire sicario")
    # Deduct price and hire
    if hasattr(clan, 'treasury'):
        clan.treasury -= sicario.price
    sicario.is_available = 0
    db.commit()
    db.refresh(clan)
    db.refresh(sicario)
    return {"detail": "Sicario hired", "sicario_id": sicario_id, "clan_id": clan_id}

@router.post("/{clan_id}/release_sicario")
def release_sicario(clan_id: int, sicario_id: int, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    sicario = db.query(Sicario).filter(Sicario.id == sicario_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    if not sicario:
        raise HTTPException(status_code=404, detail="Sicario not found")
    sicario.is_available = 1
    db.commit()
    db.refresh(sicario)
    return {"detail": "Sicario released", "sicario_id": sicario_id, "clan_id": clan_id}
