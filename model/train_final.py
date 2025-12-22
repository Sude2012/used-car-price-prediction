import pandas as pd
import numpy as np
import json
import joblib
import re
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

print("🚀 ÇİFT MOTORLU Eğitim başlatılıyor...")

# 1. AYARLARI VE VERİYİ YÜKLE
try:
    with open('system_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    df = pd.read_csv('new_fuel_corrected.csv', sep=';')
    print("✅ Veri seti yüklendi.")
except FileNotFoundError:
    print("HATA: Dosyalar bulunamadı.")
    exit()

# --- SÜTUN İSİMLERİNİ STANDARTLAŞTIR ---
df.columns = df.columns.str.strip()
for col in df.columns:
    if col.lower() == 'fiyat': df.rename(columns={col: 'Fiyat'}, inplace=True)
    elif col.lower() == 'boya': df.rename(columns={col: 'Boya'}, inplace=True)
    elif col.lower() == 'değişen': df.rename(columns={col: 'Değişen'}, inplace=True)
    elif col.lower() == 'vites': df.rename(columns={col: 'Vites'}, inplace=True)
    elif col.lower() == 'yakıt': df.rename(columns={col: 'Yakıt'}, inplace=True)
    elif col.lower() == 'marka': df.rename(columns={col: 'Marka'}, inplace=True)
    elif col.lower() == 'seri': df.rename(columns={col: 'Seri'}, inplace=True)

# Boya/Değişen Kontrolü
if 'Boya' not in df.columns or 'Değişen' not in df.columns:
    if 'Boya-değişen' in df.columns:
        def parse_damage(val):
            val = str(val).lower()
            if 'orjinal' in val: return 0, 0
            b, d = 0, 0
            import re
            m_d = re.search(r'(\d+)\s*değişen', val)
            m_b = re.search(r'(\d+)\s*boyalı', val)
            if m_d: d = int(m_d.group(1))
            if m_b: b = int(m_b.group(1))
            return b, d
        parsed = df['Boya-değişen'].apply(parse_damage)
        df['Boya'] = parsed.apply(lambda x: x[0])
        df['Değişen'] = parsed.apply(lambda x: x[1])
    else:
        if 'Boya' not in df.columns: df['Boya'] = 0
        if 'Değişen' not in df.columns: df['Değişen'] = 0

# --- ÖN İŞLEME ---
fill_cols = ['Renk', 'Boya', 'Değişen', 'Kasa Tipi', 'Vites', 'Yakıt']
for col in fill_cols:
    if col in df.columns:
        if df[col].dtype == 'object': df[col] = df[col].fillna(df[col].mode()[0])
        else: df[col] = df[col].fillna(0)

def apply_mapping(col_name, map_dict):
    if col_name not in df.columns: return 0
    return df[col_name].astype(str).map(map_dict).fillna(0)

df['Vites'] = apply_mapping('Vites', config['Vites'])
df['Yakıt'] = apply_mapping('Yakıt', config['Yakıt'])
df['Renk'] = apply_mapping('Renk', config['Renk'])
df['Kasa Tipi'] = apply_mapping('Kasa Tipi', config['Kasa Tipi'])

current_year = 2025
df['Yas'] = current_year - df['Yıl']
df['Yillik_Km'] = df['Kilometre'] / (df['Yas'] + 1)

seri_sozlugu = config['Seri_Sozlugu']
def get_seri_score(row):
    try: return seri_sozlugu[row['Marka']][row['Seri']]
    except: return 0 
df['Seri'] = df.apply(get_seri_score, axis=1)

model_cols = config['Model_Columns']
marka_cols = [col for col in model_cols if col.startswith('Marka_')]
for m_col in marka_cols:
    marka_ismi = m_col.replace('Marka_', '')
    df[m_col] = (df['Marka'] == marka_ismi).astype(int)

# --- EĞİTİM ---
for col in model_cols:
    if col not in df.columns: df[col] = 0

X = df[model_cols]
y = np.log1p(df['Fiyat'])

# 1. Random Forest Eğit
print(f"🌲 Random Forest eğitiliyor... (Satır: {len(df)})")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X, y)
joblib.dump(rf_model, 'random_forest_model.pkl')
print("✅ random_forest_model.pkl kaydedildi.")

# 2. HistGradientBoosting Eğit
print(f"🚀 HistGradientBoosting eğitiliyor...")
hgb_model = HistGradientBoostingRegressor(random_state=42, max_iter=100)
hgb_model.fit(X, y)
joblib.dump(hgb_model, 'hist_gradient_boosting_model.pkl')
print("✅ hist_gradient_boosting_model.pkl kaydedildi.")

print("🏁 İki model de hazır!")