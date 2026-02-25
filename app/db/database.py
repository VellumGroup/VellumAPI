from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)