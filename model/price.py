import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Dosyayı Oku
df = pd.read_csv('new_column.csv', sep=';')

# 2. Fiyat Kolonunu Temizleme Fonksiyonu
def clean_price(value):
    if isinstance(value, str):
        # ' TL' sil, '.' sil, boşlukları sil
        return value.replace(' TL', '').replace('.', '').strip()
    return value

# Temizliği uygula
df['Fiyat'] = df['Fiyat'].apply(clean_price)

# Sayısal tipe çevir (Hatalı veri varsa NaN yapar)
df['Fiyat'] = pd.to_numeric(df['Fiyat'], errors='coerce')

# 3. Boş Verileri Temizleme
# Fiyatı boş (NaN) olan satırları sil
df = df.dropna(subset=['Fiyat'])

# Tamamı boş olan sütunları sil
df = df.dropna(axis=1, how='all')

# 4. Yeni Dosyayı Kaydet
df.to_csv('new_price.csv', index=False, sep=';', encoding='utf-8-sig')
print("İşlem tamam! 'new_price.csv' oluşturuldu.")

# 5. Grafikleri Çizdir
plt.figure(figsize=(14, 6))

# Histogram
plt.subplot(1, 2, 1)
sns.histplot(df['Fiyat'], kde=True, bins=30)
plt.title('Fiyat Dağılımı (Histogram)')
plt.xlabel('Fiyat (TL)')
plt.ylabel('Adet')
plt.ticklabel_format(style='plain', axis='x')

# Boxplot
plt.subplot(1, 2, 2)
sns.boxplot(x=df['Fiyat'])
plt.title('Fiyat Dağılımı (Boxplot)')
plt.xlabel('Fiyat (TL)')
plt.ticklabel_format(style='plain', axis='x')

plt.tight_layout()
plt.show()