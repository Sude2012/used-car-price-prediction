import pandas as pd
import numpy as np

# 1. Dosyayı Okuma (En son HP temizlenmiş dosya)
try:
    print("Dosya okunuyor...")
    df = pd.read_csv('new_hp_final.csv', sep=';')
except FileNotFoundError:
    print("HATA: Dosya bulunamadı. Lütfen dosya ismini kontrol edin.")
    exit()

# 2. Vites Doldurma Fonksiyonu
def fill_gear(row):
    # Eğer Vites zaten doluysa (NaN değilse), olduğu gibi bırak
    if pd.notna(row['Vites']):
        return row['Vites']
    
    # Yıl bilgisine göre mantıksal doldurma
    yil = row['Yıl']
    
    if yil <= 2005:
        return 'Düz'
    elif 2005 < yil <= 2012:  # 2006 ile 2012 arası (dahil)
        return 'Yarı Otomatik'
    else:  # 2012'den büyükse (2013 ve üzeri)
        return 'Otomatik'

# 3. Fonksiyonu Uygulama
print(f"İşlem öncesi boş Vites sayısı: {df['Vites'].isnull().sum()}")

# axis=1 parametresi, satır satır işlem yapmamızı sağlar
df['Vites'] = df.apply(fill_gear, axis=1)

print(f"İşlem sonrası boş Vites sayısı: {df['Vites'].isnull().sum()}")

# 4. Kaydetme
output_filename = 'new_gear_filled.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! Dosya kaydedildi: {output_filename}")
print("-" * 30)
print(df[['Yıl', 'Vites']].sample(10)) # Rastgele 10 örneği kontrol et