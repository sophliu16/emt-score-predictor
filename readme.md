# 🧬 EMT Score Predictor

A lightweight, browser-based tool to predict EMT score based on 5 EMT-related genes.  
Intended for research or clinical pilot use.

## 🚀 How to Use (Streamlit Cloud)

1. Upload 5 gene expression values from a biopsy (e.g. ΔCt or TPM).
2. The app normalizes the sample internally.
3. You get a predicted EMT score and see how it compares to a reference population.

## 🗂 Files Included

- `emt_predictor_app.py`: Streamlit app script
- `trained_rf_model.pkl`: Pretrained model file
- `full_cells_with_emt_score_and_gmm.csv`: Distribution reference
- `requirements.txt`: Dependencies for Streamlit Cloud

## 📦 Deployment

Deploy using [Streamlit Cloud](https://streamlit.io/cloud). Just point it to this repository and it will run automatically.
