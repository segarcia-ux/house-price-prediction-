import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the dataset
data_path = '../data/House Price Prediction Dataset.csv'
df = pd.read_csv(data_path)

# Drop unnecessary column
df = df.drop('Id', axis=1)

# Features and target
X = df.drop('Price', axis=1)
y = df['Price']

# Define categorical and numerical columns
cat_cols = ['Location', 'Condition', 'Garage']
num_cols = ['Area', 'Bedrooms', 'Bathrooms', 'Floors', 'YearBuilt']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(), cat_cols)
    ])

# Full model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model on the full dataset
model.fit(X, y)

# Save the model
joblib.dump(model, 'model.pkl')
print("Model trained and saved as model.pkl")