import os
import json
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from groq import Groq
from typing import List, Dict, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '.env.local')

load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY_TEST") or os.getenv("GROQ_API_KEY_PROD") or os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or "your_groq" in GROQ_API_KEY:
    print("WARNING: Groq API key is missing or invalid in .env.local")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"

def chat_with_agent(messages: List[Dict[str, str]], system_prompt: str = None) -> str:

    api_messages = []
    
    if system_prompt:
        api_messages.append({"role": "system", "content": system_prompt})
        
    api_messages.extend(messages)

    try:
        chat_completion = client.chat.completions.create(
            messages=api_messages,
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "I apologize, but I am currently experiencing connection issues. Please try again later."


def generate_itinerary(destination: str, duration_days: int, budget_level: str, travel_style: str = "balanced") -> Dict[str, Any]:

    system_prompt = (
        "You are an expert travel planner. You MUST respond with ONLY valid, parseable JSON. "
        "Do not include any introductory or concluding text, and do not wrap the JSON in markdown formatting (like ```json). "
        "Your response must adhere to the following JSON structure exactly:\n\n"
        "{\n"
        '  "destination": "Name of the destination",\n'
        '  "total_estimated_cost": 1500.00,\n'
        '  "days": [\n'
        "    {\n"
        '      "day_number": 1,\n'
        '      "hotel_suggestion": "Name of a good hotel (optional)",\n'
        '      "activities": [\n'
        "        {\n"
        '          "time_of_day": "morning",\n'
        '          "title": "Activity Title",\n'
        '          "description": "Detailed description of the activity",\n'
        '          "estimated_cost": 50.00\n'
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "ai_notes": "Any extra advice, tips, or packing suggestions."\n'
        "}"
    )

    user_prompt = f"Please generate a detailed {duration_days}-day itinerary for {destination}. Budget level: {budget_level}. Travel style: {travel_style}."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=MODEL_NAME,
            temperature=0.5,
            response_format={"type": "json_object"},
            max_tokens=4000,
        )
        
        json_response = chat_completion.choices[0].message.content
        return json.loads(json_response)
        
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return None
