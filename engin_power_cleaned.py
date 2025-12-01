import pandas as pd
import numpy as np

# 1. Dosyayı Okuma (En son motor hacmi temizlenmiş dosyayı kullanıyoruz)
try:
    print("Dosya okunuyor...")
    # Elinizdeki en son dosya hangisiyse onu okuyun:
    df = pd.read_csv('new_motor_final_luxury.csv', sep=';') 
except FileNotFoundError:
    print("HATA: 'new_motor_final_luxury.csv' bulunamadı.")
    exit()

# 2. Motor Gücü Temizleme Fonksiyonu
def clean_motor_gucu(x):
    if pd.isna(x) or x == '-':
        return np.nan
    
    if isinstance(x, str):
        # Küçük harfe çevir ve gereksiz ekleri temizle
        x = x.lower()
        x = x.replace(' hp', '').replace(' beygir', '').replace(' kw', '') 
        x = x.replace('.', '').strip()
        
        # ARALIK DEĞERLERİ (Örn: "101 - 125")
        if '-' in x:
            try:
                parts = x.split('-')
                p1 = float(parts[0].strip())
                p2 = float(parts[1].strip())
                # İki değerin ortalamasını al
                return (p1 + p2) / 2
            except:
                return np.nan
        
        # NORMAL DEĞERLER
        try:
            return float(x)
        except:
            return np.nan
            
    return x

# 3. Temizliği Uygulama
print("Motor Gücü temizleniyor...")
df['Motor Gücü'] = df['Motor Gücü'].apply(clean_motor_gucu)

# 4. Boş Verileri ve Mantıksız Değerleri Silme
initial_count = len(df)

# Boş (NaN) olanları sil
df = df.dropna(subset=['Motor Gücü'])
nan_dropped = initial_count - len(df)

# Mantıksal Sınırlar (Lüks araçları koruyacak şekilde)
ALT_SINIR_HP = 40    # 40 beygir altı araba pek olmaz
UST_SINIR_HP = 1500  # 1500 beygir üstü çok çok nadirdir (Bugatti vs.)

df_clean = df[(df['Motor Gücü'] >= ALT_SINIR_HP) & (df['Motor Gücü'] <= UST_SINIR_HP)]
outliers_dropped = len(df) - len(df_clean) - nan_dropped

# 5. Kaydetme
output_filename = 'new_hp_final.csv'
df_clean.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

# 6. Raporlama
print("-" * 40)
print(f"Boş (NaN) olduğu için silinen: {nan_dropped}")
print(f"Mantıksız ({ALT_SINIR_HP}-{UST_SINIR_HP} HP dışı) olduğu için silinen: {outliers_dropped}")
print(f"Toplam Kalan Araç Sayısı: {len(df_clean)}")
print("-" * 40)
print("Örnek Veriler (Marka - Motor Gücü):")
print(df_clean[['Marka', 'Motor Gücü']].head(10))