from pathlib import Path
import json
from typing import Dict, List
from cluster_interpreter.services.supabase_client import query_table

def _load_schema_fields() -> Dict[str, List[str]]:
    base_path = Path(__file__).resolve().parents[3] / "data" / "schema_definitions.json"
    with open(base_path, encoding="utf-8") as f:
        schema = json.load(f)

    field_map = {}
    for table, meta in schema.items():
        fields = list(meta.get("fields", {}).keys())
        field_map[table] = fields
    return field_map

def _get_chunk_ids(cluster_id: str) -> List[int]:
    rows = query_table("assign_meta", filters={"cluster_id": cluster_id}, select=["chunk_id"])
    return [int(row["chunk_id"]) for row in rows if "chunk_id" in row]

def compute_field_coverage(cluster_id: str) -> Dict[str, float]:
    chunk_ids = _get_chunk_ids(cluster_id)
    if not chunk_ids:
        return {}

    field_map = _load_schema_fields()
    coverage = {}
    raw_ids_cache = None
    cluster_ids_cache = None

    for table, fields in field_map.items():
        for field in fields:
            full_key = f"{table}.{field}"

            try:
                if table in ["input_chunk", "assign_meta", "input_fact"]:
                    data = query_table(table, filters={"chunk_id": chunk_ids}, select=[field])

                elif table == "input_raw":
                    if raw_ids_cache is None:
                        raw_rows = query_table("input_chunk", filters={"chunk_id": chunk_ids}, select=["raw_id"])
                        raw_ids_cache = [r["raw_id"] for r in raw_rows if r.get("raw_id")]
                    data = query_table(table, filters={"id": raw_ids_cache}, select=[field])

                elif table == "cluster_meta":
                    if cluster_ids_cache is None:
                        cluster_rows = query_table("assign_meta", filters={"chunk_id": chunk_ids}, select=["cluster_id"])
                        cluster_ids_cache = list({r["cluster_id"] for r in cluster_rows if r.get("cluster_id")})
                    data = query_table(table, filters={"cluster_id": cluster_ids_cache}, select=[field])

                else:
                    data = []

                total = max(1, len(data))
                non_empty = [row.get(field) for row in data if row.get(field) not in [None, "", [], {}]]
                coverage[full_key] = len(non_empty) / total

            except Exception as e:
                coverage[full_key] = -1.0

    return coverage

# ----------------- TEST LOCAL --------------------

if __name__ == "__main__":
    test_cluster_id = "00f10bb8-51fc-4dc9-b94b-0db417e10634"
    print("📊 Calculando coverage para cluster:", test_cluster_id)
    result = compute_field_coverage(test_cluster_id)

    print("\n✅ Cobertura por campo (relativa a filas válidas accedidas):")
    for field, score in sorted(result.items()):
        print(f" - {field:30} → {score:.2f}")