import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com/products/product-catalog/?page={}"

def scrape_page(page):
    url = BASE_URL.format(page)
    print(f"Scraping page {page} → {url}")
    
    r = requests.get(url)
    if r.status_code != 200:
        print("Failed:", r.status_code)
        return []
    
    soup = BeautifulSoup(r.text, "html.parser")

    # Product listing container
    items = soup.select(".product-listing-item")
    results = []

    for item in items:
        title_tag = item.select_one(".product-listing-item__title")
        desc_tag = item.select_one(".product-listing-item__description")
        link_tag = item.select_one("a")

        if not link_tag:
            continue

        results.append({
            "name": title_tag.get_text(strip=True) if title_tag else "",
            "url": link_tag.get("href", ""),
            "description": desc_tag.get_text(strip=True) if desc_tag else ""
        })

    return results


def scrape_all():
    all_items = []
    page = 1

    while True:
        page_items = scrape_page(page)

        # stop when no more items left
        if not page_items:
            print("No more items. Stopping.")
            break

        all_items.extend(page_items)
        page += 1
        time.sleep(1)  # polite delay

    # remove duplicates by URL
    seen = set()
    unique_items = []
    for item in all_items:
        if item["url"] not in seen:
            unique_items.append(item)
            seen.add(item["url"])

    print(f"\nTotal scraped items BEFORE dedupe: {len(all_items)}")
    print(f"Total final UNIQUE items: {len(unique_items)}")

    return unique_items


if __name__ == "__main__":
    print("Starting SHL full catalogue scraper...")
    data = scrape_all()
    
    with open("data/assessments_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nSaved → data/assessments_raw.json")
