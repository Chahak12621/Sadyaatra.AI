from fastapi import APIRouter, HTTPException
from models.schemas import UserCreateSchema, UserProfileSchema
from core.supabase_client import create_user_profile, get_user_profile
import uuid

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=UserProfileSchema)
def create_user(user: UserCreateSchema):
    try:
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": user.email,
            "full_name": user.full_name,
            "role": "user",
            "onboarding_preferences": {
                "phone": user.phone,
                "dob": str(user.dob) if user.dob else None,
                "gender": user.gender,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "pincode": user.pincode
            }
        }
        created_user = create_user_profile(user_data)
        if not created_user:
            raise HTTPException(status_code=500, detail="Failed to create user profile")
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserProfileSchema)
def get_user(user_id: str):
    try:
        user_profile = get_user_profile(user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        return user_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
