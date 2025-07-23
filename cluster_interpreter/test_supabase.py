
from services.supabase_client import query_table
from dotenv import load_dotenv
from pathlib import Path
import os

# Cargar el .env desde AGENTE_IA
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

def main():
    cluster_id = "00f10bb8-51fc-4dc9-b94b-0db417e10634"

    try:
        # Consultar tabla assign_meta
        print("🔍 Getting chunk_ids assigned to cluster...")
        assigned = query_table(
            table_name="assign_meta",
            filters={"cluster_id": cluster_id},
            select=["chunk_id", "position"]
        )
        print(f"✅ Found {len(assigned)} assigned chunks.")
        for row in assigned:
            print(row)

    except Exception as e:
        print("❌ ERROR during Supabase query:")
        print(e)

if __name__ == "__main__":
    main()
