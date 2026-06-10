# https://github.com/supabase/supabase-py 

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '.env.local')
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") 

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env file.")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

def get_user_profile(user_id: str) -> Dict[str, Any]:
    response = supabase.table("user_profiles").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None

def get_group_profiles(group_id: str) -> List[Dict[str, Any]]:
    members = supabase.table("group_members").select("user_id").eq("group_id", group_id).execute()
    user_ids = [m["user_id"] for m in members.data]
    if not user_ids:
        return []
    profiles = supabase.table("user_profiles").select("*").in_("id", user_ids).execute()
    return profiles.data

def save_itinerary(user_id: str, destination: str, itinerary_json: dict, total_budget: float = None) -> Any:
    data = {
        "user_id": user_id,
        "destination": destination,
        "itinerary_json": itinerary_json,
        "total_budget": total_budget
    }
    response = supabase.table("itineraries").insert(data).execute()
    return response.data

def search_knowledge_base(query_embedding: List[float], match_threshold: float = 0.7, match_count: int = 5) -> List[Dict[str, Any]]:
    response = supabase.rpc(
        "match_knowledge_base",
        {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count
        }
    ).execute()
    return response.data