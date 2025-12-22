import pandas as pd
import numpy as np
import json

print("⚙️ Kurulum başlatılıyor...")

# 1. VERİLERİ YÜKLE
# Dosya isminiz neyse onu kullanın. Kodlarınızdan anladığım kadarıyla bu:
try:
    df_raw = pd.read_csv('new_fuel_corrected.csv', sep=';')
except FileNotFoundError:
    print("HATA: 'new_fuel_corrected.csv' bulunamadı.")
    exit()

# 2. TEMİZLİK VE DOLGU
for col in ['Renk', 'Boya', 'Değişen', 'Kasa Tipi', 'Vites', 'Yakıt']:
    if col in df_raw.columns:
        mode_val = df_raw[col].mode()[0]
        df_raw[col].fillna(mode_val, inplace=True)

# 3. LABEL ENCODING HARİTALARINI ÇIKAR
mappings = {}
# Buradaki isimler CSV dosyanızdaki sütun başlıklarıyla AYNI olmalı
kategorik_kolonlar = ['Vites', 'Yakıt', 'Renk', 'Kasa Tipi']

for col in kategorik_kolonlar:
    if col in df_raw.columns:
        # Alfabetik sıraya göre harita çıkar
        unique_vals = sorted(df_raw[col].astype(str).unique())
        mappings[col] = {val: i for i, val in enumerate(unique_vals)}
        print(f"✅ {col} haritası çıkarıldı. ({len(unique_vals)} seçenek)")
    else:
        print(f"UYARI: {col} sütunu dosyada bulunamadı!")

# 4. SERİ SÖZLÜĞÜNÜ OLUŞTUR (Target Encoding - Log1p ile)
seri_sozlugu = {}

# Fiyat sütununun logaritmasını al (Model eğitimiyle uyumlu olması için log1p)
df_raw['Log_Fiyat'] = np.log1p(df_raw['Fiyat'])

markalar = sorted(df_raw['Marka'].unique())
for marka in markalar:
    seri_sozlugu[marka] = {}
    # Sadece o markaya ait serileri al
    seriler = df_raw[df_raw['Marka'] == marka]['Seri'].unique()
    
    for seri in seriler:
        # O serinin ortalama log fiyatını bul
        avg_log = df_raw[(df_raw['Marka'] == marka) & (df_raw['Seri'] == seri)]['Log_Fiyat'].mean()
        seri_sozlugu[marka][seri] = avg_log

mappings['Seri_Sozlugu'] = seri_sozlugu
print(f"✅ Seri fiyatları {len(markalar)} marka için hesaplandı.")

# 5. MODEL SÜTUN SIRASINI BELİRLE
# Bu liste, modelinizi eğitirken (train.py) kullandığınız X sütunlarının sırasıyla BİREBİR AYNI olmalı.
# Genelde şöyledir:
model_sutunlari = [
    'Vites', 'Yakıt', 'Renk', 'Kasa Tipi', 
    'Kilometre', 'Motor Hacmi', 'Motor Gücü', 
    'Boya', 'Değişen', 
    'Seri', 'Yas', 'Yillik_Km'
]

# Markaları da One-Hot Encoding olarak ekle (Marka_Audi, Marka_BMW vb.)
for marka in markalar:
    model_sutunlari.append(f"Marka_{marka}")

mappings['Model_Columns'] = model_sutunlari
print(f"✅ Model sütun sırası kaydedildi.")

# 6. JSON OLARAK KAYDET
with open('system_config.json', 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=4)

print("\n🎉 KURULUM TAMAMLANDI! 'system_config.json' dosyası sıfırdan oluşturuldu.")