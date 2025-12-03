import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

# 1. Veriyi Yükle
print("Veri yükleniyor...")
df = pd.read_csv('final_encoded_data.csv', sep=';')
df.drop_duplicates(inplace=True)

# 2. Temizlik ve Özellik Mühendisliği (Web sitesinde de aynısı yapılmalı!)
# Aykırı Değer Temizliği
Q1 = df['Log_Fiyat'].quantile(0.05)
Q3 = df['Log_Fiyat'].quantile(0.95)
df = df[(df['Log_Fiyat'] >= Q1) & (df['Log_Fiyat'] <= Q3)]

# Yeni Özellikler
current_year = 2025
df['Yas'] = current_year - df['Yıl']
df['Yillik_Km'] = df['Kilometre'] / (df['Yas'] + 1)

# Eğitim Verisini Hazırla
# Yıl'ı çıkarıyoruz çünkü yerine 'Yas' geldi.
X = df.drop(columns=['Fiyat', 'Log_Fiyat', 'Yıl'])
y = df['Log_Fiyat']

# 3. Random Forest Eğit ve Kaydet
print("Random Forest modeli eğitiliyor (Biraz sürebilir)...")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X, y)
joblib.dump(rf_model, 'random_forest_model.pkl')
print("✅ random_forest_model.pkl kaydedildi.")

# 4. HistGradientBoosting Eğit ve Kaydet
print("HistGradientBoosting modeli eğitiliyor...")
hgb_model = HistGradientBoostingRegressor(random_state=42)
hgb_model.fit(X, y)
joblib.dump(hgb_model, 'hist_gradient_boosting_model.pkl')
print("✅ hist_gradient_boosting_model.pkl kaydedildi.")

print("\nİşlem Tamam! Modeller web entegrasyonuna hazır.")