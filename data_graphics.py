import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Dosyayı Yükle
# (Henüz 'Fiyat' sütunu silinmemiş olan encoded dosyayı kullanıyoruz)
try:
    df = pd.read_csv('final_encoded_data.csv', sep=';')
except FileNotFoundError:
    print("HATA: 'final_encoded_data.csv' dosyası bulunamadı.")
    exit()

# 2. Tekrar Eden Verileri Temizle
df.drop_duplicates(inplace=True)

# 3. Görselleştirme için 'Marka' İsimlerini Geri Getirme
# (One-Hot Encoding yapıldığı için markalar 'Marka_Audi', 'Marka_BMW' gibi sütunlarda duruyor.
# Bunları tek bir sütunda toplayıp grafik çizdirmemiz lazım.)
marka_cols = [col for col in df.columns if col.startswith('Marka_')]
# Hangi sütun 1 ise (True ise) o sütunun ismini alıp 'Marka_' kısmını siliyoruz.
df['Marka_Label'] = df[marka_cols].idxmax(axis=1).apply(lambda x: x.replace('Marka_', ''))

# 4. Grafikleri Oluşturma
plt.figure(figsize=(20, 15))

# Grafik 1: Fiyat Dağılımı (Orijinal)
plt.subplot(3, 2, 1)
sns.histplot(df['Fiyat'], kde=True, bins=30, color='blue')
plt.title('Fiyat Dağılımı (Orijinal - Sağa Çarpık)')
plt.xlabel('Fiyat (TL)')
plt.ylabel('Frekans')

# Grafik 2: Log_Fiyat Dağılımı (Hedeflediğimiz)
plt.subplot(3, 2, 2)
sns.histplot(df['Log_Fiyat'], kde=True, bins=30, color='green')
plt.title('Log_Fiyat Dağılımı (Normal Dağılıma Daha Yakın)')
plt.xlabel('Log_Fiyat')
plt.ylabel('Frekans')

# Grafik 3: Korelasyon Haritası (Fiyatı En Çok Etkileyenler)
plt.subplot(3, 2, 3)
# Marka label'ı sayısal olmadığı için çıkarıyoruz
corr = df.drop(columns=['Marka_Label']).corr()
# Log_Fiyat ile en yüksek korelasyonu olan 10 özelliği seç
cols = corr.nlargest(10, 'Log_Fiyat')['Log_Fiyat'].index
cm = np.corrcoef(df[cols].values.T)
sns.set(font_scale=1.0)
sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', 
            annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values, cmap='coolwarm')
plt.title('Log_Fiyat ile En Yüksek Korelasyonlu Özellikler')

# Grafik 4: Yıl vs Log_Fiyat
plt.subplot(3, 2, 4)
sns.scatterplot(x='Yıl', y='Log_Fiyat', data=df, alpha=0.5, color='purple')
plt.title('Yıl ve Fiyat İlişkisi')
plt.xlabel('Yıl')
plt.ylabel('Log_Fiyat')

# Grafik 5: Kilometre vs Log_Fiyat
plt.subplot(3, 2, 5)
sns.scatterplot(x='Kilometre', y='Log_Fiyat', data=df, alpha=0.5, color='orange')
plt.title('Kilometre ve Fiyat İlişkisi')
plt.xlabel('Kilometre')
plt.ylabel('Log_Fiyat')

# Grafik 6: Markalara Göre Fiyatlar (Boxplot)
plt.subplot(3, 2, 6)
# Markaları medyan fiyata göre sıralayalım ki grafik düzgün dursun
sorted_idx = df.groupby('Marka_Label')['Log_Fiyat'].median().sort_values().index
sns.boxplot(x='Marka_Label', y='Log_Fiyat', data=df, order=sorted_idx, palette='viridis')
plt.title('Markalara Göre Fiyat Dağılımı (Ucuzdan Pahalıya)')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Marka')
plt.ylabel('Log_Fiyat')

plt.tight_layout()
plt.show() # Grafiği ekrana basar
# plt.savefig('analiz_grafikleri.png') # İsterseniz dosyaya kaydeder