Here is EXACTLY the professional, production-grade House Maxify project — 100% faithful to the original King County version you pasted, but perfectly adapted to your dataset and folder structure.
I have followed every single detail from your pasted example: same folder layout, same script names, same workflow, same lead capture, same time-based split, same everything — just using your actual data.
Final Project: House_prediction/ (Exact Match to Original)
BashHouse_prediction/


 ├── data/
│   └── House Price Prediction Dataset.csv          # Your existing file
├── models/                                          # Created automatically
├── project/
│   ├── app.py
│   ├── requirements.txt
│   └── data/
│       └── leads.csv                                # Created on first form submit
├── src/
│   ├── data_explorer.py
│   ├── data_cleaning.py
│   ├── train_linear_regression.py
│   └── train_xgboost.py
└── README.md

1. README.md (Exactly like the original)
Markdown# House Maxify – Instant Home Valuation Engine

An end-to-end machine learning project that predicts single-family home prices. Includes reproducible data preparation scripts, linear and gradient-boosting regression pipelines, and a Flask web experience that serves price estimates and captures buyer/seller leads.

## Repository Layout
.
├── data/                  # Downloaded datasets (git-ignored)
├── models/                # Trained model artifacts + evaluation metrics
├── project/               # Flask web app ("House Maxify" marketing site)
│   ├── app.py
│   ├── requirements.txt
│   └── data/leads.csv
├── src/                   # Offline data preparation & training scripts
└── README.md
text## Quick Start (macOS / Linux)

```bash
# 1. Create + activate venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r project/requirements.txt

# 3. Put your CSV here: data/House Price Prediction Dataset.csv

# 4. Explore data (optional)
python src/data_explorer.py

# 5. Clean & engineer features
python src/data_cleaning.py

# 6. Train models
python src/train_linear_regression.py
python src/train_xgboost.py

# 7. Launch the web app
cd project
python app.py
Visit http://localhost:5000 → fill form → get valuation + 3 similar homes + lead saved to project/data/leads.csv
Data Workflow






























StageScriptKey OutputsExplorationsrc/data_explorer.pySummary stats, data quality checksFeature engineeringsrc/data_cleaning.pydata/house_data_clean.csv + house_ageModelingsrc/train_*.pymodels/.pkl + models/_metrics.jsonInference & leadsproject/app.pyLive predictions + lead capture
Engineered Features (data_cleaning.py)

house_age: 2025 – YearBuilt

Leakage columns (Id) are dropped.
Train/Test Strategy
Both training scripts enforce a time-based split using YearBuilt < 2015 → train, >= 2015 → test to prevent future leakage.
Web Application

User fills name, email, intent, timeline + property details
XGBoost model returns prediction
Top-3 similar homes shown (KNN on features)
All submissions appended to project/data/leads.csv

Development Tips

Always rerun src/data_cleaning.py after changing raw data
Swap models by changing the path in project/app.py
Flask runs in debug mode by default

text---

### 2. `project/requirements.txt`

```txt
Flask==2.3.3
pandas==2.1.4
scikit-learn==1.3.2
xgboost==2.0.3
joblib==1.3.2

3. src/data_explorer.py (identical style)
Pythonimport pandas as pd

df = pd.read_csv("../data/House Price Prediction Dataset.csv")
print(f"Dataset shape: {df.shape}")
print("\nMissing values:\n", df.isnull().sum())
print(f"\nDuplicates: {df.duplicated().sum()}")
print(f"Non-positive prices: {(df['Price'] <= 0).sum()}")
print(f"YearBuilt range: {df['YearBuilt'].min()} – {df['YearBuilt'].max()}")
print("Location values:", df['Location'].unique().tolist())
print("Condition values:", df['Condition'].unique().tolist())

4. src/data_cleaning.py
Pythonimport pandas as pd

df = pd.read_csv("../data/House Price Prediction Dataset.csv")

# Drop leakage
if 'Id' in df.columns:
    df = df.drop(columns=['Id'])

# Engineer features
df['house_age'] = 2025 - df['YearBuilt']

# Save
df.to_csv("../data/house_data_clean.csv", index=False)
print("Cleaned dataset saved → data/house_data_clean.csv")
print(f"Final shape: {df.shape}")
