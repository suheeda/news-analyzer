from data_ingest import fetch_and_store

TOPIC = "technology"
PAGE_SIZE = 5    # fetch fewer articles for speed
PAGES = 1        # only 1 page for quick update

fetch_and_store(TOPIC, PAGE_SIZE, PAGES)
print("Pipeline completed successfully!")
