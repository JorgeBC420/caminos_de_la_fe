
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models.mount_sql import Mount as MountSQL
from api.models.player_sql import Player
from api.routes.dependencies import get_db

router = APIRouter()

# CRUD real para monturas
@router.get("/mounts/{player_id}")
def get_mounts(player_id: int, db: Session = Depends(get_db)):
    mounts = db.query(MountSQL).filter(MountSQL.owner_id == player_id).all()
    return {"player_id": player_id, "mounts": [
        {"id": m.id, "mount_type": m.mount_type, "speed_bonus": m.speed_bonus, "active": m.active} for m in mounts
    ]}

@router.post("/mounts/{player_id}")
def create_mount(player_id: int, mount: dict, db: Session = Depends(get_db)):
    db_mount = MountSQL(
        owner_id=player_id,
        mount_type=mount['mount_type'],
        speed_bonus=mount.get('speed_bonus', 2.0),
        model=mount.get('model', 'cube'),
        color=mount.get('color'),
        active=mount.get('active', False)
    )
    db.add(db_mount)
    db.commit()
    db.refresh(db_mount)
    return {"status": "ok", "mount": {"id": db_mount.id, "mount_type": db_mount.mount_type}}

@router.delete("/mounts/{player_id}/{mount_id}")
def delete_mount(player_id: int, mount_id: int, db: Session = Depends(get_db)):
    mount = db.query(MountSQL).filter(MountSQL.owner_id == player_id, MountSQL.id == mount_id).first()
    if not mount:
        raise HTTPException(status_code=404, detail="Mount not found")
    db.delete(mount)
    db.commit()
    return {"status": "ok"}

@router.post("/mounts/{player_id}/activate")
def activate_mount(player_id: int, mount_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    # player.active_mount_id = mount_id
    # db.commit()
    return {"status": "activated", "player_id": player_id, "mount_id": mount_id}
