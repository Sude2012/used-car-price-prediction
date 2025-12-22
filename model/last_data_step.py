import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder

# 1. Dosyayı Okuma
try:
    df = pd.read_csv('new_fuel_corrected.csv', sep=';')
except FileNotFoundError:
    print("HATA: Dosya bulunamadı.")
    exit()

# ----------------- TEMİZLİK ADIMLARI -----------------

# 1. Model Sütununu Silme
if 'Model' in df.columns:
    df.drop(columns=['Model'], inplace=True)

# 2. Boya-Değişen Ayrıştırma
def parse_damage(val):
    val = str(val).lower().strip()
    if val in ['tamamı orjinal', 'orjinal']:
        return 0, 0
    if val in ['belirtilmemiş', 'nan']:
        return np.nan, np.nan
        
    boya = 0
    degisen = 0
    
    degisen_match = re.search(r'(\d+)\s*değişen', val)
    boya_match = re.search(r'(\d+)\s*boyalı', val)
    
    if degisen_match: degisen = int(degisen_match.group(1))
    if boya_match: boya = int(boya_match.group(1))
        
    return boya, degisen

if 'Boya-değişen' in df.columns:
    print("Boya ve Değişen bilgileri ayrıştırılıyor...")
    parsed = df['Boya-değişen'].apply(parse_damage)
    df['Boya'] = parsed.apply(lambda x: x[0])
    df['Değişen'] = parsed.apply(lambda x: x[1])
    df.drop(columns=['Boya-değişen'], inplace=True)

# 3. Boş Değerleri Doldurma
print("Boş değerler mod ile dolduruluyor...")
for col in df.columns:
    if df[col].isnull().any():
        mode_val = df[col].mode()[0]
        df[col].fillna(mode_val, inplace=True)

# Sayısal dönüşüm
if 'Boya' in df.columns: df['Boya'] = df['Boya'].astype(int)
if 'Değişen' in df.columns: df['Değişen'] = df['Değişen'].astype(int)

# ----------------- SON RÜTUŞLAR (YENİ EKLENENLER) -----------------

# 4. TEKRAR EDEN VERİLERİ SİLME
initial_len = len(df)
df.drop_duplicates(inplace=True)
final_len = len(df)
print(f"Tekrar eden {initial_len - final_len} satır silindi.")

# 5. HEDEF DEĞİŞKEN SEÇİMİ (LOG_FIYAT)
# Normal 'Fiyat'ı siliyoruz ki model eğitim sırasında bunu görüp cevabı ezberlemesin (Leakage).
if 'Fiyat' in df.columns and 'Log_Fiyat' in df.columns:
    print("Model eğitimi için 'Log_Fiyat' seçildi. Normal 'Fiyat' sütunu siliniyor...")
    df.drop(columns=['Fiyat'], inplace=True)

# ----------------- ENCODING ADIMLARI -----------------

# A. Label Encoding
label_cols = ['Vites', 'Yakıt', 'Renk', 'Kasa Tipi']
le = LabelEncoder()
print("Label Encoding uygulanıyor...")
for col in label_cols:
    if col in df.columns:
        df[col] = le.fit_transform(df[col].astype(str))

# B. Target Encoding (Seri)
# DİKKAT: Artık hedefimiz Log_Fiyat olduğu için ortalamayı ona göre alıyoruz!
if 'Seri' in df.columns and 'Log_Fiyat' in df.columns:
    print("Target Encoding (Seri -> Log_Fiyat ortalamasına göre) uygulanıyor...")
    target_means = df.groupby('Seri')['Log_Fiyat'].transform('mean')
    df['Seri'] = target_means

# C. One-Hot Encoding (Marka)
if 'Marka' in df.columns:
    print("One-Hot Encoding (Marka) uygulanıyor...")
    df = pd.get_dummies(df, columns=['Marka'], prefix='Marka')

# D. Boolean -> Int Dönüşümü
print("True/False değerleri 1/0 formatına çevriliyor...")
bool_cols = df.select_dtypes(include=['bool']).columns
df[bool_cols] = df[bool_cols].astype(int)

# ----------------- KAYDETME -----------------
output_filename = 'final_model_ready_log.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')

print("-" * 30)
print(f"HAZIRLIK TAMAMLANDI! Dosya: {output_filename}")
print(f"Kalan Satır Sayısı: {len(df)}")
print("-" * 30)
print(df.head())