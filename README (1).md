# CSCI316 — Arabic Sentiment Analysis via Transfer Learning

Gulf Arabic code-switched sentiment classification using Jais-7B and XLM-RoBERTa.
3-class prediction: Negative / Neutral / Positive.

---

## Project Structure

| File | Description |
|------|-------------|
| `CSCI316_Keras_Pipeline.ipynb` | Data preprocessing, tokenization & OOV analysis + TF/Keras experiments — XLM-RoBERTa Full FT + LoRA (bonus) |
| `JAIS model.ipynb` | PyTorch + HuggingFace — Jais-7B LoRA + Full FT (primary) |
| `Evaluation.ipynb` | Cultural metric — SauDiSenti Dialect Alignment Score (SDAS) |
| `dashboard/` | Flask app — Docker inference API + web interface |
| `Dockerfile` | Docker container configuration |
| `.dockerignore` | Files excluded from Docker build |
| `requirements.txt` | Python dependencies |
| `data_full_clean.csv` | Cleaned dataset (12,425 samples) |
| `data_train.csv` | Training set (8,697 samples — 70%) |
| `data_val.csv` | Validation set (1,864 samples — 15%) |
| `data_test.csv` | Test set (1,864 samples — 15%) |
| `data_train_tokenized.csv` | Tokenized training data (Jais BPE tokenizer) |
| `finalData.csv` | Labeled dataset (12,477 samples — Groq API labels) |
| `class_weights.json` | Class weights: Neg=1.252, Neu=0.584, Pos=2.038 |
| `keras_fullft_results.csv` | XLM-RoBERTa Full FT results |
| `keras_lora_results.csv` | XLM-RoBERTa LoRA results |
| `Jais_Models (Drive link).pdf` | Google Drive link to Jais models and results (too large to upload) |

---

## Models

### Primary — PyTorch + HuggingFace
- **Jais-7B LoRA** — Best model. Accuracy: 63.36% | Macro F1: 58.98%
- **Jais-7B Full FT** — Accuracy: 56.22% | Macro F1: 25.46%
- Base model: `inceptionai/jais-adapted-7b` (gated — requires HuggingFace token)

### Bonus — TensorFlow / Keras
- **XLM-RoBERTa Full FT** — Accuracy: 60.25% | Macro F1: 57.64%
- **XLM-RoBERTa LoRA** — Accuracy: 58.53% | Macro F1: 41.76%

---

## Setup & Requirements

- Python 3.10+
- Docker Desktop
- HuggingFace account with access to `inceptionai/jais-adapted-7b`

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Running the Notebooks

1. Upload project folder to Google Drive
2. Open notebook in Google Colab
3. Mount Drive and extract zip:
```python
from google.colab import drive
drive.mount('/content/drive')

import zipfile
zipfile.ZipFile('/content/drive/MyDrive/Proj316_files.zip').extractall('/content/')
```
4. For Jais notebooks — HuggingFace login required:
```python
from huggingface_hub import login
login(token="your_hf_token_here")
```

---

## Docker Deployment

Build and run:
```bash
docker build -t csci316-sentiment .
docker run -p 5000:5000 csci316-sentiment
```

Test the API:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "ما تاخدش الحاجة For Granted عشان ما تزولش"}'
```

Expected response:
```json
{"label": "Neutral", "confidence": 0.85}
```

---

## Results Summary

| Model | Strategy | Framework | Accuracy | Macro F1 |
|-------|----------|-----------|----------|----------|
| Jais-7B ⭐ | LoRA | PyTorch + HuggingFace | 63.36% | 58.98% |
| Jais-7B | Full FT | PyTorch + HuggingFace | 56.22% | 25.46% |
| XLM-RoBERTa | Full FT | TensorFlow / Keras | 60.25% | 57.64% |
| XLM-RoBERTa | LoRA | TensorFlow / Keras | 58.53% | 41.76% |

---

## Dataset

- Source: [MagedSaeed/arabic-english-code-switching-text](https://huggingface.co/datasets/MagedSaeed/arabic-english-code-switching-text)
- Labels generated using Groq API (llama-3.1-8b-instant)
- 12,425 samples after cleaning

---

## References

1. Al-Thubaity et al. (2018). SauDiSenti: A Saudi Dialectal Arabic Sentiment Lexicon. LREC 2018.
2. Conneau et al. (2020). Unsupervised Cross-lingual Representation Learning at Scale. ACL 2020.
3. Dettmers et al. (2022). LLM.int8(): 8-bit Matrix Multiplication for Transformers. NeurIPS 2022.
4. Devlin et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers. NAACL-HLT 2019.
5. HuggingFace Inc. (2024). PEFT: State-of-the-art Parameter-Efficient Fine-Tuning. GitHub.
6. Hu et al. (2022). LoRA: Low-Rank Adaptation of Large Language Models. ICLR 2022.
7. Inception AI (2023). JAIS: Arabic-Centric Foundation LLM. arXiv:2308.16149.
8. MagedSaeed (2024). Arabic-English Code-Switching Text Dataset. HuggingFace Datasets. https://huggingface.co/datasets/MagedSaeed/arabic-english-code-switching-text
9. Scikit-learn (2024). compute_class_weight. scikit-learn documentation.

---

## Group — CSCI316 Big Data Mining | 2026
