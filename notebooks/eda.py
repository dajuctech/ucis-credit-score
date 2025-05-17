import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
DATA_PATH = os.path.join("data", "processed", "credit_data_cleaned.csv")
df = pd.read_csv(DATA_PATH)

# Set style
sns.set(style="whitegrid")

# 1. Dataset shape & types
print("🔍 Shape:", df.shape)
print("\n🔍 Data types:\n", df.dtypes.value_counts())
print("\n🔍 Sample data:\n", df.head())

# 2. Missing values heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title("Missing Values Heatmap")
plt.tight_layout()
plt.savefig("reports/eda_missing_heatmap.png")
plt.close()

# 3. Class distribution
# Try to find a column representing the target
possible_targets = ['Credit_Score', 'credit_score', 'Target', 'Score']
TARGET_COL = next((col for col in possible_targets if col in df.columns), None)

if TARGET_COL:
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x=TARGET_COL)
    plt.title(f"Distribution of {TARGET_COL}")
    plt.tight_layout()
    plt.savefig("reports/eda_class_distribution.png")
    plt.close()
    print(f"✅ Class distribution plot created for '{TARGET_COL}'")
else:
    print("⚠️ No known target column found. Skipping class distribution plot.")

# 4. Correlation heatmap (numerical features only)
plt.figure(figsize=(16, 12))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, cmap="coolwarm", annot=False, fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("reports/eda_correlation_heatmap.png")
plt.close()

# 5. Histograms of numerical features
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[num_cols].hist(figsize=(16, 12), bins=30)
plt.tight_layout()
plt.savefig("reports/eda_histograms.png")
plt.close()

print("✅ EDA completed. Charts saved in /reports/")
