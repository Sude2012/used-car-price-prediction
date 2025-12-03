import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

# 1. Veriyi Yükle
df = pd.read_csv('final_encoded_data.csv', sep=';')
df.drop_duplicates(inplace=True)

# --- ADIM 1: AYKIRI DEĞER TEMİZLİĞİ (IQR Yöntemi) ---
# Fiyatı aşırı düşük veya aşırı yüksek olan %5'lik kısmı atıyoruz
# Çünkü bunlar muhtemelen hatalı veri veya çok özel durumlar.
Q1 = df['Log_Fiyat'].quantile(0.05)
Q3 = df['Log_Fiyat'].quantile(0.95)
df = df[(df['Log_Fiyat'] >= Q1) & (df['Log_Fiyat'] <= Q3)]

print(f"Aykırı değerler temizlendi. Yeni veri sayısı: {len(df)}")

# --- ADIM 2: YENİ ÖZELLİK EKLEME (Feature Engineering) ---
# Mevcut yıl 2025 kabul edelim (veya verinin çekildiği yıl)
current_year = 2025
df['Yas'] = current_year - df['Yıl']
# Sıfıra bölünme hatasını önlemek için +1 ekliyoruz
df['Yillik_Km'] = df['Kilometre'] / (df['Yas'] + 1) 

# --- ADIM 3: VERİYİ HAZIRLA ---
X = df.drop(columns=['Fiyat', 'Log_Fiyat']) # Yıl sütununu tutabiliriz veya silebiliriz, Yas geldiği için.
y = df['Log_Fiyat']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- ADIM 4: XGBOOST ve GRID SEARCH (En iyi ayarları bulma) ---
print("En iyi parametreler aranıyor... (Bu işlem biraz sürebilir)")

xgb = XGBRegressor(objective='reg:squarederror', random_state=42)

# Denenecek ayarlar
param_grid = {
    'n_estimators': [100, 500, 1000],   # Ağaç sayısı
    'learning_rate': [0.01, 0.05, 0.1], # Öğrenme hızı (düşük olması genelde iyidir)
    'max_depth': [3, 5, 7],             # Ağaç derinliği
    'subsample': [0.7, 0.8, 0.9]        # Her ağaçta verinin yüzde kaçını kullansın
}

grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, 
                           cv=3, n_jobs=-1, verbose=1, scoring='neg_mean_absolute_percentage_error')

grid_search.fit(X_train, y_train)

print(f"En iyi parametreler: {grid_search.best_params_}")

# En iyi modeli al
best_model = grid_search.best_estimator_

# --- ADIM 5: TAHMİN VE SONUÇ ---
y_pred_log = best_model.predict(X_test)

# Geri dönüştürme
y_pred_real = np.exp(y_pred_log)
y_test_real = np.exp(y_test)

# Skorlar
mae = mean_absolute_error(y_test_real, y_pred_real)
mape = mean_absolute_percentage_error(y_test_real, y_pred_real)
r2 = r2_score(y_test_real, y_pred_real)

print("-" * 30)
print(f"YENİ MODEL (XGBoost Optimized) SONUÇLARI:")
print(f"R2 Score: {r2:.4f}")
print(f"MAE: {mae:,.0f} TL")
print(f"MAPE: %{mape*100:.2f}")
print("-" * 30)