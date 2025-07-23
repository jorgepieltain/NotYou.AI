from fastapi import FastAPI, Request
import numpy as np
import umap

app = FastAPI()

@app.post("/umap")
async def reduce_embeddings(request: Request):
    try:
        data = await request.json()
        ids = [item["id"] for item in data]
        vectors = np.array([item["embedding"] for item in data])
    except Exception as e:
        return {"error": f"Invalid input format: {str(e)}"}

    try:
        reducer = umap.UMAP(n_components=15, random_state=42)
        reduced = reducer.fit_transform(vectors)
    except Exception as e:
        return {"error": f"UMAP reduction failed: {str(e)}"}

    return [
        {"id": id_, "embedding_umap15": vec.tolist()}
        for id_, vec in zip(ids, reduced)
    ]

