from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("https://sjfrzaogkavltubccfdv.supabase.co"),
    os.getenv("sb_publishable_5mvAANzGV5FUssiYL3x85w_aeRaV8wv")
)