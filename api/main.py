from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from embeddings.vector_store import VectorStore
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load vector store
store = VectorStore()

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(q: Query):
    q_vec = model.encode([q.query])[0]
    results = store.search(q_vec, k=10)
    
    return {
        "query": q.query,
        "recommendations": [
            {
                "assessment_name": r["name"],
                "assessment_url": r["url"],
                "score": r["score"]
            }
            for r in results
        ]
    }
