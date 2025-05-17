import pandas as pd
import sweetviz as sv
import os

# Load data
file_path = os.path.join("data", "processed", "credit_data_cleaned.csv")
df = pd.read_csv(file_path)

# Generate the report
report = sv.analyze(df)
report.show_html("reports/sweetviz_credit_report.html")

print("✅ Sweetviz report created at reports/sweetviz_credit_report.html")
