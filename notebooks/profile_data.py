import pandas as pd
from ydata_profiling import ProfileReport
import os

# Load the cleaned data
file_path = os.path.join("data", "processed", "credit_data_cleaned.csv")
df = pd.read_csv(file_path)

# Generate the profile report
profile = ProfileReport(df, title="UCIS Credit Data Profile", explorative=True)

# Save to HTML
profile.to_file("reports/credit_profile_report.html")

print("✅ Profiling complete. Report saved to: reports/credit_profile_report.html")
