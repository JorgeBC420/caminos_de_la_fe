from fastapi import APIRouter, HTTPException
import json
import os
from typing import List, Optional

router = APIRouter(prefix="/story", tags=["story"])

STORY_PATH = os.path.join(os.path.dirname(__file__), '../client/data/missions/mission_story.json')

@router.get("/", response_model=List[dict])
def list_chapters():
    try:
        with open(STORY_PATH, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
    except Exception:
        chapters = []
    return chapters

@router.get("/{chapter_id}", response_model=dict)
def get_chapter(chapter_id: int):
    try:
        with open(STORY_PATH, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        if 0 <= chapter_id < len(chapters):
            return chapters[chapter_id]
    except Exception:
        pass
    raise HTTPException(status_code=404, detail="Chapter not found")

@router.get("/act/{act_id}", response_model=List[dict])
def get_act(act_id: int):
    try:
        with open(STORY_PATH, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        act_chapters = [ch for ch in chapters if ch.get('act') == act_id]
        return act_chapters
    except Exception:
        pass
    raise HTTPException(status_code=404, detail="Act not found")
