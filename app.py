import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json

# ---------------------------------------------------------
# 1. AYARLAR VE YÜKLEMELER
# ---------------------------------------------------------
st.set_page_config(page_title="Araba Fiyat Tahmini", page_icon="🚗")

@st.cache_resource
def load_system():
    # Modelleri Yükle
    rf = joblib.load('random_forest_model.pkl')
    hgb = joblib.load('hist_gradient_boosting_model.pkl')
    
    # Kurulum dosyasını yükle (Tüm ayarlar burada)
    with open('system_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    return rf, hgb, config

try:
    rf_model, hgb_model, config = load_system()
    st.success("✅ Sistem başarıyla yüklendi!")
except FileNotFoundError:
    st.error("HATA: 'system_config.json' veya model dosyaları bulunamadı. Lütfen önce setup_full.py'yi çalıştırın.")
    st.stop()

# Config'den verileri çekelim
seri_dict = config['Seri_Sozlugu']
vites_map = config['Vites']
yakit_map = config['Yakıt']
renk_map = config['Renk']
kasa_map = config['Kasa Tipi']
model_columns = config['Model_Columns']

# ---------------------------------------------------------
# 2. ARAYÜZ
# ---------------------------------------------------------
st.title("🚗 Profesyonel Fiyat Tahmin Sistemi")
st.markdown("Aracın özelliklerini seçin, yapay zeka gerçek piyasa verileriyle hesaplasın.")

col1, col2 = st.columns(2)

with col1:
    # MARKA VE SERİ (Dinamik)
    marka_listesi = sorted(list(seri_dict.keys()))
    secilen_marka = st.selectbox("Marka", marka_listesi)
    
    seri_listesi = sorted(list(seri_dict[secilen_marka].keys()))
    secilen_seri = st.selectbox("Model / Seri", seri_listesi)
    
    yil = st.number_input("Model Yılı", min_value=1990, max_value=2024, value=2015)
    km = st.number_input("Kilometre", min_value=0, value=100000, step=5000)
    
    # VİTES (Config'den gelen gerçek seçenekler)
    vites = st.selectbox("Vites", sorted(vites_map.keys()))

with col2:
    motor_hacmi = st.number_input("Motor Hacmi (cc)", min_value=800, value=1600)
    motor_gucu = st.number_input("Motor Gücü (hp)", min_value=50, value=110)
    
    # YAKIT (Config'den)
    yakit = st.selectbox("Yakıt", sorted(yakit_map.keys()))
    
    # KASA TİPİ (Config'den - Artık '0' gitmeyecek!)
    kasa = st.selectbox("Kasa Tipi", sorted(kasa_map.keys()))
    
    # RENK (Config'den - Artık '0' gitmeyecek!)
    renk = st.selectbox("Renk", sorted(renk_map.keys()))
    
    st.write("---")
    boya = st.slider("Boyalı Parça", 0, 15, 0)
    degisen = st.slider("Değişen Parça", 0, 15, 0)

# ---------------------------------------------------------
# 3. VERİ HAZIRLAMA (Backend)
# ---------------------------------------------------------
def prepare_input_data():
    # A. Özellik Mühendisliği
    yas = 2025 - yil
    yillik_km = km / (yas + 1)
    
    # B. Temel Sözlük
    # Burada modelin beklediği sütun isimlerine göre boş bir yapı oluşturuyoruz
    # Böylece sütun sırası asla kaymaz.
    input_data = {col: 0 for col in model_columns}
    
    # C. Değerleri Yerleştirme
    input_data['Seri'] = seri_dict[secilen_marka][secilen_seri]
    input_data['Kilometre'] = km
    input_data['Vites'] = vites_map[vites]
    input_data['Yakıt'] = yakit_map[yakit]
    input_data['Renk'] = renk_map[renk]
    input_data['Kasa Tipi'] = kasa_map[kasa]
    input_data['Motor Hacmi'] = motor_hacmi
    input_data['Motor Gücü'] = motor_gucu
    input_data['Boya'] = boya
    input_data['Değişen'] = degisen
    input_data['Yas'] = yas
    input_data['Yillik_Km'] = yillik_km
    
    # D. Marka (One-Hot Encoding)
    # Modelde 'Marka_Volkswagen' gibi sütunlar var. Seçileni 1 yapıyoruz.
    marka_col = f"Marka_{secilen_marka}"
    if marka_col in input_data:
        input_data[marka_col] = 1
        
    # DataFrame'e çevir (Sütun sırasını garantiye alarak)
    df = pd.DataFrame([input_data])
    
    # Modelin beklediği sütun sırasına göre diz (Garanti olsun)
    df = df[model_columns]
    
    return df

# ---------------------------------------------------------
# 4. TAHMİN
# ---------------------------------------------------------
if st.button("Fiyatı Hesapla 🔍", type="primary"):
    input_df = prepare_input_data()
    
    # Tahmin
    log_pred = hgb_model.predict(input_df)[0]
    gercek_fiyat = np.exp(log_pred)
    
    st.divider()
    st.success(f"🚘 {secilen_marka} {secilen_seri} ({yil})")
    st.metric(label="Tahmini Piyasa Değeri", value=f"{gercek_fiyat:,.0f} TL")
    
    st.info("Bu sistem, Kasa Tipi, Renk ve Seri verilerini eğitim veri setindeki gerçek dağılıma göre işler.")