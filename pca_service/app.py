from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sklearn.decomposition import PCA
import numpy as np

app = FastAPI()

class EmbeddingItem(BaseModel):
    id: int
    embedding: List[float]

@app.post("/reduce")
def reduce_embeddings(data: List[EmbeddingItem]):
    ids = [item.id for item in data]
    vectors = np.array([item.embedding for item in data])

    if len(vectors) < 5:
        return {"error": "Need at least 5 dimensions to reduce to 5D"}

    pca = PCA(n_components=5)
    reduced = pca.fit_transform(vectors)

    return [
        {"id": id_, "embedding_5d": reduced[i].tolist()}
        for i, id_ in enumerate(ids)
    ]
