import pandas as pd
import numpy as np
import json

# 1. Ham veriyi oku (Marka ve Seri isimlerinin olduğu dosya)
# Not: 'new_fuel_corrected.csv' dosyasında Marka ve Seri sütunları duruyor olmalı.
try:
    df = pd.read_csv('new_fuel_corrected.csv', sep=';')
except FileNotFoundError:
    print("HATA: 'new_fuel_corrected.csv' bulunamadı.")
    exit()

# 2. Log_Fiyat Hesapla (Eğer dosyada yoksa)
# Modelimiz Log_Fiyat üzerinden eğitildiği için sözlüğümüz de Log değerleri içermeli.
if 'Log_Fiyat' not in df.columns:
    df['Log_Fiyat'] = np.log(df['Fiyat'])

# 3. İçiçe Sözlük Yapısı Oluşturma
# Hedeflenen Yapı: { "Volkswagen": { "Golf": 13.9, "Passat": 14.1 }, "BMW": { "3 Serisi": 14.5 } }
sozluk = {}

markalar = df['Marka'].unique()

print("Sözlük oluşturuluyor...")

for marka in markalar:
    # Her marka için boş bir sözlük aç
    sozluk[marka] = {}
    
    # O markaya ait serileri bul
    seriler = df[df['Marka'] == marka]['Seri'].unique()
    
    for seri in seriler:
        # O markanın o serisinin ortalama Log_Fiyatını hesapla
        ortalama_log_fiyat = df[(df['Marka'] == marka) & (df['Seri'] == seri)]['Log_Fiyat'].mean()
        
        # Sözlüğe ekle
        sozluk[marka][seri] = ortalama_log_fiyat

# 4. JSON Dosyası Olarak Kaydet
dosya_adi = 'seri_sozlugu.json'
with open(dosya_adi, 'w', encoding='utf-8') as f:
    json.dump(sozluk, f, ensure_ascii=False, indent=4)

print(f"✅ BAŞARILI! '{dosya_adi}' oluşturuldu.")
print("Artık app.py dosyasında bu sözlüğü kullanabilirsiniz.")