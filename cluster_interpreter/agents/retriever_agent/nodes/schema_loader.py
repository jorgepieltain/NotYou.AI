from pathlib import Path
import json
from typing import Dict, Any

def load_schema_data() -> Dict[str, Any]:
    """
    Carga el esquema de tablas y las relaciones desde la carpeta /data/.
    Devuelve un diccionario con 'schema_summary' y 'schema_links'.
    """
    try:
        # Ruta base: .../cluster_interpreter/data/
        base_path = Path(__file__).resolve().parents[3] / "data"
        schema_path = base_path / "schema_definitions.json"
        links_path = base_path / "schema_links.json"

        # Cargar schema
        with open(schema_path, encoding="utf-8") as f:
            schema_summary = json.load(f)

        # Cargar relaciones entre tablas
        with open(links_path, encoding="utf-8") as f:
            schema_links = json.load(f)

        return {
            "schema_summary": schema_summary,
            "schema_links": schema_links
        }

    except Exception as e:
        raise RuntimeError(f"❌ Error loading schema or links: {e}")

# -------------------- TEST LOCAL --------------------

if __name__ == "__main__":
    print("📦 Cargando schema...")
    result = load_schema_data()

    print("\n✅ Claves devueltas:", list(result.keys()))

    print("\n📊 Tablas encontradas en el schema:")
    for table in result["schema_summary"].keys():
        print(f" - {table}")

    print("\n🔗 Relaciones entre tablas (schema_links):")
    links = result["schema_links"]

    for from_table, meta in links.items():
        links_to = meta.get("links_to", {})
        for to_table, link_info in links_to.items():
            via = link_info.get("via", "N/A")
            rel_type = link_info.get("type", "N/A")
            desc = link_info.get("description", "")
            print(f" - {from_table} → {to_table}  | via: {via}  | type: {rel_type}")
            if desc:
                print(f"   📝 {desc}")