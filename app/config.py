import os
import supabase
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
DEBUG = True
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)