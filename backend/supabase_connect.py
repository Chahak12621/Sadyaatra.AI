import os
from dotenv import load_dotenv
from supabase import create_client, Client

backend_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(backend_dir, '.env.local')

load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("Connecting to Supabase...")
print(f"URL: {SUPABASE_URL}")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env.local")
    exit(1)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Connection Successful!\n")
    
    print("Checking tables...")
    tables_to_check = [
        "user_profiles",
        "agent_profiles",
        "chat_messages",
        "knowledge_base",
        "trip_groups",
        "group_members",
        "itineraries"
    ]
    
    for table in tables_to_check:
        try:
            response = supabase.table(table).select("*").limit(1).execute()
            print(f" OK Table '{table}' is accessible via Python.")
        except Exception as e:
            print(f" NOT OK Table '{table}': {e}")

    print("\n---------------------------------------------------------")
    print("NOTE ON SCHEMAS AND POLICIES:")
    print("The Supabase Python Client (which uses REST APIs) is designed ")
    print("for reading/writing data, not for querying database metadata ")
    print("(like raw schemas or security policies).")
    print("To view your schemas and policies, you should always use the ")
    print("Supabase Dashboard or the SQL queries you ran earlier!")
    print("---------------------------------------------------------")

except Exception as e:
    print(f"\nFailed to connect to Supabase: {e}")
