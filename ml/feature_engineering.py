import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
INPUT_PATH = os.path.join(ROOT_DIR, "data", "processed", "credit_data_cleaned.csv")
PCA_OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "reduced", "credit_data_pca.csv")
UMAP_OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "reduced", "credit_data_umap.csv")

# Load data
df = pd.read_csv(INPUT_PATH)
print(f"✅ Loaded cleaned data: {df.shape}")

# Drop non-numeric columns (like datetime or object)
numeric_df = df.select_dtypes(include=["int64", "float64"])

# Scale features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(numeric_df)

# Apply PCA
pca = PCA(n_components=2, random_state=42)
pca_result = pca.fit_transform(scaled_features)
df_pca = pd.DataFrame(pca_result, columns=["PCA1", "PCA2"])
df_pca.to_csv(PCA_OUTPUT_PATH, index=False)
print(f"✅ PCA reduced data saved: {PCA_OUTPUT_PATH}")

# Apply UMAP
umap_model = umap.UMAP(n_components=2, random_state=42)
umap_result = umap_model.fit_transform(scaled_features)
df_umap = pd.DataFrame(umap_result, columns=["UMAP1", "UMAP2"])
df_umap.to_csv(UMAP_OUTPUT_PATH, index=False)
print(f"✅ UMAP reduced data saved: {UMAP_OUTPUT_PATH}")
