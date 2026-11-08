import time
print("Starting download test...")
start = time.time()
try:
    from transformers import pipeline
    print("Loading pipeline...")
    sentiment_pipeline = pipeline("sentiment-analysis", model="CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment")
    print(f"Successfully loaded in {time.time() - start:.2f} seconds.")
except Exception as e:
    print(f"Error loading: {e}")
