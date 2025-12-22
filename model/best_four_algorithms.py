import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
import time

# 1. Veriyi Yükle
try:
    df = pd.read_csv('final_encoded_data.csv', sep=';')
except FileNotFoundError:
    print("HATA: Dosya bulunamadı. Lütfen dosya adını kontrol edin.")
    exit()

# 2. Temizlik ve Özellik Mühendisliği (Performansı artıran kritik adım)
df.drop_duplicates(inplace=True)

# Aykırı Değer Temizliği (Fiyatı aşırı uçuk olan %5'lik kısmı atıyoruz)
Q1 = df['Log_Fiyat'].quantile(0.05)
Q3 = df['Log_Fiyat'].quantile(0.95)
df = df[(df['Log_Fiyat'] >= Q1) & (df['Log_Fiyat'] <= Q3)]

# Yeni Özellikler Üretme
current_year = 2025
df['Yas'] = current_year - df['Yıl']
# Yıllık ortalama yapılan kilometre (Sıfıra bölünme hatası olmasın diye +1 ekliyoruz)
df['Yillik_Km'] = df['Kilometre'] / (df['Yas'] + 1)

# Hedef ve Özellikleri Belirle
# 'Fiyat' (Data Leakage), 'Log_Fiyat' (Hedef) ve 'Yıl' (Yerine 'Yas' geldi) sütunlarını çıkarıyoruz.
X = df.drop(columns=['Fiyat', 'Log_Fiyat', 'Yıl']) 
y = df['Log_Fiyat']

# 80-20 Eğitim/Test Bölmesi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Yarışacak Modelleri Tanımla
models = {
    "Linear Regression (Ridge)": Ridge(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    "Extra Trees": ExtraTreesRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    "HistGradientBoosting (XGBoost Alt.)": HistGradientBoostingRegressor(random_state=42)
}

# 4. Döngü ile Çalıştır ve Sonuçları Yazdır
print("\n" + "="*85)
print(f"{'MODEL ADI':<35} | {'R2 SKOR':<10} | {'ORT. HATA':<15} | {'YÜZDE HATA':<10}")
print("="*85)

for name, model in models.items():
    start_time = time.time()
    
    # Modeli Eğit
    model.fit(X_train, y_train)
    
    # Tahmin Et (Logaritmik sonuç döner)
    y_pred_log = model.predict(X_test)
    
    # Logaritmadan Gerçek Fiyata Dönüştür
    y_pred_real = np.exp(y_pred_log)
    y_test_real = np.exp(y_test)
    
    # Performans Ölç
    r2 = r2_score(y_test_real, y_pred_real)
    mae = mean_absolute_error(y_test_real, y_pred_real)
    mape = mean_absolute_percentage_error(y_test_real, y_pred_real)
    
    print(f"{name:<35} | {r2:<10.4f} | {mae:<15,.0f} TL | %{mape*100:<9.2f}")

print("="*85)