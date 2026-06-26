"""
model.py — Training dan penyimpanan model prediksi hasil panen
Jalankan file ini sekali untuk membuat model.pkl dan encoders.pkl
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import joblib
import os

# ─── LOAD DATASET ─────────────────────────────────────────────────────────────
def load_data(filepath="yield_df.csv"):
    """Muat dataset dari file CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset '{filepath}' tidak ditemukan.\n"
            "Download dari: https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset\n"
            "Simpan sebagai 'yield_df.csv' di folder yang sama dengan model.py"
        )
    df = pd.read_csv(filepath)
    print(f"✅ Dataset berhasil dimuat: {df.shape[0]} baris, {df.shape[1]} kolom")
    print(f"   Kolom: {list(df.columns)}")
    return df


# ─── PREPROCESSING ────────────────────────────────────────────────────────────
def preprocess(df):
    """Bersihkan dan encode dataset."""
    # Hapus kolom yang tidak diperlukan (jika ada)
    drop_cols = [c for c in ["Unnamed: 0"] if c in df.columns]
    df = df.drop(columns=drop_cols)

    # Standarisasi nama kolom
    df.columns = [c.strip() for c in df.columns]

    # Hapus baris dengan nilai kosong
    df = df.dropna()

    # Encode kolom kategorikal
    encoders = {}
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    # Pastikan kolom target tidak di-encode
    target = "hg/ha_yield"
    if target in cat_cols:
        cat_cols.remove(target)

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        print(f"   Encode '{col}': {list(le.classes_[:5])}{'...' if len(le.classes_) > 5 else ''}")

    return df, encoders, cat_cols


# ─── TRAIN MODEL ──────────────────────────────────────────────────────────────
def train(df, encoders, cat_cols):
    """Latih model Random Forest Regressor."""
    target = "hg/ha_yield"

    feature_cols = [c for c in df.columns if c != target]
    X = df[feature_cols]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\n🌲 Melatih Random Forest ({X_train.shape[0]} data latih)...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluasi
    y_pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    r2   = r2_score(y_test, y_pred)
    print(f"\n📊 Hasil Evaluasi Model:")
    print(f"   MAE (Mean Absolute Error) : {mae:,.0f} hg/ha")
    print(f"   R² Score                  : {r2:.4f}  ({r2*100:.1f}% variance explained)")

    # Feature importance
    importances = pd.Series(
        model.feature_importances_, index=feature_cols
    ).sort_values(ascending=False)
    print(f"\n🔍 Feature Importance (Top 5):")
    print(importances.head(5).to_string())

    return model, feature_cols, importances


# ─── SIMPAN MODEL ─────────────────────────────────────────────────────────────
def save_artifacts(model, encoders, feature_cols, importances):
    """Simpan model dan encoder ke file .joblib (compressed)."""
    payload = {
        "model"        : model,
        "encoders"     : encoders,
        "feature_cols" : feature_cols,
        "importances"  : importances,
    }
    joblib.dump(payload, "model.joblib", compress=3)
    print("\n✅ Model tersimpan di 'model.joblib' (compressed)")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  CROP YIELD PREDICTOR — Training Model")
    print("=" * 55)

    df              = load_data("yield_df.csv")
    df, encoders, cat_cols = preprocess(df)
    model, feature_cols, importances = train(df, encoders, cat_cols)
    save_artifacts(model, encoders, feature_cols, importances)

    print("\n🚀 Selesai! Sekarang jalankan: streamlit run app.py")
    print("=" * 55)
