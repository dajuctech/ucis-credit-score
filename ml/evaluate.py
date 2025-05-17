import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split

# ========== Paths ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "credit_data_cleaned.csv")
REPORT_CSV = os.path.join(ROOT_DIR, "reports", "model_comparison.csv")
CONF_MATRIX_IMG = os.path.join(ROOT_DIR, "reports", "confusion_matrix.png")
ROC_CURVE_IMG = os.path.join(ROOT_DIR, "reports", "roc_curve.png")

# ========== Load Model & Data ==========
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# ========== Prepare Data ==========
# Reconstruct target
if all(col in df.columns for col in ['Credit_Score_Poor', 'Credit_Score_Standard']):
    def reconstruct_target(row):
        if row['Credit_Score_Poor'] == 1:
            return 'Poor'
        elif row['Credit_Score_Standard'] == 1:
            return 'Standard'
        else:
            return 'Good'
    y = df.apply(reconstruct_target, axis=1)
    X = df.drop(columns=['Credit_Score_Poor', 'Credit_Score_Standard'])
    X = X.select_dtypes(include=["number"])
else:
    raise ValueError("❌ Could not reconstruct target labels.")

# ========== Test Split Only ==========
_, X_temp, _, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

# ========== Predictions ==========
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)

# ========== Metrics ==========
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

# Binarize target for ROC AUC
y_test_bin = label_binarize(y_test, classes=["Poor", "Standard", "Good"])
auc_score = roc_auc_score(y_test_bin, y_proba, average="macro", multi_class="ovr")

print(f"✅ Accuracy: {accuracy:.4f}")
print(f"✅ F1 Score: {f1:.4f}")
print(f"✅ AUC Score: {auc_score:.4f}")

# ========== Save to CSV ==========
results = pd.DataFrame([{
    "Model": type(model).__name__,
    "Accuracy": accuracy,
    "F1_Score": f1,
    "AUC": auc_score
}])
results.to_csv(REPORT_CSV, index=False)
print(f"📄 Evaluation report saved to: {REPORT_CSV}")

# ========== Confusion Matrix ==========
cm = confusion_matrix(y_test, y_pred, labels=["Poor", "Standard", "Good"])
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Poor", "Standard", "Good"], yticklabels=["Poor", "Standard", "Good"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig(CONF_MATRIX_IMG)
plt.close()
print(f"🖼️ Confusion matrix saved to: {CONF_MATRIX_IMG}")

# ========== ROC Curve ==========
fpr = dict()
tpr = dict()
roc_auc = dict()
n_classes = y_test_bin.shape[1]

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

plt.figure(figsize=(8, 6))
for i, label in enumerate(["Poor", "Standard", "Good"]):
    plt.plot(fpr[i], tpr[i], label=f"{label} (AUC = {roc_auc[i]:.2f})")

plt.plot([0, 1], [0, 1], 'k--')
plt.title("ROC Curve")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.tight_layout()
plt.savefig(ROC_CURVE_IMG)
plt.close()
print(f"🖼️ ROC curve saved to: {ROC_CURVE_IMG}")
