import pandas as pd
import numpy as np

# 1. Dosyayı Okuma (Önceki km temizlenmiş dosyanın elinde olduğunu varsayıyorum)
try:
    print("Dosya okunuyor...")
    # new_km_cleaned_no_zero.csv veya new_motor_cleaned.csv (hangisi en son elindeyse)
    df = pd.read_csv('new_motor_cleaned.csv', sep=';') 
except FileNotFoundError:
    # Eğer dosya yoksa sıfırdan oluşturma zincirini buraya eklemek gerekebilir
    print("HATA: 'new_motor_cleaned.csv' bulunamadı. Lütfen önceki adımları tamamla.")
    exit()

# 2. Mantıksal Sınırları Belirleme
# IQR yerine "Domain Bilgisi" (Araba bilgisi) kullanıyoruz.
ALT_SINIR_CC = 800   # 0.8 Litre altı pek olmaz (Motorsiklet değilse)
UST_SINIR_CC = 6500  # 6.5 Litre üstü çok nadirdir (Genelde hata veya kamyon verisidir)

print(f"Mantıksal Filtre: {ALT_SINIR_CC} cc ile {UST_SINIR_CC} cc arası araçlar korunacak.")

# 3. Temizlik İşlemi
initial_count = len(df)

# Önce boş (NaN) olanları temizle
df = df.dropna(subset=['Motor Hacmi'])
nan_dropped = initial_count - len(df)

# Sınır dışı olanları temizle
df_clean = df[(df['Motor Hacmi'] >= ALT_SINIR_CC) & (df['Motor Hacmi'] <= UST_SINIR_CC)]

outliers_dropped = len(df) - len(df_clean) - nan_dropped

# 4. İstatistikler
print("-" * 30)
print(f"Boş (NaN) olduğu için silinen: {nan_dropped}")
print(f"Mantıksız ({ALT_SINIR_CC}-{UST_SINIR_CC} dışı) olduğu için silinen: {outliers_dropped}")
print(f"Toplam Kalan Araç Sayısı: {len(df_clean)}")

# Lüks araç kontrolü (Silinmediğini teyit etmek için)
print("\n--- Korunan Yüksek Motorlu Araçlar (Örnek) ---")
print(df_clean[df_clean['Motor Hacmi'] > 2000][['Marka', 'Model', 'Motor Hacmi']].head())

# 5. Kaydetme
output_filename = 'new_motor_final_luxury.csv'
df_clean.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')
print(f"\nDosya kaydedildi: {output_filename}")