import pandas as pd
import numpy as np

# 1. Dosyayı Okuma (En son km temizliği yaptığımız dosya)
try:
    print("Dosya okunuyor...")
    df = pd.read_csv('new_km_cleaned_final.csv', sep=';')
except FileNotFoundError:
    print("HATA: Dosya bulunamadı. Lütfen dosya ismini kontrol edin.")
    exit()

# 2. Motor Hacmi Temizleme Fonksiyonu
def clean_motor_hacmi(x):
    if pd.isna(x) or x == '-':
        return np.nan
    
    if isinstance(x, str):
        # Küçük harfe çevir ve gereksiz ekleri temizle
        x = x.lower()
        x = x.replace(' cc', '').replace(' cm3', '').replace("' e kadar", "").replace(' e kadar', '')
        x = x.replace('.', '') # Binlik ayracı varsa kaldır
        x = x.strip()
        
        # ARALIK DEĞERLERİ (Örn: "1201 - 1400")
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
print("Motor Hacmi temizleniyor...")
df['Motor Hacmi'] = df['Motor Hacmi'].apply(clean_motor_hacmi)

# 4. Kaydetme
output_filename = 'new_motor_cleaned.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! Motor Hacmi temizlendi. Yeni dosya: {output_filename}")
print("-" * 40)
print("Örnek Veriler:")
print(df[['Marka', 'Motor Hacmi']].head(10))