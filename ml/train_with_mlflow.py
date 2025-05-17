import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, classification_report

# ========== Paths ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "credit_data_cleaned.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

# ========== Load & Prepare Data ==========
df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded dataset: {df.shape}")

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
    raise ValueError("❌ Cannot reconstruct target from one-hot columns.")

# Split data
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)
print(f"✅ Split: train={len(y_train)}, val={len(y_val)}, test={len(y_test)}")

# ========== Define Models ==========
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000)
    #"RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    #"XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42),
    #"SVM": SVC(kernel='rbf', probability=True)
}

# ========== MLflow Setup ==========
mlflow.set_experiment("Credit_Score_Classification")
best_model = None
best_score = 0
best_model_name = ""

# ========== Train & Log ==========
for name, model in models.items():
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        val_preds = model.predict(X_val)
        acc = accuracy_score(y_val, val_preds)
        f1 = f1_score(y_val, val_preds, average='weighted')

        mlflow.log_param("model", name)
        mlflow.log_metric("val_accuracy", acc)
        mlflow.log_metric("val_f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        print(f"\n🔍 {name} Accuracy: {acc:.4f} | F1: {f1:.4f}")
        print(classification_report(y_val, val_preds))

        if acc > best_score:
            best_score = acc
            best_model = model
            best_model_name = name

# ========== Save Best Model Locally ==========
joblib.dump(best_model, MODEL_PATH)
print(f"\n✅ Best model '{best_model_name}' saved to: {MODEL_PATH}")
