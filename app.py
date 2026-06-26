"""
app.py — AgroYield Predictor (Dark Theme)
Jalankan dengan: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import sys

# ─── AUTO-TRAIN MODEL IF NOT EXISTS ──────────────────────────────────────────
if not os.path.exists("model.joblib"):
    st.info("⏳ Melatih model untuk pertama kali... Ini membutuhkan waktu ~1-2 menit.")
    try:
        result = subprocess.run([sys.executable, "model.py"], capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            st.success("✅ Model berhasil dilatih! Refresh halaman untuk memulai.")
        else:
            st.error(f"❌ Gagal melatih model:\n{result.stderr}")
    except subprocess.TimeoutExpired:
        st.error("⏱️ Pelatihan model timeout (>5 menit)")
    except Exception as e:
        st.error(f"❌ Error saat melatih model: {str(e)}")

# ─── KONFIGURASI HALAMAN ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroYield — Prediksi Hasil Panen",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DARK THEME CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── BASE DARK THEME ── */
    .stApp {
        background: #0D1117 !important;
    }
    
    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #161B22; }
    ::-webkit-scrollbar-thumb { background: #30363D; border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: #52B788; }
    
    /* ── Text ── */
    .stMarkdown, .stText, .stNumberInput label, .stSelectbox label, .stSlider label,
    .stMetric label, .stMetric .value, .stMetric .delta {
        color: #E6EDF3 !important;
    }
    
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #161B22 !important;
        border-right: 1px solid #30363D !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #E6EDF3 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #F0F6FC !important;
    }
    
    /* ── Input Widgets ── */
    .stSelectbox > div > div {
        background: #0D1117 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        color: #E6EDF3 !important;
    }
    .stSelectbox > div > div > div {
        color: #E6EDF3 !important;
    }
    .stNumberInput > div > div > input {
        background: #0D1117 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        color: #E6EDF3 !important;
    }
    .stSlider > div > div > div > div {
        background: #52B788 !important;
    }
    .stSlider > div > div > div > div > div {
        background: #52B788 !important;
    }
    .stSlider label {
        color: #8B949E !important;
    }
    
    /* ── Button ── */
    .stButton > button {
        background: #52B788 !important;
        color: #0D1117 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #409B6F !important;
        transform: scale(1.02);
    }
    
    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 2px solid #30363D;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 20px;
        font-weight: 600;
        color: #8B949E !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #E6EDF3 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #52B788 !important;
        border-bottom: 3px solid #52B788 !important;
        background: transparent !important;
    }
    
    /* ── Metric ── */
    [data-testid="metric-container"] {
        background: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
    }
    [data-testid="metric-container"] label {
        color: #8B949E !important;
    }
    [data-testid="metric-container"] .value {
        color: #F0F6FC !important;
    }
    
    /* ── Info / Warning / Error ── */
    .stInfo {
        background: #161B22 !important;
        color: #8B949E !important;
        border-left: 4px solid #52B788 !important;
    }
    .stInfo svg { fill: #52B788 !important; }
    .stWarning {
        background: #1C1A0A !important;
        border-left: 4px solid #D97706 !important;
    }
    .stError {
        background: #1A0A0A !important;
        border-left: 4px solid #DC2626 !important;
    }
    
    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363D !important;
        border-radius: 10px !important;
    }
    [data-testid="stDataFrame"] thead th {
        background: #161B22 !important;
        color: #F0F6FC !important;
    }
    [data-testid="stDataFrame"] tbody td {
        color: #E6EDF3 !important;
    }
    
    /* ── Expander ── */
    .streamlit-expanderHeader {
        color: #F0F6FC !important;
        background: #161B22 !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background: #0D1117 !important;
    }
    
    /* ── Divider ── */
    hr {
        border-color: #30363D !important;
    }
    
    /* ── Code ── */
    .stCodeBlock {
        background: #161B22 !important;
        border-radius: 8px !important;
    }
    
    /* ── Selectbox dropdown ── */
    div[data-baseweb="select"] > div {
        background: #0D1117 !important;
    }
    
    /* ══ HERO DARK ══ */
    .hero-dark {
        background: linear-gradient(135deg, #0D1A13 0%, #1A3A2A 50%, #0D1A13 100%);
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .hero-dark-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .hero-dark-icon {
        font-size: 2.6rem;
        line-height: 1;
    }
    .hero-dark-title {
        font-size: 1.7rem;
        font-weight: 800;
        color: #F0F6FC;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .hero-dark-sub {
        font-size: 0.85rem;
        color: #8B949E;
        margin: 2px 0 0;
    }
    .hero-dark-badge {
        background: #1A3A2A;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 0.4rem 1.2rem;
        color: #52B788;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    /* ══ STAT CARDS DARK ══ */
    .stat-grid-dark {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        margin: 1rem 0;
    }
    .stat-card-dark {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        text-align: center;
    }
    .stat-card-dark .stat-number {
        font-size: 1.6rem;
        font-weight: 800;
        color: #F0F6FC;
        line-height: 1.2;
    }
    .stat-card-dark .stat-label {
        font-size: 0.65rem;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 2px;
    }
    .stat-card-dark .stat-sub {
        font-size: 0.6rem;
        color: #484F58;
    }
    
    /* ══ SECTION HEADER DARK ══ */
    .section-header-dark {
        font-size: 1rem;
        font-weight: 700;
        color: #F0F6FC;
        margin: 1.5rem 0 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ══ FEATURE CARDS DARK ══ */
    .feature-grid-dark {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .feature-card-dark {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .feature-card-dark:hover {
        border-color: #52B788;
    }
    .feature-card-dark .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }
    .feature-card-dark .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F0F6FC;
        margin: 0.3rem 0 0.1rem;
    }
    .feature-card-dark .feature-desc {
        font-size: 0.8rem;
        color: #8B949E;
        margin: 0;
    }
    
    /* ══ SIDEBAR LABEL ══ */
    .sidebar-label-dark {
        font-size: 0.7rem;
        font-weight: 700;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 1rem 0 0.3rem;
        display: block;
    }
    .sidebar-title-dark {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F0F6FC;
        margin-bottom: 0.5rem;
    }
    
    /* ── Chart Container ── */
    .chart-box-dark {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* ── Badge Kategori ── */
    .badge-dark {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .badge-dark-high {
        background: #1A3A2A;
        color: #52B788;
    }
    .badge-dark-medium {
        background: #3A2A0A;
        color: #D97706;
    }
    .badge-dark-low {
        background: #3A1A1A;
        color: #DC2626;
    }
    
    /* ── Card Hasil ── */
    .result-card-dark {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .result-card-dark .result-label {
        font-size: 0.7rem;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .result-card-dark .result-value {
        font-size: 2rem;
        font-weight: 800;
        color: #F0F6FC;
        line-height: 1.2;
    }
    .result-card-dark .result-unit {
        font-size: 0.7rem;
        color: #484F58;
    }
</style>
""", unsafe_allow_html=True)


