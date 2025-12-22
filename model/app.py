import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json

# --- 1. AYARLAR ---
st.set_page_config(page_title="Araç Fiyat Tahmini", page_icon="🚗")

@st.cache_resource
def load_system():
    # İki modeli de yüklemeye çalışıyoruz
    models = {}
    try:
        models['rf'] = joblib.load('random_forest_model.pkl')
        models['hgb'] = joblib.load('hist_gradient_boosting_model.pkl')
    except Exception as e:
        st.error(f"Model dosyaları bulunamadı! Lütfen train_final.py'yi çalıştırın. Hata: {e}")
        st.stop()

    with open('system_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    return models, config

try:
    models, config = load_system()
except FileNotFoundError:
    st.error("HATA: 'system_config.json' bulunamadı.")
    st.stop()

# Config Verileri
seri_dict = config['Seri_Sozlugu']
vites_map = config['Vites']
yakit_map = config['Yakıt']
renk_map = config['Renk']
kasa_map = config['Kasa Tipi']
model_columns = config['Model_Columns']
marka_listesi = sorted(list(seri_dict.keys()))

# --- 2. ARAYÜZ ---
st.title("🚗 Profesyonel Fiyat Tahmini")
st.markdown("**Çift Motorlu Yapay Zeka:** Random Forest & Gradient Boosting Ortalaması")

col1, col2 = st.columns(2)

with col1:
    secilen_marka = st.selectbox("Marka", marka_listesi)
    
    uygun_seriler = sorted(list(seri_dict.get(secilen_marka, {}).keys()))
    if not uygun_seriler: uygun_seriler = ["Model Bulunamadı"]
    secilen_seri = st.selectbox("Seri / Model", uygun_seriler)

    yil = st.number_input("Model Yılı", 1990, 2024, 2017)
    km = st.number_input("Kilometre", 0, 999999, 100000, step=5000)
    vites = st.selectbox("Vites", sorted(vites_map.keys()))

with col2:
    motor_hacmi = st.number_input("Motor Hacmi (cc)", 800, 6500, 1600)
    motor_gucu = st.number_input("Motor Gücü (hp)", 40, 1000, 110)
    yakit = st.selectbox("Yakıt", sorted(yakit_map.keys()))
    kasa = st.selectbox("Kasa Tipi", sorted(kasa_map.keys()))
    renk = st.selectbox("Renk", sorted(renk_map.keys()))

st.divider()
c1, c2 = st.columns(2)
boya = c1.slider("Boyalı Parça", 0, 15, 0)
degisen = c2.slider("Değişen Parça", 0, 15, 0)

if st.button("FİYATI HESAPLA 🔍", type="primary"):
    
    # A. Veri Hazırlama
    input_data = {}
    input_data['Vites'] = vites_map.get(vites, 0)
    input_data['Yakıt'] = yakit_map.get(yakit, 0)
    input_data['Renk'] = renk_map.get(renk, 0)
    input_data['Kasa Tipi'] = kasa_map.get(kasa, 0)
    
    input_data['Kilometre'] = km
    input_data['Motor Hacmi'] = motor_hacmi
    input_data['Motor Gücü'] = motor_gucu
    input_data['Boya'] = boya
    input_data['Değişen'] = degisen
    
    yas = 2025 - yil
    input_data['Yas'] = yas
    input_data['Yillik_Km'] = km / (yas + 1)
    
    try: input_data['Seri'] = seri_dict[secilen_marka][secilen_seri]
    except: input_data['Seri'] = 0
    
    for col in model_columns:
        if 'Marka_' in col: input_data[col] = 0     
    secilen_marka_col = f"Marka_{secilen_marka}"
    if secilen_marka_col in model_columns: input_data[secilen_marka_col] = 1
    else: input_data[f"Marka_{secilen_marka}"] = 1

    df_input = pd.DataFrame([input_data])
    for col in model_columns:
        if col not in df_input.columns: df_input[col] = 0
    df_input = df_input[model_columns]
    
    # B. Çift Model Tahmini
    # 1. Random Forest Tahmini
    log_rf = models['rf'].predict(df_input)[0]
    fiyat_rf = np.expm1(log_rf)
    
    # 2. HGB Tahmini
    log_hgb = models['hgb'].predict(df_input)[0]
    fiyat_hgb = np.expm1(log_hgb)
    
    # 3. Ortalama (Ensemble)
    ortalama_fiyat = (fiyat_rf + fiyat_hgb) / 2
    
    # C. Sonuç Ekranı
    st.success(f"🚘 {secilen_marka} {secilen_seri}")
    
    # Ana Büyük Gösterge
    st.metric("Ortalama Piyasa Değeri", f"{ortalama_fiyat:,.0f} TL")
    
    # Detaylar
    st.markdown("---")
    col_d1, col_d2 = st.columns(2)
    col_d1.info(f"🌲 Random Forest: {fiyat_rf:,.0f} TL")
    col_d2.info(f"🚀 Gradient Boosting: {fiyat_hgb:,.0f} TL")
    
    alt = ortalama_fiyat * 0.92
    ust = ortalama_fiyat * 1.08
    st.caption(f"Güvenilir Aralık: {alt:,.0f} TL - {ust:,.0f} TL")