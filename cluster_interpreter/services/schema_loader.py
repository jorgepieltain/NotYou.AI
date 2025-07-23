import json
from pathlib import Path

class SchemaManager:
    def __init__(self, schema_path: str):
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self._generate_prompt_descriptions()

    def _load_schema(self) -> dict:
        with self.schema_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _generate_prompt_descriptions(self):
        for table_name, table_info in self.schema.items():
            lines = [f"Table: {table_name}", f"{table_info.get('description', '')}"]
            for field_name, field_info in table_info.get("fields", {}).items():
                lines.append(f"- {field_name} ({field_info.get('type', 'unknown')}): {field_info.get('description', '')}")
            table_info["prompt_description"] = "\n".join(lines)

    def get_all_tables(self) -> list:
        return list(self.schema.keys())

    def get_table(self, table_name: str) -> dict:
        return self.schema.get(table_name, {})

    def get_field_description(self, table_name: str, field_name: str) -> str:
        return self.schema.get(table_name, {}).get("fields", {}).get(field_name, {}).get("description", "")

    def get_prompt_description(self, tables: list[str] = None) -> str:
        if tables is None:
            return "\n\n".join([tbl["prompt_description"] for tbl in self.schema.values()])
        return "\n\n".join([self.schema[table]["prompt_description"] for table in tables if table in self.schema])


# Ejemplo de uso
if __name__ == "__main__":
    manager = SchemaManager("cluster_interpreter/data/schema_definitions.json")
    print(manager.get_prompt_description())
