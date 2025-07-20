import streamlit as st
import pandas as pd
import numpy as np
import cloudpickle
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io

# === Load model and EMT score distribution from Google Drive ===
@st.cache_resource
def load_model_and_data():
    # Google Drive direct download links
    model_url = "https://drive.google.com/uc?export=download&id=1Z-BoP5x2b13csQU1lJSJAxWt_2ZCi727"
    data_url = "https://drive.google.com/uc?export=download&id=1-rJKiqZAOv71BBwCwkWUKxEbsnlyDYx5"

    # Load model using cloudpickle
    model_bytes = requests.get(model_url).content
    model = cloudpickle.load(io.BytesIO(model_bytes))

    # Load dataset
    data_bytes = requests.get(data_url).content
    df = pd.read_csv(io.BytesIO(data_bytes), index_col=0)
    df = df.drop(index="PC1_weight", errors="ignore")
    emt_scores = df["EMT_score"].astype(float)
    return model, emt_scores

model, emt_scores = load_model_and_data()

# === Define the top 5 genes used in training ===
top_genes = ['FSTL3', 'COL1A1', 'FN1', 'SPARC', 'TIMP1']  # Replace with your actual gene list

st.title("🧬 EMT Score Predictor")
st.markdown("Input expression values for the five EMT-related genes below. These values can be TPM, ΔCt, or other relative units.")

# === Input form ===
gene_inputs = {}
with st.form("emt_form"):
    for gene in top_genes:
        val = st.number_input(f"{gene} expression", step=0.01, format="%.2f")
        gene_inputs[gene] = val
    submitted = st.form_submit_button("Predict EMT Score")

# === On submit ===
if submitted:
    try:
        # Normalize across genes (z-score per sample)
        raw_vals = np.array([gene_inputs[gene] for gene in top_genes])
        z_vals = (raw_vals - raw_vals.mean()) / raw_vals.std()

        # Predict EMT
        emt_pred = model.predict([z_vals])[0]
        st.success(f"Predicted EMT Score: {emt_pred:.3f}")

        # Plot result
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.kdeplot(emt_scores, fill=True, label="Training EMT Score Distribution", color="skyblue", ax=ax)
        ax.axvline(emt_pred, color="red", linestyle="--", label=f"Your Sample: {emt_pred:.2f}")
        ax.set_xlabel("EMT Score")
        ax.set_ylabel("Density")
        ax.set_title("EMT Score Compared to Training Set")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error in prediction: {e}")
