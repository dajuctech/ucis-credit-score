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

# Attempt to reconstruct 'Credit_Score' from one-hot encoded columns
if all(col in df_labels.columns for col in ['Credit_Score_Poor', 'Credit_Score_Standard']):
    def reconstruct_credit_score(row):
        if row['Credit_Score_Poor'] == 1:
            return 'Poor'
        elif row['Credit_Score_Standard'] == 1:
            return 'Standard'
        else:
            return 'Good'  # One-hot dropped column (drop_first=True)
    
    labels = df_labels.apply(reconstruct_credit_score, axis=1)
    target_col = 'Credit_Score'
    print("✅ Reconstructed 'Credit_Score' from one-hot columns.")
else:
    labels = None
    target_col = None
    print("⚠️ Could not reconstruct 'Credit_Score'. Plotting without class colors.")

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
