import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

# ========== Paths ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
PCA_PATH = os.path.join(ROOT_DIR, "data", "reduced", "credit_data_pca.csv")
UMAP_PATH = os.path.join(ROOT_DIR, "data", "reduced", "credit_data_umap.csv")
REPORT_PATH = os.path.join(ROOT_DIR, "reports", "cluster_summary.json")
DENDROGRAM_PATH = os.path.join(ROOT_DIR, "reports", "dendrogram.png")

# ========== Load Reduced Data ==========
df_pca = pd.read_csv(PCA_PATH)
df_umap = pd.read_csv(UMAP_PATH)
print(f"✅ PCA shape: {df_pca.shape}, UMAP shape: {df_umap.shape}")

# ========== Clustering Summary ==========
summary = {}

# ========== KMeans Clustering ==========
def run_kmeans(data, label):
    inertia_scores = []
    silhouette_scores = []
    for k in range(2, 6):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(data)
        inertia_scores.append(km.inertia_)
        sil_score = silhouette_score(data, labels)
        silhouette_scores.append(sil_score)
        print(f"{label} - KMeans (k={k}): Silhouette = {sil_score:.4f}")

    # Choose best k by highest silhouette
    best_k = 2 + silhouette_scores.index(max(silhouette_scores))
    best_model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    best_labels = best_model.fit_predict(data)

    summary[f"{label}_KMeans"] = {
        "best_k": best_k,
        "silhouette_score": max(silhouette_scores)
    }

    return best_labels

# ========== Hierarchical Clustering ==========
def run_hierarchical(data, label):
    # Subsample for scalability
    if len(data) > 2000:
        print(f"⚠️ Subsampling {label} data from {len(data)} to 2000 for hierarchical clustering...")
        data = data.sample(n=2000, random_state=42).reset_index(drop=True)

    # Dendrogram
    linkage_matrix = linkage(data, method='ward')
    plt.figure(figsize=(10, 4))
    dendrogram(linkage_matrix, truncate_mode="lastp", p=20, leaf_rotation=45., leaf_font_size=10.)
    plt.title(f"{label} - Dendrogram")
    plt.tight_layout()
    plt.savefig(DENDROGRAM_PATH)
    plt.close()
    print(f"📈 Dendrogram saved to: {DENDROGRAM_PATH}")

    # Clustering
    model = AgglomerativeClustering(n_clusters=3)
    labels = model.fit_predict(data)
    sil_score = silhouette_score(data, labels)

    summary[f"{label}_Hierarchical"] = {
        "n_clusters": 3,
        "silhouette_score": sil_score
    }

    print(f"{label} - Hierarchical: Silhouette = {sil_score:.4f}")
    return labels

# ========== Run Clustering ==========
run_kmeans(df_pca, "PCA")
run_kmeans(df_umap, "UMAP")
run_hierarchical(df_pca, "PCA")
run_hierarchical(df_umap, "UMAP")

# ========== Save Summary ==========
with open(REPORT_PATH, "w") as f:
    json.dump(summary, f, indent=4)
print(f"\n📄 Cluster summary saved to: {REPORT_PATH}")
