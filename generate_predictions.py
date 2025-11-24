import requests
import csv
import json

API_URL = "http://127.0.0.1:9000/recommend"

# Load recall queries
with open("recall_queries.json", "r") as f:
    queries = json.load(f)

rows = []

print("Generating predictions...")

for qid, text in queries.items():
    response = requests.post(API_URL, json={"query": text})

    if response.status_code != 200:
        print(f"Error calling API for {qid}")
        continue

    data = response.json()

    # Extract URLs only
    urls = [item["assessment_url"] for item in data["recommendations"]]

    # Join top-10 URLs
    row = [qid, ",".join(urls[:10])]
    rows.append(row)

# Save into CSV
with open("predictions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["query_id", "assessment_urls"])
    writer.writerows(rows)

print("predictions.csv generated successfully!")
