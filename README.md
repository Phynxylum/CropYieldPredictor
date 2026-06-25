# 🌾 AgroYield Predictor
### Aplikasi Prediksi Hasil Panen berbasis AI — Ujian Praktikum Agroekoteknologi

---

## 📁 Struktur Folder Proyek

```
crop-yield-predictor/
├── app.py              ← Aplikasi utama (Streamlit UI)
├── model.py            ← Script training model ML
├── requirements.txt    ← Daftar library yang dibutuhkan
├── yield_df.csv        ← Dataset (download dari Kaggle — lihat Langkah 2)
├── model.pkl           ← File model terlatih (dibuat otomatis setelah Langkah 4)
└── README.md           ← Panduan ini
```

---

## 🚀 Panduan Lengkap dari Nol

### LANGKAH 1 — Install Python
1. Download Python dari https://python.org/downloads (versi 3.10 atau lebih baru)
2. Saat install, **centang** opsi "Add Python to PATH"
3. Buka **Command Prompt** (tekan Win+R, ketik `cmd`, Enter)
4. Cek instalasi berhasil:
   ```
   python --version
   ```
   Harusnya muncul: `Python 3.x.x`

---

### LANGKAH 2 — Download Dataset dari Kaggle
1. Buka browser, kunjungi:
   **https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset**
2. Login ke Kaggle (buat akun gratis jika belum punya)
3. Klik tombol **Download** (pojok kanan atas)
4. Extract file ZIP yang terdownload
5. Cari file bernama **`yield_df.csv`**
6. **Salin/pindahkan** file tersebut ke dalam folder `crop-yield-predictor/`

---

### LANGKAH 3 — Install Library yang Dibutuhkan
1. Buka Command Prompt
2. Masuk ke folder proyek:
   ```
   cd C:\Users\Alfino\crop-yield-predictor
   ```
   *(sesuaikan path dengan lokasi folder kalian)*
3. Install semua library sekaligus:
   ```
   pip install -r requirements.txt
   ```
4. Tunggu hingga selesai (bisa 2–5 menit tergantung koneksi internet)

---

### LANGKAH 4 — Training Model (Hanya Sekali)
1. Pastikan file `yield_df.csv` sudah ada di folder proyek
2. Jalankan script training:
   ```
   python model.py
   ```
3. Tunggu proses training selesai (~30–60 detik)
4. Jika berhasil, akan muncul output seperti:
   ```
   ✅ Dataset berhasil dimuat: 28.242 baris, 7 kolom
   🌲 Melatih Random Forest (22.593 data latih)...
   📊 Hasil Evaluasi Model:
      MAE  : 13.245 hg/ha
      R²   : 0.9312  (93.1% variance explained)
   ✅ Model tersimpan di 'model.pkl'
   🚀 Selesai! Sekarang jalankan: streamlit run app.py
   ```
5. File `model.pkl` akan muncul di folder — **jangan hapus!**

---

### LANGKAH 5 — Jalankan Aplikasi
1. Di Command Prompt (masih di folder proyek), jalankan:
   ```
   streamlit run app.py
   ```
2. Browser akan terbuka otomatis di alamat:
   **http://localhost:8501**
3. Aplikasi siap digunakan! 🎉

---

## 🎯 Cara Menggunakan Aplikasi

1. **Panel kiri (sidebar):**
   - Pilih jenis tanaman (contoh: Rice, Maize, Wheat)
   - Pilih wilayah/negara
   - Masukkan tahun
   - Isi curah hujan, suhu, dan penggunaan pestisida

2. **Klik tombol "🔍 Prediksi Sekarang"**

3. **Hasil prediksi muncul:**
   - Hasil dalam ton/hektar
   - Kategori produktivitas (Tinggi / Sedang / Rendah)
   - Rekomendasi singkat
   - Grafik faktor-faktor yang mempengaruhi hasil panen

4. **Tab lainnya:**
   - 📈 Analisis Data → visualisasi dataset
   - ℹ️ Tentang Model → penjelasan teknis AI

---

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` lagi |
| `FileNotFoundError: yield_df.csv` | Pastikan file CSV ada di folder proyek |
| `FileNotFoundError: model.pkl` | Jalankan `python model.py` terlebih dahulu |
| Browser tidak terbuka | Buka manual: http://localhost:8501 |
| Port 8501 sudah dipakai | `streamlit run app.py --server.port 8502` |

---

## 📊 Penjelasan Teknis (untuk Presentasi)

### Algoritma: Random Forest Regressor
- **Tipe:** Supervised Learning — Regression
- **Cara kerja:** Membangun 200 *decision tree* dari subset data acak, lalu rata-ratakan hasilnya
- **Kelebihan:** Akurat, tahan overfitting, bisa ukur feature importance

### Fitur (Input) Model:
| Fitur | Keterangan |
|-------|-----------|
| `Item` | Jenis tanaman (dikodekan dengan Label Encoder) |
| `Area` | Wilayah/negara (dikodekan dengan Label Encoder) |
| `Year` | Tahun tanam |
| `average_rain_fall_mm_per_year` | Curah hujan rata-rata (mm) |
| `avg_temp` | Suhu rata-rata (°C) |
| `pesticides_tonnes` | Jumlah pestisida yang digunakan (ton) |

### Target (Output) Model:
- `hg/ha_yield` = hasil panen dalam hektogram per hektar
- Dikonversi ke ton/ha untuk kemudahan interpretasi (÷ 10.000)

---

## 👥 Anggota Kelompok
*(isi sesuai anggota kelompok kalian)*

| Nama | NIM | Tugas |
|------|-----|-------|
|      |     | Data preprocessing & model training |
|      |     | Streamlit UI & visualisasi |
|      |     | Presentasi & dokumentasi |

---

*Dibuat untuk Ujian Praktikum | Program Studi Agroekoteknologi | UNTIRTA*
