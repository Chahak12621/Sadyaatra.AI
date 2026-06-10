from fastapi import APIRouter, HTTPException
from models.schemas import AgentCreateSchema, AgentProfileSchema
from core.supabase_client import create_agent_profile, get_agent_profile
import uuid

router = APIRouter(prefix="/api/agents", tags=["Agents"])

@router.post("/", response_model=AgentProfileSchema)
def create_agent(agent: AgentCreateSchema):
    try:
        agent_id = str(uuid.uuid4())
        agent_data = agent.model_dump()
        agent_data["id"] = agent_id
        agent_data["role"] = "agent"
        agent_data["status"] = "pending_review"
        if "password" in agent_data:
            del agent_data["password"]
        if agent_data.get("dob"):
            agent_data["dob"] = str(agent_data["dob"])
        if agent_data.get("licence_expiry"):
            agent_data["licence_expiry"] = str(agent_data["licence_expiry"])
        created_agent = create_agent_profile(agent_data)
        if not created_agent:
            raise HTTPException(status_code=500, detail="Failed to create agent profile")
        return created_agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}", response_model=AgentProfileSchema)
def get_agent(agent_id: str):
    try:
        agent_profile = get_agent_profile(agent_id)
        if not agent_profile:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
