# Arabic Sentiment Analysis via Transfer Learning

Classifies Gulf Arabic and Arabic-English code-switched text into negative, neutral, or positive sentiment. Experiments compare Jais-7B LoRA/full fine-tuning with XLM-RoBERTa TensorFlow/Keras experiments; includes preprocessing, token/OOV analysis, evaluation, and a Flask dashboard.

## Results (reported)

| Model | Strategy | Accuracy | Macro F1 |
|---|---|---:|---:|
| Jais-7B | LoRA | 63.36% | 58.98% |
| Jais-7B | Full fine-tune | 56.22% | 25.46% |
| XLM-RoBERTa | Full fine-tune | 60.25% | 57.64% |
| XLM-RoBERTa | LoRA | 58.53% | 41.76% |

Numbers are reported project results and have not been independently reproduced. Dashboard currently uses a lightweight rule-based demo, not the trained checkpoint.

## Setup

Python 3.10+. Install dashboard dependencies with `pip install -r dashboard/requirements.txt`. Notebooks target Google Colab and require separate ML dependencies/GPU. For gated Jais access set `HF_TOKEN` in the environment; never paste credentials into notebooks.

Run dashboard: `python dashboard/app.py`; open `http://localhost:5000`. API: `POST /api/predict` with JSON `{"text":"..."}`.

Dataset source: [Arabic-English Code-Switching Text](https://huggingface.co/datasets/MagedSaeed/arabic-english-code-switching-text). Check dataset lineage/terms before redistribution.
