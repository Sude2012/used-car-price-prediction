import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

# 1. Veriyi Yükle
df = pd.read_csv('final_encoded_data.csv', sep=';')
df.drop_duplicates(inplace=True)

# 2. Hedef ve Özellikleri Ayır (Log_Fiyat Hedef)
X = df.drop(columns=['Fiyat', 'Log_Fiyat'])
y = df['Log_Fiyat']

# 3. 80-20 Eğitim/Test Bölmesi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Model Kurulumu (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Tahmin
y_pred_log = model.predict(X_test)

# 6. Logaritmik Değerleri Gerçek Fiyata Çevirme
y_pred_real = np.exp(y_pred_log)
y_test_real = np.exp(y_test)

# 7. Metrikleri Hesaplama
mae = mean_absolute_error(y_test_real, y_pred_real)
mape = mean_absolute_percentage_error(y_test_real, y_pred_real)
r2 = r2_score(y_test_real, y_pred_real)

print(f"MODEL SONUÇLARI (Random Forest):")
print(f"R2 Score: {r2:.4f}")
print(f"MAE (Ortalama Hata): {mae:,.0f} TL")
print(f"MAPE (Yüzdesel Hata): %{mape*100:.2f}")

# Örnek Tahminleri Görme
results = pd.DataFrame({'Gerçek Fiyat': y_test_real, 'Tahmin': y_pred_real})
results['Fark'] = results['Gerçek Fiyat'] - results['Tahmin']
print("\nÖrnek Karşılaştırma:")
print(results.head(10))