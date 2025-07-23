
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Cargar .env desde el directorio raíz del proyecto (AGENTE_IA/.env)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def query_table(table_name: str, filters: dict = None, select: list = None, limit: int = None, order: str = None):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise EnvironmentError("SUPABASE_URL or SUPABASE_KEY not set in environment variables.")

    base_url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    params = []

    # Select columns
    if select:
        params.append(f"select={','.join(select)}")

    # Filters
    if filters:
        for key, value in filters.items():
            if isinstance(value, list):
                joined = ",".join(f'"{v}"' for v in value)
                params.append(f"{key}=in.({joined})")
            else:
                params.append(f"{key}=eq.{value}")

    # Order
    if order:
        params.append(f"order={order}")

    # Limit
    if limit:
        params.append(f"limit={limit}")

    full_url = base_url + ("?" + "&".join(params) if params else "")

    response = requests.get(full_url, headers=HEADERS)
    response.raise_for_status()
    return response.json()
