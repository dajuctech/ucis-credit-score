import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# ========== Paths ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "credit_data_cleaned.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

# ========== Load Data ==========
df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded dataset: {df.shape}")

# ========== Reconstruct Target ==========
if all(col in df.columns for col in ['Credit_Score_Poor', 'Credit_Score_Standard']):
    def reconstruct_target(row):
        if row['Credit_Score_Poor'] == 1:
            return 'Poor'
        elif row['Credit_Score_Standard'] == 1:
            return 'Standard'
        else:
            return 'Good'
    y = df.apply(reconstruct_target, axis=1)
    
    # Drop label columns and keep only numeric features
    X = df.drop(columns=['Credit_Score_Poor', 'Credit_Score_Standard'])
    X = X.select_dtypes(include=["number"])  # Remove any datetime/object fields
else:
    raise ValueError("❌ Cannot reconstruct target from one-hot columns.")

# ========== Split Data ==========
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

print("✅ Data split: train={}, val={}, test={}".format(len(y_train), len(y_val), len(y_test)))

# ========== Define Models ==========
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    # Uncomment below to include other models
    # "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    # "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42),
    # "SVM": SVC(kernel='rbf', probability=True)
}

# ========== Train & Evaluate ==========
best_model = None
best_score = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    val_preds = model.predict(X_val)
    score = accuracy_score(y_val, val_preds)
    print(f"\n🔍 {name} Validation Accuracy: {score:.4f}")
    print(classification_report(y_val, val_preds))

    if score > best_score:
        best_model = model
        best_score = score
        best_model_name = name

# ========== Save Best Model ==========
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
joblib.dump(best_model, MODEL_PATH)
print(f"\n✅ Best model '{best_model_name}' saved to: {MODEL_PATH}")
