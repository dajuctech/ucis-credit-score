import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

# Paths
PCA_PATH = os.path.join("data", "reduced", "credit_data_pca.csv")
UMAP_PATH = os.path.join("data", "reduced", "credit_data_umap.csv")
LABEL_PATH = os.path.join("data", "processed", "credit_data_cleaned.csv")  # To extract labels if needed

# Load data
df_pca = pd.read_csv(PCA_PATH)
df_umap = pd.read_csv(UMAP_PATH)
df_labels = pd.read_csv(LABEL_PATH)

# Try to extract the target label if available
target_col = None
for col in ['Credit_Score', 'credit_score', 'Target', 'Score']:
    if col in df_labels.columns:
        target_col = col
        break

if target_col:
    labels = df_labels[target_col]
else:
    labels = None
    print("⚠️ No label column found. Plotting without class colors.")

# PCA Scatter Plot
plt.figure(figsize=(8, 6))
if labels is not None:
    sns.scatterplot(x="PCA1", y="PCA2", hue=labels, data=df_pca, palette="viridis")
    plt.legend(title=target_col)
else:
    sns.scatterplot(x="PCA1", y="PCA2", data=df_pca)
plt.title("PCA - 2D Projection")
plt.tight_layout()
plt.savefig("reports/pca_scatter_plot.png")
plt.close()

# UMAP Scatter Plot
plt.figure(figsize=(8, 6))
if labels is not None:
    sns.scatterplot(x="UMAP1", y="UMAP2", hue=labels, data=df_umap, palette="viridis")
    plt.legend(title=target_col)
else:
    sns.scatterplot(x="UMAP1", y="UMAP2", data=df_umap)
plt.title("UMAP - 2D Projection")
plt.tight_layout()
plt.savefig("reports/umap_scatter_plot.png")
plt.close()

print("✅ PCA and UMAP scatter plots saved to reports/")
