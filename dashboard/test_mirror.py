import os
import time

# Set Hugging Face mirror to bypass potential network blocks
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

print("Starting download test with mirror...")
start = time.time()
try:
    from transformers import pipeline
    print("Loading pipeline...")
    sentiment_pipeline = pipeline("sentiment-analysis", model="CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment")
    print(f"Successfully loaded in {time.time() - start:.2f} seconds.")
except Exception as e:
    print(f"Error loading: {e}")
