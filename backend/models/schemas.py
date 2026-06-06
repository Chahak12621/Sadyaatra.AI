from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date, datetime 
from enum import Enum
from uuid import UUID 

# enums and constants 

class UserRole(str, Enum):
    USER = "user"

class AgentRole(str, Enum):
    AGENT = "agent" 

class SenderRole(str, Enum):
    USER = "user"
    AGENT = "agent"

class AgentStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected" 

class GroupMemberRole(str, Enum):
    MEMBER = "member"
    ADMIN = "admin" # fallback? 

# pydantic schemas

class UserProfileSchema(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    onboarding_preferences: Dict[str, Any]
    created_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore") 

class AgentProfileSchema(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[str] = None
    vehicle_color: Optional[str] = None
    seating_capacity: Optional[str] = None
    aadhar_number: Optional[str] = None
    pan_number: Optional[str] = None
    licence_number: Optional[str] = None
    licence_expiry: Optional[date] = None
    aadhar_front_url: Optional[str] = None
    aadhar_back_url: Optional[str] = None
    licence_image_url: Optional[str] = None
    vehicle_rc_url: Optional[str] = None
    vehicle_insurance_url: Optional[str] = None
    profile_photo_url: Optional[str] = None
    role: AgentRole
    status: AgentStatus
    rejection_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

class ChatMessageSchema(BaseModel):
    id: UUID
    sender_id: UUID
    sender_role: SenderRole
    receiver_id: UUID
    message: str
    read: bool
    created_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

class KnowledgeBaseSchema(BaseModel):
    id: UUID
    title: str
    content: str
    location_tags: List[str] = []
    embedding: List[float] = []
    created_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

class TripGroupSchema(BaseModel):
    id: UUID
    name: str
    created_by: UUID
    destination: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore") 

class GroupMemberSchema(BaseModel):
    group_id: UUID
    user_id: UUID
    role: GroupMemberRole
    joined_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

class ItinerarySchema(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    destination: str
    start_date: date
    end_date: date
    total_budget: Optional[float] = None
    itinerary_json: Dict[str, Any]
    created_at: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

# input schemas for validation
class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

class AgentCreateSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str
    dob: date
    gender: str
    address: str
    city: str
    state: str
    pincode: str
    vehicle_type: str
    vehicle_number: str
    vehicle_model: str
    vehicle_year: str
    vehicle_color: str
    seating_capacity: str
    aadhar_number: str
    pan_number: str
    licence_number: str
    licence_expiry: date
    aadhar_front_url: str
    aadhar_back_url: str
    licence_image_url: str
    vehicle_rc_url: str
    vehicle_insurance_url: str
    profile_photo_url: str

# api endpt models 

class TripRequest(BaseModel):
    destination: str = Field(..., description="The target city or region")
    duration_days: int = Field(..., ge=1, le=30, description="How many days the trip will last")
    budget_level: str = Field(..., description="E.g., 'budget', 'moderate', 'luxury'")
    travel_style: Optional[str] = Field("balanced", description="E.g., 'adventurous', 'relaxing', 'historical'")
    group_id: Optional[str] = Field(None, description="Supabase UUID for the group, if applicable")
    user_id: Optional[str] = Field(None, description="Supabase UUID for the solo user, if applicable")

class ChatMessagePayload(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="The message text")

class ChatRequest(BaseModel):
    messages: List[ChatMessagePayload] = Field(..., description="The full conversation history")
    current_context: Optional[str] = Field(None, description="Optional context for the AI")

class Activity(BaseModel):
    time_of_day: str
    title: str
    description: str
    estimated_cost: float

class ItineraryDay(BaseModel):
    day_number: int
    activities: List[Activity]
    hotel_suggestion: Optional[str] = None

class ItineraryResponse(BaseModel):
    """The strict JSON format the Groq AI MUST return."""
    destination: str
    total_estimated_cost: float
    days: List[ItineraryDay]
    ai_notes: str