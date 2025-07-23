from fastapi import FastAPI, Request
import numpy as np
import hdbscan

app = FastAPI()

@app.post("/multi-cluster")
async def multi_cluster(request: Request):
    data = await request.json()

    # Extraer IDs y vectores
    try:
        ids = [item["id"] for item in data]
        vectors = np.array([item["embedding"] for item in data])
    except Exception as e:
        return {"error": f"Invalid input format: {str(e)}"}

    # Primer clustering
    try:
        level1 = hdbscan.HDBSCAN(min_cluster_size=5)
        labels_lvl1 = level1.fit_predict(vectors)
    except Exception as e:
        return {"error": f"Level 1 clustering failed: {str(e)}"}

    # Armar resultados de primer nivel
    results = []
    for i, label1 in enumerate(labels_lvl1):
        results.append({
            "id": ids[i],
            "embedding": vectors[i].tolist(),
            "cluster_level_1": int(label1),
        })

    # Segundo clustering: por cada cluster de nivel 1
    final_results = []
    for cluster_id in set(labels_lvl1):
        cluster_items = [r for r in results if r["cluster_level_1"] == cluster_id]

        if len(cluster_items) < 5:
            # Demasiado pequeño para sub-clustering
            for item in cluster_items:
                item["cluster_level_2"] = -1
                final_results.append(item)
            continue

        try:
            sub_vectors = np.array([item["embedding"] for item in cluster_items])
            level2 = hdbscan.HDBSCAN(min_cluster_size=3)
            labels_lvl2 = level2.fit_predict(sub_vectors)
        except Exception as e:
            return {"error": f"Level 2 clustering failed for cluster {cluster_id}: {str(e)}"}

        for item, sub_label in zip(cluster_items, labels_lvl2):
            item["cluster_level_2"] = int(sub_label)
            final_results.append(item)

    # Quitar embeddings si no los necesitas en el output final
    for item in final_results:
        del item["embedding"]

    return final_results
