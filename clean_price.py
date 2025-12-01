import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Veriyi Oku
df = pd.read_csv('new_price.csv', sep=';')

# 2. Seçenek A: Hatalı Veriyi Silme
# 100 Milyon TL üzerindeki araçları siliyoruz (Sadece o 635 Milyonluk hata gitsin diye)
limit_fiyat = 100000000 
df_cleaned = df[df['Fiyat'] < limit_fiyat]

# 3. Yeni Dosyayı Kaydet
df_cleaned.to_csv('new_price_cleaned.csv', index=False, sep=';', encoding='utf-8-sig')

print(f"İşlem Tamam! {len(df) - len(df_cleaned)} adet hatalı veri silindi.")
print("Temizlenmiş veri 'new_price_cleaned.csv' dosyasına kaydedildi.")

# 4. Grafikleri Çiz
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.histplot(df_cleaned['Fiyat'], kde=True, bins=30)
plt.title('Fiyat Dağılımı (Hatalı Veri Temizlendi)')
plt.ticklabel_format(style='plain', axis='x')

plt.subplot(1, 2, 2)
sns.boxplot(x=df_cleaned['Fiyat'])
plt.title('Fiyat Dağılımı (Boxplot)')
plt.ticklabel_format(style='plain', axis='x')

plt.tight_layout()
plt.show()