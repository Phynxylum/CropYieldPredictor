import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("yield_df.csv")

print(f"Dataset loaded: {df.shape[0]} rows, columns: {list(df.columns)}")

# Encode categorical columns
label_encoders = {}

for col in ["Area", "Item"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
feature_names = [
    "Area",
    "Item",
    "Year",
    "average_rain_fall_mm_per_year",
    "pesticides_tonnes",
    "avg_temp",
]

X = df[feature_names]
y = df["hg/ha_yield"]

# Train model
print("Training Random Forest...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

print(f"Training complete. R² score: {model.score(X, y):.4f}")

# Save artifacts
artifacts = {
    "model": model,
    "label_encoders": label_encoders,
    "feature_names": feature_names,
    "importances": model.feature_importances_,
}

joblib.dump(artifacts, "artifacts.joblib")

print("Saved artifacts.joblib — you can now run the Streamlit app.")