import pandas as pd
import numpy as np
import json

print("⚙️ Kurulum başlatılıyor...")

# 1. Verileri Yükle
try:
    df_raw = pd.read_csv('new_fuel_corrected.csv', sep=';')
    df_encoded = pd.read_csv('final_encoded_data.csv', sep=';')
except FileNotFoundError:
    print("HATA: csv dosyaları bulunamadı. Lütfen klasörü kontrol edin.")
    exit()

# 2. Eksik Verileri Doldur
for col in ['Renk', 'Boya', 'Değişen']:
    if col in df_raw.columns:
        mode_val = df_raw[col].mode()[0]
        df_raw[col].fillna(mode_val, inplace=True)

# 3. KATEGORİK HARİTAYI ÇIKAR
mappings = {}
kategorik_kolonlar = ['Vites', 'Yakıt', 'Renk', 'Kasa Tipi']

for col in kategorik_kolonlar:
    if col in df_raw.columns:
        unique_vals = sorted(df_raw[col].astype(str).unique())
        mappings[col] = {val: i for i, val in enumerate(unique_vals)}
        print(f"✅ {col} haritası çıkarıldı. ({len(unique_vals)} seçenek)")

# 4. SERİ SÖZLÜĞÜNÜ OLUŞTUR
seri_sozlugu = {}
if 'Log_Fiyat' not in df_raw.columns:
    df_raw['Log_Fiyat'] = np.log(df_raw['Fiyat'])

markalar = df_raw['Marka'].unique()
for marka in markalar:
    seri_sozlugu[marka] = {}
    seriler = df_raw[df_raw['Marka'] == marka]['Seri'].unique()
    for seri in seriler:
        avg_log = df_raw[(df_raw['Marka'] == marka) & (df_raw['Seri'] == seri)]['Log_Fiyat'].mean()
        seri_sozlugu[marka][seri] = avg_log

mappings['Seri_Sozlugu'] = seri_sozlugu
print("✅ Seri fiyatları hesaplandı.")

# 5. SÜTUN SIRASINI KAYDET (DÜZELTİLEN KISIM BURASI)
# Modelin beklediği sütunları alıyoruz VE elle oluşturduğumuz özellikleri ekliyoruz.
train_cols = [c for c in df_encoded.columns if c not in ['Fiyat', 'Log_Fiyat', 'Yıl']]
train_cols = train_cols + ['Yas', 'Yillik_Km']  # <-- BURASI EKLENDİ

mappings['Model_Columns'] = train_cols
print(f"✅ Model sütun sırası kaydedildi. ({len(train_cols)} sütun)")

# 6. JSON OLARAK KAYDET
with open('system_config.json', 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=4)

print("\n🎉 KURULUM TAMAMLANDI! 'system_config.json' güncellendi.")
print("Şimdi app.py'yi tekrar çalıştırabilirsiniz.")