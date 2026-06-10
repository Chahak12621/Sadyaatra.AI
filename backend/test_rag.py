import time
from core.supabase_client import supabase
from core.embedding_client import generate_embedding
from models.schemas import ChatRequest, ChatMessagePayload
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def run_rag_test():
    print("Testing RAG Integration...\n")
    
    fact_text = "Sadyaatra is offering a secret 50% discount on all Goa packages if you use the promo code GOA50 at checkout. This is a highly guarded secret."
    print("Step 1: Generating embedding for secret fact...")
    fact_embedding = generate_embedding(fact_text)
    
    print("Step 2: Inserting secret fact into Supabase...")
    try:
        response = supabase.table('knowledge_base').insert({
            'title': 'Secret Promo Code',
            'content': fact_text,
            'location_tags': ['Goa'],
            'embedding': fact_embedding
        }).execute()
        
        inserted_id = response.data[0]['id']
        print(f"Successfully inserted secret fact (ID: {inserted_id})\n")
    except Exception as e:
        print(f"Failed to insert fact into Supabase: {e}")
        print("Did you run the knowledge_base_rpc.sql script in your Supabase SQL Editor?")
        return
        
    time.sleep(1)

    print("Step 3: Asking the API 'Are there any discounts for Goa?'")
    chat_payload = {
        "messages": [
            {"role": "user", "content": "Are there any discounts for Goa?"}
        ]
    }
    
    response = client.post("/api/chat", json=chat_payload)
    
    if response.status_code == 200:
        print(f"\nAPI Response:\n{response.json()['response']}\n")
        print("If the AI mentioned 'GOA50', RAG is working perfectly!")
    else:
        print(f"\nAPI Request Failed: {response.status_code}")
        print(response.text)
        
    print("\nStep 4: Cleaning up dummy fact...")
    supabase.table('knowledge_base').delete().eq('id', inserted_id).execute()
    print("Done!")

if __name__ == "__main__":
    run_rag_test()
