import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load data for EDA
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data_full_clean.csv")
df = None
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

# Instead of downloading a 400MB Hugging Face model which is blocked on the network,
# we use a lightweight rule-based Arabic sentiment analyzer for the dashboard demo.
class SimpleArabicSentiment:
    def __init__(self):
        self.positive_words = ['سعيد', 'ممتاز', 'رائع', 'جميل', 'جيد', 'حب', 'فرح', 'نجاح', 'عظيم', 'مذهل', 'شكر', 'أفضل', 'خير']
        self.negative_words = ['حزين', 'سيء', 'قبيح', 'ضعيف', 'كره', 'غضب', 'فشل', 'فظيع', 'مشكلة', 'خطأ', 'أسوأ', 'شر', 'غبي']
        
    def __call__(self, text):
        pos_count = sum(1 for word in self.positive_words if word in text)
        neg_count = sum(1 for word in self.negative_words if word in text)
        
        if pos_count > neg_count:
            return [{'label': 'Positive', 'score': 0.75 + (pos_count * 0.05)}]
        elif neg_count > pos_count:
            return [{'label': 'Negative', 'score': 0.75 + (neg_count * 0.05)}]
        else:
            return [{'label': 'Neutral', 'score': 0.85}]

sentiment_pipeline = SimpleArabicSentiment()

def get_sentiment_pipeline():
    return sentiment_pipeline

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    if df is None:
        return jsonify({"error": "Data file not found"}), 404
        
    # Example stats: Label distribution
    # The clean data has Negative=0, Neutral=1, Positive=2, but also 'Sentiment' column
    if 'Sentiment' in df.columns:
        counts = df['Sentiment'].value_counts().to_dict()
    else:
        counts = {
            "Negative": int((df['label'] == 0).sum()),
            "Neutral": int((df['label'] == 1).sum()),
            "Positive": int((df['label'] == 2).sum())
        }
        
    total_samples = len(df)
    
    return jsonify({
        "labelDistribution": counts,
        "totalSamples": total_samples
    })

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
        
    text = data["text"]
    
    if not get_sentiment_pipeline():
        # Fallback if model failed to load
        return jsonify({"sentiment": "Model Unavailable", "score": 0.0})
        
    try:
        # returns [{'label': 'positive', 'score': 0.99}]
        result = get_sentiment_pipeline()(text)[0]
        label = result['label'].capitalize()
        score = float(result['score'])
        return jsonify({"sentiment": label, "score": score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
