from services.schema_loader import SchemaManager
from services.supabase_client import SupabaseClient
import openai
import os

schema_path = "cluster_interpreter/data/schema_definitions.json"
schema = SchemaManager(schema_path)
supabase = SupabaseClient()
openai.api_key = os.getenv("OPENAI_API_KEY")


def build_prompt(goal: str) -> str:
    schema_context = schema.get_prompt_description()
    return f"""
You are a data reasoning agent.
Your task is to decide which fields from a Supabase database schema are relevant to fulfill this goal:

GOAL: \"{goal}\"

The schema is:
{schema_context}

Return a JSON with:
- fields_used: dictionary of fully qualified fields (e.g., 'assign_meta.position') and a short justification for each.
- target_tables: list of table names needed to retrieve data for this goal.

Only include fields that are semantically useful for answering the goal. Be concise.
"""


def call_field_selector_llm(goal: str) -> dict:
    prompt = build_prompt(goal)
    response = openai.ChatCompletion.create(
        model="gpt-4",  # puedes cambiar por gpt-3.5-turbo si quieres ahorrar
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return eval(response.choices[0].message.content)  # Asegúrate de que el output es seguro


def retrieve_data(goal: str, cluster_id: str) -> dict:
    reasoning = call_field_selector_llm(goal)
    target_tables = reasoning.get("target_tables", [])
    fields_used = reasoning.get("fields_used", {})
    data = {}

    for table in target_tables:
        rows = supabase.select_where(table, {"cluster_id": cluster_id})
        data[table] = rows

    return {
        "cluster_id": cluster_id,
        "fields_used": fields_used,
        "data": data
    }


# Ejemplo de uso
if __name__ == "__main__":
    goal = "Generate a precise summary of the cluster using the most central and validated chunks."
    cluster_id = "123e4567-e89b-12d3-a456-426614174000"
    result = retrieve_data(goal, cluster_id)
    print(result)
