from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from models.schemas import TripGroupSchema, GroupMemberSchema
from core.supabase_client import create_trip_group, add_group_member, get_group_profiles
import uuid

router = APIRouter(prefix="/api/groups", tags=["Groups"])

class GroupCreateRequest(BaseModel):
    name: str
    created_by: str
    destination: str | None = None

class AddMemberRequest(BaseModel):
    user_id: str
    role: str = "member"

@router.post("/", response_model=TripGroupSchema)
def create_group(request: GroupCreateRequest):
    try:
        group_id = str(uuid.uuid4())
        group_data = {
            "id": group_id,
            "name": request.name,
            "created_by": request.created_by,
            "destination": request.destination
        }
        created_group = create_trip_group(group_data)
        if not created_group:
            raise HTTPException(status_code=500, detail="Failed to create group")
        add_group_member(group_id, request.created_by, "admin")
        return created_group
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{group_id}/members", response_model=GroupMemberSchema)
def add_member(group_id: str, request: AddMemberRequest):
    try:
        member = add_group_member(group_id, request.user_id, request.role)
        if not member:
            raise HTTPException(status_code=500, detail="Failed to add member")
        return member
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{group_id}/members")
def get_members(group_id: str):
    try:
        profiles = get_group_profiles(group_id)
        return profiles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
