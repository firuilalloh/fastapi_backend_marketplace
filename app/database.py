from supabase import create_client, Client
from app.config import Settings

def get_supabase_client() -> Client:
    try:
        supabase_url = Settings.supabase_url
        supabase_key = Settings.supabase_anon_key
        supabase: Client = create_client(supabase_url, supabase_key)
        return supabase
    
    except Exception as e:
        print("Error creating Supabase client:", e)
        raise e