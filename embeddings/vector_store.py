import numpy as np
import faiss
import pandas as pd

class VectorStore:
    def __init__(self):
        self.emb = np.load("data/embeddings.npy")
        self.meta = pd.read_csv("data/assessments_clean.csv")
        
        self.index = faiss.IndexFlatIP(self.emb.shape[1])
        faiss.normalize_L2(self.emb)
        self.index.add(self.emb.astype("float32"))

    def search(self, query_vec, k=10):
        import numpy as np
        q = np.array([query_vec]).astype("float32")
        faiss.normalize_L2(q)
        scores, idxs = self.index.search(q, k)

        results = []
        for i, s in zip(idxs[0], scores[0]):
            row = self.meta.iloc[i].to_dict()
            row["score"] = float(s)
            results.append(row)

        return results
