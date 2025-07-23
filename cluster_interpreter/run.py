from agents.retriever_agent import retrieve_data

# 👇 Cambia por un cluster_id real si lo tienes
goal = "Generate a precise summary of the cluster using the most central and validated chunks."
cluster_id = "1f3ac050-2e32-4b1b-9286-01dbbcf8362e"

if __name__ == "__main__":
    result = retrieve_data(goal, cluster_id)
    print("\n🔍 FIELDS USED:")
    for k, v in result["fields_used"].items():
        print(f"  {k}: {v}")

    print("\n📦 DATA RETRIEVED:")
    for table, rows in result["data"].items():
        print(f"\n🗂️ {table}: {len(rows)} rows")
        for row in rows[:3]:  # preview primeros 3
            print(row)
