import pandas as pd
import numpy as np

# 1. Dosyayı Okuma (Vitesleri doldurduğumuz dosya)
try:
    print("Dosya okunuyor...")
    df = pd.read_csv('new_gear_filled.csv', sep=';')
except FileNotFoundError:
    print("HATA: 'new_gear_filled.csv' bulunamadı.")
    exit()

# 2. Yakıt Tespit Fonksiyonu
def detect_fuel(row):
    # Eğer Yakıt zaten doluysa ve 'Bilinmiyor' değilse dokunma
    current_fuel = str(row['Yakıt']).lower()
    if pd.notna(row['Yakıt']) and current_fuel != 'nan' and current_fuel != 'bilinmiyor':
        return row['Yakıt']
    
    # Model isminden ipucu arama
    model_name = str(row['Model']).lower()
    
    # --- DİZEL İPUÇLARI ---
    diesel_keywords = ['tdi', 'cdti', 'dci', 'tdci', 'crdi', 'hdi', 'bluehdi', 
                       'multijet', 'jtd', 'd-4d', 'cdi', 'diesel', 'dizel']
    
    if any(keyword in model_name for keyword in diesel_keywords):
        return 'Dizel'
    
    # --- BENZİN İPUÇLARI ---
    gasoline_keywords = ['tsi', 'tfsi', 'fsi', 'gdi', 'tce', 'vtec', 'vti', 
                         'ecoboost', 'puretech', 'benzin', 'ls', 'turbo']
    
    if any(keyword in model_name for keyword in gasoline_keywords):
        return 'Benzin'
    
    # --- HİBRİT / ELEKTRİK ---
    if 'hybrid' in model_name or 'hibrit' in model_name:
        return 'Hibrit'
    
    if 'electric' in model_name or 'elektrik' in model_name or ' ev ' in model_name:
        return 'Elektrik'

    # Hiçbir ipucu yoksa 'Bilinmiyor' olarak kalır (veya istersen 'Benzin' varsayabiliriz)
    return 'Bilinmiyor'

# 3. Fonksiyonu Uygulama
print(f"İşlem öncesi 'Bilinmiyor' veya boş Yakıt sayısı: {len(df[(df['Yakıt'] == 'Bilinmiyor') | (df['Yakıt'].isna())])}")

df['Yakıt'] = df.apply(detect_fuel, axis=1)

# Hâlâ 'Bilinmiyor' kalan varsa, onları "Benzin" olarak doldurmak (Genelde eski modeller benzindir) 
# veya en çok geçen yakıt türüyle (Mode) doldurmak mantıklıdır.
# Burada en çok tekrar eden değerle (Mode) dolduruyoruz:
en_cok_gecen_yakit = df['Yakıt'].mode()[0]
df['Yakıt'] = df['Yakıt'].replace('Bilinmiyor', en_cok_gecen_yakit)

print(f"İşlem sonrası boş Yakıt sayısı: {len(df[(df['Yakıt'] == 'Bilinmiyor') | (df['Yakıt'].isna())])}")

# 4. Kaydetme
output_filename = 'new_fuel_filled.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! Yakıt türleri tahmin edildi ve '{output_filename}' kaydedildi.")
print("-" * 30)
print(df[['Model', 'Yakıt']].sample(10))