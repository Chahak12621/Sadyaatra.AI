from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import ItinerarySchema
from core.supabase_client import get_user_itineraries

router = APIRouter(prefix="/api/itineraries", tags=["Itineraries"])

@router.get("/user/{user_id}", response_model=List[ItinerarySchema])
def fetch_user_itineraries(user_id: str):
    try:
        itineraries = get_user_itineraries(user_id)
        return itineraries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
