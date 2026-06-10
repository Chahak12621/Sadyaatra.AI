import json
from core.llm_client import chat_with_agent, generate_itinerary

def run_tests():
    print("Testing Groq LLM Client...\n")

    print("Test 1: Chat")
    messages = [
        {"role": "user", "content": "What are the top 3 places to visit in Goa?"}
    ]
    system_prompt = "You are a helpful travel agent. Keep your answers brief, under 50 words."
    
    chat_response = chat_with_agent(messages, system_prompt)
    print(f"Agent Response:\n{chat_response}\n")

    print("Test 2: Structured JSON Itinerary")
    print("Generating a 2-day budget itinerary for Manali...")
    
    itinerary = generate_itinerary(
        destination="Manali",
        duration_days=2,
        budget_level="budget",
        travel_style="adventurous"
    )

    if itinerary:
        print("\nSuccessfully generated valid JSON itinerary!")
        print(json.dumps(itinerary, indent=2))
    else:
        print("\nFailed to generate or parse the itinerary JSON.")

if __name__ == "__main__":
    run_tests()
