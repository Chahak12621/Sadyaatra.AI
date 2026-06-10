from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, TripRequest, ItineraryResponse
from core.llm_client import chat_with_agent, generate_itinerary
from core.supabase_client import save_itinerary
import json

from routers import users, agents, groups, itineraries

app = FastAPI(title="Sadyaatra Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(agents.router)
app.include_router(groups.router)
app.include_router(itineraries.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Sadyaatra API is running!"}

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
   
    latest_user_msg = request.messages[-1].content if request.messages else ""
    rag_context = ""
    
    if latest_user_msg:
        try:
            from core.embedding_client import generate_embedding
            from core.supabase_client import search_knowledge_base
            
            query_embedding = generate_embedding(latest_user_msg)
            matching_facts = search_knowledge_base(query_embedding, match_threshold=0.4, match_count=3)
            
            if matching_facts:
                rag_context = "IMPORTANT INTERNAL FACTS from the database to help answer the user:\n"
                for fact in matching_facts:
                    rag_context += f"- {fact.get('title', '')}: {fact.get('content', '')}\n"
        except Exception as e:
            print(f"Warning: RAG Retrieval failed: {e}")

    system_prompt = "You are a helpful, expert travel agent for Sadyaatra. Keep your responses concise and engaging."
    
    if rag_context:
        system_prompt += f"\n\n{rag_context}\n"
        
    if request.current_context:
        system_prompt += f" Context to keep in mind: {request.current_context}"
        
    try:
        response_text = chat_with_agent(messages, system_prompt)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Chat Error: {str(e)}")


@app.post("/api/itinerary", response_model=ItineraryResponse)
def generate_trip_itinerary(request: TripRequest):

    try:
        itinerary_data = generate_itinerary(
            destination=request.destination,
            duration_days=request.duration_days,
            budget_level=request.budget_level,
            travel_style=request.travel_style
        )
        
        if not itinerary_data:
            raise HTTPException(status_code=500, detail="Failed to generate itinerary from AI.")
            
        if request.user_id:
            try:
                save_itinerary(
                    user_id=request.user_id,
                    destination=request.destination,
                    itinerary_json=itinerary_data,
                    total_budget=itinerary_data.get("total_estimated_cost")
                )
            except Exception as e:
                print(f"Warning: Failed to save itinerary to Supabase: {e}")
                
        return itinerary_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Itinerary Generation Error: {str(e)}")
