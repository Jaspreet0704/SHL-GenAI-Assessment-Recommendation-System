This project is built as part of the SHL AI Intern Hiring – Nov 2025 assignment.
It implements a content-based recommendation engine using generative embeddings to match job descriptions with the most relevant SHL assessments.

The system includes:
-Web Scraper (or uploaded dataset alternative)
-Data Cleaning & Preprocessing
-Embedding Generation using OpenAI
-Similarity Search using FAISS / NumPy
-FastAPI backend for recommendations
-Simple HTML frontend for real-time queries
-Evaluation scripts 
-Full submission files required by SHL



How the Recommendation Engine Works

1. Dataset Preparation
Assessments scraped / collected from SHL product catalog
Cleaned titles + descriptions 
Saved as assessments_clean.csv

2. Embedding Generation
OpenAI text-embedding-3-small used
Saved as embeddings.npy

3. Similarity Search
Compute cosine similarity between job query and all assessments
Return highest-matching assessments with URLs

4. API Serving
FastAPI endpoint /recommend returns structured JSON predictions

5. Frontend Integration
JS fetch call sends query → displays ranked assessments
