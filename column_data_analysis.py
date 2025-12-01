import pandas as pd

# 1. Dosyayı Okuma
# Dosyanız noktalı virgül (;) ile ayrıldığı için sep=';' kullanıyoruz.
giris_dosyasi = 'new_concat_data.csv' 
df = pd.read_csv(giris_dosyasi, sep=';')

print(f"{giris_dosyasi} okunuyor...")

# 2. İstenmeyen Kolonları Silme
# Listeye 'İlan Tarihi'ni de ekledik.
silinecek_kolonlar = ['Araç Durumu', 'Link', 'İlan Tarihi']

# errors='ignore' parametresi, eğer kolon zaten yoksa hata vermesini engeller.
df = df.drop(columns=silinecek_kolonlar, errors='ignore')

print(f"Şu kolonlar başarıyla silindi: {silinecek_kolonlar}")

# 3. Yeni Dosyayı Kaydetme
cikis_dosyasi = 'new_column.csv'
df.to_csv(cikis_dosyasi, index=False, sep=';', encoding='utf-8-sig')

print(f"İşlem tamam! Yeni dosya '{cikis_dosyasi}' adıyla oluşturuldu.")

# Kontrol için ilk 5 satırı ve kalan kolonları yazdıralım
print("\n--- Yeni Dosya İçeriği (İlk 5 Satır) ---")
print(df.head())
print("\n--- Kalan Kolonlar ---")
print(df.columns.tolist())