# 📈 Business Insights Report

## 1. Dataset Overview
- **Total Records:** 100,000
- **Features Used:** 18 numeric and categorical variables
- **Target Variable:** Credit_Score (Good, Standard, Poor)

## 2. Key Insights from EDA
- Customers with higher **Credit Utilization Ratio** tend to have poorer credit scores.
- The **Occupation** and **Payment Behavior** features significantly correlate with creditworthiness.
- Missing values were found mostly in payment history and were handled using imputation.

## 3. Modeling Results
| Model               | Accuracy | F1 Score | AUC |
|--------------------|----------|----------|-----|
| Logistic Regression| 74.2%    | 0.71     | 0.78|
| XGBoost            | 82.5%    | 0.80     | 0.86|
| Random Forest      | 81.7%    | 0.79     | 0.84|

✅ **Best Model:** XGBoost (Saved as `ml/models/model.pkl`)

## 4. Clustering Analysis
- Using UMAP + KMeans, customers were grouped into 3 main segments.
- Cluster 1: Low risk, high income
- Cluster 2: High risk, many delayed payments
- Cluster 3: Medium risk, moderate income, stable behavior

## 5. Business Recommendations
- Target Cluster 1 for premium card upselling.
- Offer credit counseling or budgeting support to Cluster 2.
- Monitor Cluster 3 for early signs of risk drift.

## 6. Next Steps
- Deploy dashboard for real-time credit predictions.
- Integrate alerts for users trending toward high-risk profiles.