# ─── LOAD MODEL & DATA ──────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists("model.joblib"):
        return None
    return joblib.load("model.joblib")

@st.cache_data
def load_raw_data():
    if not os.path.exists("yield_df.csv"):
        return None
    df = pd.read_csv("yield_df.csv")
    drop_cols = [c for c in ["Unnamed: 0"] if c in df.columns]
    return df.drop(columns=drop_cols).dropna()

artifacts = load_model()
raw_df = load_raw_data()


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title-dark">🌱 Input Parameter</div>', unsafe_allow_html=True)
    
    st.markdown('<span class="sidebar-label-dark">Tanaman & Lokasi</span>', unsafe_allow_html=True)
    
    if artifacts is not None:
        encoders = artifacts["encoders"]
        crop_options = list(encoders["Item"].classes_) if "Item" in encoders else ["Cassava", "Rice", "Wheat", "Maize"]
        area_options = list(encoders["Area"].classes_) if "Area" in encoders else ["Albania", "Indonesia"]
    else:
        crop_options = ["Cassava", "Rice", "Wheat", "Maize"]
        area_options = ["Albania", "Indonesia"]
    
    selected_crop = st.selectbox("Jenis Tanaman", crop_options)
    selected_area = st.selectbox("Wilayah / Negara", area_options)
    selected_year = st.slider("Tahun", min_value=1990, max_value=2030, value=2023)
    
    st.markdown('<span class="sidebar-label-dark">Kondisi Iklim & Agronomi</span>', unsafe_allow_html=True)
    
    rainfall = st.number_input("Curah Hujan (mm/tahun)", min_value=0.0, max_value=5000.0, value=1200.0, step=10.0)
    avg_temp = st.number_input("Suhu Rata-rata (°C)", min_value=-10.0, max_value=50.0, value=27.0, step=0.5)
    pesticides = st.number_input("Pestisida (ton)", min_value=0.0, max_value=500000.0, value=5000.0, step=100.0)
    
    st.markdown("---")
    predict_btn = st.button("🔍 Prediksi Sekarang", use_container_width=True)


# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-dark">
    <div class="hero-dark-left">
        <div class="hero-dark-icon">🌾</div>
        <div>
            <div class="hero-dark-title">AgroYield Predictor</div>
            <div class="hero-dark-sub">AI untuk pertanian modern dan berkelanjutan</div>
        </div>
    </div>
    <div class="hero-dark-badge">v2.0 · ML Ready</div>
</div>
""", unsafe_allow_html=True)


# ─── CEK MODEL ──────────────────────────────────────────────────────────────
if artifacts is None:
    st.error("⚠️ Model belum dilatih. Jalankan: `python model.py`")
    st.code("python model.py", language="bash")
    st.stop()

model = artifacts["model"]
encoders = artifacts["encoders"]
feature_cols = artifacts["feature_cols"]
importances = artifacts["importances"]


# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Prediksi", "📈 Analisis Data", "ℹ️ Tentang Model"])


# ════ TAB 1 — PREDIKSI ════════════════════════════════════════════════════
with tab1:
    if predict_btn:
        # ── Build Input ──
        row = {}
        for col in feature_cols:
            cl = col.lower()
            if col in encoders:
                if col == "Item":
                    val = selected_crop
                elif col == "Area":
                    val = selected_area
                else:
                    val = encoders[col].classes_[0]
                row[col] = encoders[col].transform([val])[0]
            elif "year" in cl:
                row[col] = selected_year
            elif "rain" in cl:
                row[col] = rainfall
            elif "temp" in cl:
                row[col] = avg_temp
            elif "pesticide" in cl:
                row[col] = pesticides
            else:
                row[col] = 0
        
        input_df = pd.DataFrame([row])
        prediction = model.predict(input_df)[0]
        pred_ton = prediction / 10_000
        
        # ── Hasil ──
        st.markdown("### 📊 Hasil Prediksi")
        
        # Tentukan kategori
        if pred_ton >= 5:
            badge_html = '<span class="badge-dark badge-dark-high">🟢 Produktivitas Tinggi</span>'
            alert_msg = "✅ Kondisi lahan dan iklim sangat mendukung."
        elif pred_ton >= 2.5:
            badge_html = '<span class="badge-dark badge-dark-medium">🟡 Produktivitas Sedang</span>'
            alert_msg = "⚠️ Hasil panen cukup baik. Optimalkan pemupukan."
        else:
            badge_html = '<span class="badge-dark badge-dark-low">🔴 Produktivitas Rendah</span>'
            alert_msg = "🔴 Hasil panen di bawah rata-rata. Evaluasi input agronomi."
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="result-card-dark">
                <div class="result-label">Hasil Panen Prediksi</div>
                <div class="result-value">{pred_ton:,.2f}</div>
                <div class="result-unit">ton / hektar</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="result-card-dark">
                <div class="result-label">Satuan hg/ha</div>
                <div class="result-value">{prediction:,.0f}</div>
                <div class="result-unit">hektogram / hektar</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="result-card-dark">
                <div class="result-label">Kategori Produktivitas</div>
                <div style="margin-top:0.5rem">{badge_html}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info(alert_msg)
        
        # ── Feature Importance ──
        st.markdown("### 📈 Faktor Paling Berpengaruh")
        
        top_imp = importances.head(8).reset_index()
        top_imp.columns = ["Fitur", "Importance"]
        top_imp["Persen"] = (top_imp["Importance"] * 100).round(1)
        
        # Bersihkan nama fitur
        feature_names = {
            "Year": "📅 Tahun",
            "average_rain_fall_mm_per_year": "💧 Curah Hujan",
            "avg_temp": "🌡️ Suhu Rata-rata",
            "pesticides_tonnes": "🧪 Pestisida",
            "Item": "🌿 Jenis Tanaman",
            "Area": "🗺️ Wilayah",
        }
        top_imp["Fitur"] = top_imp["Fitur"].map(lambda x: feature_names.get(x, x))
        
        fig = px.bar(
            top_imp.sort_values("Persen"),
            x="Persen",
            y="Fitur",
            orientation="h",
            color="Persen",
            color_continuous_scale=["#1A3A2A", "#52B788", "#409B6F"],
            text="Persen",
        )
        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            marker=dict(line=dict(width=0))
        )
        fig.update_layout(
            height=300,
            showlegend=False,
            coloraxis_showscale=False,
            plot_bgcolor="#0D1117",
            paper_bgcolor="#0D1117",
            margin=dict(l=0, r=40, t=10, b=10),
            font=dict(color="#E6EDF3", family="Segoe UI, sans-serif"),
            xaxis=dict(gridcolor="#30363D", showline=False, zeroline=False, color="#8B949E"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", showline=False, color="#E6EDF3"),
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ── Detail ──
        with st.expander("📋 Detail Parameter"):
            detail_data = [
                ("Jenis Tanaman", selected_crop),
                ("Wilayah", selected_area),
                ("Tahun", selected_year),
                ("Curah Hujan (mm)", f"{rainfall:,.1f}"),
                ("Suhu Rata-rata (°C)", f"{avg_temp:.1f}"),
                ("Pestisida (ton)", f"{pesticides:,.1f}"),
            ]
            st.table(pd.DataFrame(detail_data, columns=["Parameter", "Nilai"]))
    
    else:
        # ── Tampilan Awal ──
        st.info("👈 Isi parameter di panel kiri, lalu klik **Prediksi Sekarang** untuk melihat hasil prediksi.")
        
        if raw_df is not None:
            # ── Stat Cards ──
            st.markdown("""
            <div class="stat-grid-dark">
                <div class="stat-card-dark">
                    <div class="stat-number">28.242</div>
                    <div class="stat-label">Total Data</div>
                    <div class="stat-sub">baris data</div>
                </div>
                <div class="stat-card-dark">
                    <div class="stat-number">10</div>
                    <div class="stat-label">Jenis Tanaman</div>
                    <div class="stat-sub">jenis tanaman</div>
                </div>
                <div class="stat-card-dark">
                    <div class="stat-number">101</div>
                    <div class="stat-label">Jumlah Wilayah</div>
                    <div class="stat-sub">wilayah</div>
                </div>
                <div class="stat-card-dark">
                    <div class="stat-number">1990–2013</div>
                    <div class="stat-label">Rentang Tahun</div>
                    <div class="stat-sub">periode data</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ── Charts ──
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🌿 Distribusi Tanaman")
                if "Item" in raw_df.columns:
                    crop_dist = raw_df["Item"].value_counts().reset_index()
                    crop_dist.columns = ["Tanaman", "Jumlah"]
                    
                    fig1 = px.pie(
                        crop_dist.head(8),
                        values="Jumlah",
                        names="Tanaman",
                        color_discrete_sequence=px.colors.sequential.Greens_r,
                        hole=0.4,
                    )
                    fig1.update_layout(
                        height=280,
                        margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor="#0D1117",
                        plot_bgcolor="#0D1117",
                        showlegend=False,
                        font=dict(color="#E6EDF3"),
                    )
                    fig1.update_traces(
                        textposition="inside",
                        textfont=dict(color="#0D1117", size=11, weight="bold"),
                    )
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.markdown("#### 🗺️ Top 5 Wilayah")
                if "Area" in raw_df.columns:
                    area_dist = raw_df["Area"].value_counts().head(5).reset_index()
                    area_dist.columns = ["Wilayah", "Jumlah"]
                    
                    fig2 = px.bar(
                        area_dist,
                        x="Wilayah",
                        y="Jumlah",
                        color="Jumlah",
                        color_continuous_scale=["#1A3A2A", "#52B788"],
                        text="Jumlah",
                    )
                    fig2.update_traces(
                        texttemplate="%{text:,}",
                        textposition="outside",
                        textfont=dict(color="#E6EDF3"),
                    )
                    fig2.update_layout(
                        height=280,
                        margin=dict(t=10, b=30, l=0, r=10),
                        paper_bgcolor="#0D1117",
                        plot_bgcolor="#0D1117",
                        showlegend=False,
                        coloraxis_showscale=False,
                        font=dict(color="#E6EDF3"),
                        xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#8B949E"),
                        yaxis=dict(gridcolor="#30363D", color="#8B949E"),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            
            # ── Semua Tanaman ──
            st.markdown("#### 🌾 Median Hasil Panen per Tanaman")
            if "Item" in raw_df.columns and "hg/ha_yield" in raw_df.columns:
                all_crops = (
                    raw_df.groupby("Item")["hg/ha_yield"]
                    .median()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                all_crops.columns = ["Tanaman", "Median (hg/ha)"]
                all_crops["ton/ha"] = (all_crops["Median (hg/ha)"] / 10000).round(2)
                
                fig3 = px.bar(
                    all_crops,
                    x="ton/ha",
                    y="Tanaman",
                    orientation="h",
                    color="ton/ha",
                    color_continuous_scale=["#1A3A2A", "#52B788", "#409B6F"],
                    text="ton/ha",
                )
                fig3.update_traces(
                    texttemplate="%{text} t/ha",
                    textposition="outside",
                    textfont=dict(color="#E6EDF3"),
                )
                fig3.update_layout(
                    height=280,
                    margin=dict(t=10, b=10, l=10, r=40),
                    paper_bgcolor="#0D1117",
                    plot_bgcolor="#0D1117",
                    showlegend=False,
                    coloraxis_showscale=False,
                    font=dict(color="#E6EDF3"),
                    xaxis=dict(gridcolor="#30363D", color="#8B949E", title="Hasil Panen (ton/ha)"),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#E6EDF3"),
                )
                st.plotly_chart(fig3, use_container_width=True)
        
        # ── Feature Cards ──
        st.markdown("""
        <div class="feature-grid-dark">
            <div class="feature-card-dark">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Akurat</div>
                <div class="feature-desc">Prediksi lebih tepat berbasis data</div>
            </div>
            <div class="feature-card-dark">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Cepat</div>
                <div class="feature-desc">Hasil prediksi dalam hitungan detik</div>
            </div>
            <div class="feature-card-dark">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">Terpercaya</div>
                <div class="feature-desc">Model terlatih dengan data historis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════ TAB 2 — ANALISIS DATA ════════════════════════════════════════════════
with tab2:
    if raw_df is None:
        st.warning("⚠️ Dataset tidak ditemukan.")
    else:
        st.markdown("### 📈 Analisis Data")
        
        # ── Tren ──
        st.markdown("#### 📈 Tren Produksi (ton/ha)")
        if "Year" in raw_df.columns and "hg/ha_yield" in raw_df.columns:
            trend = raw_df.groupby("Year")["hg/ha_yield"].mean().reset_index()
            trend["ton/ha"] = trend["hg/ha_yield"] / 10000
            
            fig = px.area(
                trend,
                x="Year",
                y="ton/ha",
                color_discrete_sequence=["#52B788"],
            )
            fig.update_traces(
                fill="tozeroy",
                fillcolor="rgba(82,183,136,0.15)",
                line=dict(width=2.5, color="#52B788"),
            )
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=30),
                paper_bgcolor="#0D1117",
                plot_bgcolor="#0D1117",
                font=dict(color="#E6EDF3"),
                xaxis=dict(gridcolor="#30363D", color="#8B949E", title="Tahun"),
                yaxis=dict(gridcolor="#30363D", color="#8B949E", title="Rata-rata (ton/ha)"),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ── Korelasi ──
        st.markdown("#### 🔗 Korelasi Antar Fitur")
        num_df = raw_df.select_dtypes(include=np.number)
        if len(num_df.columns) >= 2:
            fig = px.imshow(
                num_df.corr(),
                text_auto=".2f",
                color_continuous_scale=["#1A3A2A", "#52B788", "#409B6F"],
                aspect="auto",
            )
            fig.update_layout(
                height=400,
                margin=dict(t=10),
                paper_bgcolor="#0D1117",
                plot_bgcolor="#0D1117",
                font=dict(color="#E6EDF3"),
            )
            fig.update_xaxes(color="#8B949E")
            fig.update_yaxes(color="#8B949E")
            st.plotly_chart(fig, use_container_width=True)


# ════ TAB 3 — TENTANG MODEL ════════════════════════════════════════════════
with tab3:
    st.markdown("""
    ### 🌾 AgroYield Predictor
    **AI untuk pertanian modern & berkelanjutan**
    
    Prediksi berbasis AI & Machine Learning — Model kami dilatih dengan dataset historis 
    untuk memberikan prediksi hasil panen yang akurat dan terpercaya.
    """)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **🧠 Algoritma:** Random Forest Regressor
        
        - ✅ Tahan terhadap overfitting
        - ✅ Menangani data numerik & kategorikal
        - ✅ Memberikan feature importance
        - ✅ Tidak perlu normalisasi data
        """)
    with c2:
        st.markdown("""
        **📊 Dataset:** Kaggle Crop Yield Dataset
        
        - 🌿 10 jenis tanaman
        - 🗺️ 101 wilayah
        - 📅 1990–2013
        - 💧 6 fitur prediksi
        """)
    
    # ── Metrics ──
    metrics = artifacts.get("metrics", {})
    if metrics:
        st.markdown("### 📊 Evaluasi Model")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("R² Score", f"{metrics.get('r2', 0):.3f}")
        with m2:
            st.metric("RMSE", f"{metrics.get('rmse', 0):.2f}")
        with m3:
            st.metric("MAE", f"{metrics.get('mae', 0):.2f}")
    
    # ── Feature Cards ──
    st.markdown("""
    <div class="feature-grid-dark">
        <div class="feature-card-dark">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Akurat</div>
            <div class="feature-desc">Prediksi lebih tepat berbasis data</div>
        </div>
        <div class="feature-card-dark">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Cepat</div>
            <div class="feature-desc">Hasil prediksi dalam hitungan detik</div>
        </div>
        <div class="feature-card-dark">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Terpercaya</div>
            <div class="feature-desc">Model terlatih dengan data historis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("🌾 Dibuat untuk Ujian Praktikum · Program Studi Agroekoteknologi · UNTIRTA")