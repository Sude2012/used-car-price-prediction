import pandas as pd
import numpy as np

# 1. Önceki dosyayı (Fiyat işlemleri yapılmış olanı) okuyoruz
# Eğer dosya yoksa baştan oluşturma adımlarını buraya eklemen gerekir.
# Biz varsayalım ki 'new_price_final.csv' elimizde veya hafızada.
# (Not: Ben kodumda garanti olsun diye baştan işleyerek geldim)

df = pd.read_csv('new_price_final.csv', sep=';')

# 2. Kilometre Temizleme Fonksiyonu
def clean_km(x):
    if isinstance(x, str):
        # ' km' yi sil, noktayı sil, boşlukları temizle
        return x.replace(' km', '').replace('.', '').strip()
    return x

# 3. Temizliği Uygulama
print("Kilometre kolonu temizleniyor...")
df['Kilometre'] = df['Kilometre'].apply(clean_km)

# Sayısal tipe çevirme (int64)
# errors='coerce' hatalı veri varsa (örneğin harf girilmişse) NaN yapar
df['Kilometre'] = pd.to_numeric(df['Kilometre'], errors='coerce')

# 4. Yeni Dosyayı Kaydetme
output_filename = 'new_km_cleaned.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! Kilometre temizlendi ve '{output_filename}' oluşturuldu.")
print(df[['Marka', 'Kilometre']].head())