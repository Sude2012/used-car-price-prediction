import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Veriyi Oku
print("Dosya okunuyor...")
df = pd.read_csv('new_price.csv', sep=';')

# 2. Aykırı Değer Temizliği (Önceki adımda anlaştığımız işlem)
# 100 Milyon TL üzerindeki bariz hatalı veriyi siliyoruz.
df = df[df['Fiyat'] < 100000000]

# 3. Logaritmik Dönüşüm (Model Başarısı İçin Kritik Adım)
# Fiyat değerlerinin logaritmasını alıp yeni bir kolona yazıyoruz.
# np.log1p fonksiyonu, log(1 + x) işlemini yapar (0 değerleri için güvenlidir).
df['Log_Fiyat'] = np.log1p(df['Fiyat'])

# 4. Final Dosyasını Kaydetme
output_filename = 'new_price_final.csv'
df.to_csv(output_filename, index=False, sep=';', encoding='utf-8-sig')
print(f"BAŞARILI! Logaritmik dönüşüm yapıldı ve '{output_filename}' oluşturuldu.")

# 5. Görselleştirme (Farkı Görmek İçin)
plt.figure(figsize=(14, 6))

# Grafik 1: Orijinal Fiyat (Çarpık Dağılım)
plt.subplot(1, 2, 1)
sns.histplot(df['Fiyat'], kde=True, bins=30, color='red')
plt.title('Orijinal Fiyat Dağılımı (Model İçin Zor)')
plt.xlabel('Fiyat (TL)')
plt.ticklabel_format(style='plain', axis='x')

# Grafik 2: Log Fiyat (Normal Dağılım - Çan Eğrisi)
plt.subplot(1, 2, 2)
sns.histplot(df['Log_Fiyat'], kde=True, bins=30, color='green')
plt.title('Logaritmik Fiyat Dağılımı (Model İçin İdeal)')
plt.xlabel('Log(Fiyat)')

plt.tight_layout()
plt.show()

# İstatistiksel Kontrol
print("\n--- Dönüşüm Sonrası Kontrol ---")
print(df[['Fiyat', 'Log_Fiyat']].head())
print(f"\nOrijinal Veri Çarpıklığı (Skew): {df['Fiyat'].skew():.2f}")
print(f"Log Dönüşümlü Veri Çarpıklığı (Skew): {df['Log_Fiyat'].skew():.2f} (0'a ne kadar yakınsa o kadar iyi)")