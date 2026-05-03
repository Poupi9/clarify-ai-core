import os
from dotenv import load_dotenv

# 1. Load the variables from the hidden .env file into the system memory
load_dotenv()

# 2. Retrieve the variables securely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEXT_PUBLIC_SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
NEXT_PUBLIC_SUPABASE_ANON_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# 3. Safety check: Crash the program early with a clear error if a key is missing
if not GEMINI_API_KEY:
    raise ValueError("🚨 ERROR: Missing GEMINI_API_KEY in the .env file.")
    
if not NEXT_PUBLIC_SUPABASE_URL:
    raise ValueError("🚨 ERROR: Missing NEXT_PUBLIC_SUPABASE_URL in the .env file.")

if not NEXT_PUBLIC_SUPABASE_ANON_KEY:
    raise ValueError("🚨 ERROR: Missing NEXT_PUBLIC_SUPABASE_ANON_KEY in the .env file.")