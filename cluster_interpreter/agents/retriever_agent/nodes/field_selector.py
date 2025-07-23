import os
import json
import traceback
from pathlib import Path
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv


def _load_env() -> str:
    env_path = Path(__file__).resolve().parents[4] / ".env"
    if not env_path.exists():
        raise FileNotFoundError(f"❌ .env not found at {env_path}")
    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.startswith("sk-"):
        raise ValueError("❌ OPENAI_API_KEY is missing or invalid in .env")
    return api_key


def _load_prompt_template() -> str:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "retriever_prompt.txt"
    with open(prompt_path, encoding="utf-8") as f:
        return f.read()


def _format_prompt(template: str, agent_goal: str, schema_summary: dict) -> str:
    return template.replace("<AGENT_GOAL>", agent_goal).replace(
        "<SCHEMA_SUMMARY>", json.dumps(schema_summary, indent=2)
    )


def _call_openai(prompt: str) -> dict:
    try:
        print("🤖 Llamando a OpenAI...")
        client = OpenAI(api_key=_load_env())
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        print("🧠 Respuesta LLM:\n", content)

        cleaned = content.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)

    except Exception as e:
        print("❌ Error durante la llamada o el parseo de la respuesta:")
        traceback.print_exc()
        raise RuntimeError("Fallo en _call_openai")


def _convert_to_table_field_dict(fields_used: list, justification: dict) -> Dict[str, Dict[str, str]]:
    result = {}
    for full_field in fields_used:
        try:
            table, field = full_field.split(".")
            result.setdefault(table, {})[field] = justification.get(full_field, "No justification provided.")
        except ValueError:
            continue
    return result


def filter_schema_by_coverage(schema_summary: dict, field_coverage: dict, threshold: float = 0.3) -> dict:
    filtered = {}
    for table, table_data in schema_summary.items():
        valid_fields = {
            field: meta
            for field, meta in table_data.get("fields", {}).items()
            if field_coverage.get(f"{table}.{field}", 0) >= threshold
        }
        if valid_fields:
            filtered[table] = {
                "description": table_data.get("description", ""),
                "fields": valid_fields
            }
    return filtered


def select_fields_for_goal(agent_goal: str, schema_summary: dict, field_coverage: dict) -> Dict[str, Dict[str, str]]:
    template = _load_prompt_template()
    schema_filtered = filter_schema_by_coverage(schema_summary, field_coverage)
    prompt = _format_prompt(template, agent_goal, schema_filtered)
    llm_output = _call_openai(prompt)
    return _convert_to_table_field_dict(llm_output["fields_used"], llm_output["justification"])


# ----------------- TEST LOCAL --------------------

if __name__ == "__main__":
    print("🚀 Iniciando test local de field_selector.py")

    try:
        TEST_SCHEMA_PATH = Path(__file__).resolve().parents[3] / "data" / "schema_definitions.json"
        TEST_COVERAGE_PATH = Path(__file__).resolve().parents[3] / "data" / "mock_field_coverage.json"

        print("📂 Cargando schema...")
        with open(TEST_SCHEMA_PATH, encoding="utf-8") as f:
            schema_summary = json.load(f)

        print("📂 Cargando coverage mock...")
        with open(TEST_COVERAGE_PATH, encoding="utf-8") as f:
            field_coverage = json.load(f)

        goal = "Preparar los datos necesarios para que otro agente genere un resumen temático del clúster. El resumen debe basarse en el contenido real de los textos (input_chunk.content), complementado si es útil con embeddings, metadatos o relaciones del cluster. Solo se deben seleccionar campos accesibles desde los chunk_id asignados al clúster actual."
        print("🎯 Analizando goal:", goal)

        selected_fields = select_fields_for_goal(goal, schema_summary, field_coverage)

        print("\n✅ Campos seleccionados por tabla:")
        for table, fields in selected_fields.items():
            print(f"📂 {table}")
            for field, reason in fields.items():
                print(f"  - {field:20} → {reason}")

    except Exception:
        print("❌ ERROR GENERAL en el bloque de test:")
        traceback.print_exc()
