import pandas as pd
import numpy as np

# 1. Dosyayı Okuma
try:
    # Yakıtları ilk doldurduğumuz dosya (veya elindeki en son dosya)
    df = pd.read_csv('new_fuel_filled.csv', sep=';') 
except FileNotFoundError:
    print("HATA: Dosya bulunamadı.")
    exit()

# 2. Hatalı Yakıt Verilerini (lt, sayı) Temizleme Fonksiyonu
def correct_fuel_type(val):
    val = str(val).lower().strip()
    
    # Geçerli Yakıt Türleri
    if 'dizel' in val or 'diesel' in val: return 'Dizel'
    if 'benzin' in val or 'gasoline' in val: return 'Benzin'
    if 'lpg' in val: return 'LPG' 
    if 'hibrit' in val or 'hybrid' in val: return 'Hibrit'
    if 'elektrik' in val or 'electric' in val: return 'Elektrik'
    
    # Hatalı Veriler (lt veya sayı içeriyorsa) -> NaN yap
    if 'lt' in val or any(char.isdigit() for char in val):
        return np.nan
        
    return val.capitalize()

print("Yakıt sütunu temizleniyor (lt değerleri siliniyor)...")
df['Yakıt'] = df['Yakıt'].apply(correct_fuel_type)

# 3. Silinenleri Tekrar Model İsmine Göre Doldurma
def re_detect_fuel(row):
    # Eğer yakıt doluysa dokunma
    if pd.notna(row['Yakıt']): 
        return row['Yakıt']
    
    model = str(row['Model']).lower()
    
    # Dizel İpuçları
    if any(k in model for k in ['tdi','cdti','dci','tdci','crdi','hdi','multijet']): 
        return 'Dizel'
    
    # Benzin İpuçları
    if any(k in model for k in ['tsi','tfsi','fsi','gdi','vtec','benzin','turbo']): 
        return 'Benzin'
    
    # Diğerleri
    if 'hybrid' in model: return 'Hibrit'
    
    # Hiçbir ipucu yoksa varsayılan olarak Benzin ata
    return 'Benzin'

print("Silinen yakıt türleri Model ismine göre yeniden tahmin ediliyor...")
df['Yakıt'] = df.apply(re_detect_fuel, axis=1)

# 4. Kaydetme
output_filename = 'new_fuel_corrected.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! Yakıt türleri düzeltildi. Yeni dosya: {output_filename}")
print(df['Yakıt'].value_counts())