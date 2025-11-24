import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Load dataset
with open("data/assessments_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

df = pd.DataFrame(items)

# Combine fields to embed
df["text"] = df["name"].fillna("") + ". " + df["description"].fillna("")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

# Save results
np.save("data/embeddings.npy", embeddings)
df.to_csv("data/assessments_clean.csv", index=False)

print("Embeddings saved successfully!")
