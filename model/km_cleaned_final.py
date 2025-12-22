import pandas as pd
import numpy as np

# 1. Dosyayı Okuma
# new_price_final.csv dosyasını okuyoruz (Fiyatı temizlenmiş dosya)
try:
    print("Dosya okunuyor...")
    df = pd.read_csv('new_price_final.csv', sep=';')
except FileNotFoundError:
    print("HATA: 'new_price_final.csv' dosyası bulunamadı. Lütfen önceki adımları çalıştırdığınızdan emin olun.")
    exit()

# 2. Kilometre Temizleme Fonksiyonu
def clean_km(x):
    if isinstance(x, str):
        # ' km' yi sil, noktayı sil, boşlukları temizle
        return x.replace(' km', '').replace('.', '').strip()
    return x

# 3. Temizliği Uygulama
print("Kilometre sütunu temizleniyor...")
df['Kilometre'] = df['Kilometre'].apply(clean_km)

# Sayısal tipe çevirme (Hatalı veri varsa NaN yapar)
df['Kilometre'] = pd.to_numeric(df['Kilometre'], errors='coerce')

# 4. 0 km Araçları Silme
initial_count = len(df)
# Sadece kilometresi 0'dan büyük olanları alıyoruz
df = df[df['Kilometre'] > 0]
deleted_count = initial_count - len(df)

print(f"0 km olan {deleted_count} adet araç silindi.")

# 5. Kaydetme
output_filename = 'new_km_cleaned_final.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! İşlem tamamlandı. Yeni dosya: {output_filename}")
print("-" * 30)
print(df[['Marka', 'Kilometre']].head())