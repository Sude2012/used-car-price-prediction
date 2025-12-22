import pandas as pd
import numpy as np
import re

# 1. Dosyayı Okuma
try:
    # Yakıtları ilk doldurduğumuz dosya
    df = pd.read_csv('new_fuel_filled.csv', sep=';') 
except FileNotFoundError:
    # Eğer dosya yoksa, kullanıcının yüklediği corrected dosyadan devam etme senaryosu (kodun çalışması için)
    try:
        df = pd.read_csv('new_fuel_corrected.csv', sep=';')
    except:
        print("HATA: Dosya bulunamadı.")
        exit()

# --- MEVCUT YAKIT DÜZELTME İŞLEMLERİ ---
def correct_fuel_type(val):
    val = str(val).lower().strip()
    if 'dizel' in val or 'diesel' in val: return 'Dizel'
    if 'benzin' in val or 'gasoline' in val: return 'Benzin'
    if 'lpg' in val: return 'LPG' 
    if 'hibrit' in val or 'hybrid' in val: return 'Hibrit'
    if 'elektrik' in val or 'electric' in val: return 'Elektrik'
    if 'lt' in val or any(char.isdigit() for char in val): return np.nan
    return val.capitalize()

print("Yakıt sütunu temizleniyor...")
df['Yakıt'] = df['Yakıt'].apply(correct_fuel_type)

def re_detect_fuel(row):
    if pd.notna(row['Yakıt']): return row['Yakıt']
    model = str(row['Model']).lower()
    if any(k in model for k in ['tdi','cdti','dci','tdci','crdi','hdi','multijet']): return 'Dizel'
    if any(k in model for k in ['tsi','tfsi','fsi','gdi','vtec','benzin','turbo']): return 'Benzin'
    if 'hybrid' in model: return 'Hibrit'
    return 'Benzin'

print("Eksik yakıt türleri Model ismine göre tamamlanıyor...")
df['Yakıt'] = df.apply(re_detect_fuel, axis=1)

# --- YENİ İSTEKLER ---

# 1. Model Kolonunu Silme (Yakıt işleminden sonra)
print("Model sütunu siliniyor...")
if 'Model' in df.columns:
    df.drop(columns=['Model'], inplace=True)

# 2. Renk Sütunundaki Boşlukları Mod ile Doldurma
print("Renk sütunundaki boşluklar mod değeri ile dolduruluyor...")
renk_mode = df['Renk'].mode()[0]
df['Renk'].fillna(renk_mode, inplace=True)

# 3. Boya ve Değişen Sütunlarını Ayrıştırma
print("Boya ve Değişen bilgileri ayrıştırılıyor...")

def parse_damage(val):
    val = str(val).lower().strip()
    
    # Orjinal araçlar
    if val == 'tamamı orjinal' or val == 'orjinal':
        return 0, 0
    
    # Belirtilmemiş veya boş ise NaN döndür (sonra mod ile dolduracağız)
    if val == 'belirtilmemiş' or val == 'nan':
        return np.nan, np.nan
        
    boya = 0
    degisen = 0
    
    # Regex ile sayıları çekme
    # Örn: "2 değişen, 3 boyalı"
    degisen_match = re.search(r'(\d+)\s*değişen', val)
    boya_match = re.search(r'(\d+)\s*boyalı', val)
    
    if degisen_match:
        degisen = int(degisen_match.group(1))
    
    if boya_match:
        boya = int(boya_match.group(1))
        
    return boya, degisen

# Fonksiyonu uygula
parsed_data = df['Boya-değişen'].apply(parse_damage)

# Yeni sütunları oluştur
df['Boya'] = parsed_data.apply(lambda x: x[0])
df['Değişen'] = parsed_data.apply(lambda x: x[1])

# NaN (Belirtilmemiş) değerleri Mod (En çok tekrar eden, muhtemelen 0) ile doldur
boya_mode = df['Boya'].mode()[0]
degisen_mode = df['Değişen'].mode()[0]

df['Boya'].fillna(boya_mode, inplace=True)
df['Değişen'].fillna(degisen_mode, inplace=True)

# Sayısal tipe çevir
df['Boya'] = df['Boya'].astype(int)
df['Değişen'] = df['Değişen'].astype(int)

# Eski sütunu kaldır
if 'Boya-değişen' in df.columns:
    df.drop(columns=['Boya-değişen'], inplace=True)

# 4. Kaydetme
output_filename = 'new_fuel_final_processed.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print(f"BAŞARILI! Tüm işlemler tamamlandı. Yeni dosya: {output_filename}")
print(df.head())