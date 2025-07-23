from fastapi import FastAPI, Request
import numpy as np
import hdbscan

app = FastAPI()

@app.post("/cluster")
async def cluster_embeddings(request: Request):
    data = await request.json()
    
    # Extraer IDs y embeddings
    try:
        ids = [item["id"] for item in data]
        vectors = np.array([item["embedding_5d"] for item in data])
    except Exception as e:
        return {"error": f"Invalid input format: {str(e)}"}
    
    # Ejecutar HDBSCAN
    try:
        clusterer = hdbscan.HDBSCAN(min_cluster_size=5)
        labels = clusterer.fit_predict(vectors)
    except Exception as e:
        return {"error": f"Clustering failed: {str(e)}"}
    
    # Devolver resultado con IDs
    return [
        {"id": id_, "cluster": int(label)}
        for id_, label in zip(ids, labels)
    ]
