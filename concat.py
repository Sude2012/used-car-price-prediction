import pandas as pd

# 'sep=';'' parametresini ekliyoruz çünkü Excel (TR) noktalı virgül kullanır.
# Ayrıca Türkçe karakter sorunu yaşamamak için encoding parametresi de ekledim.

try:
    df1 = pd.read_csv('ARABAM_VERI_SETI_EXCEL_UYUMLU kopyası.csv', sep=';', encoding='utf-8-sig')
    # İkinci dosyanın adı farklıysa burayı güncellemeyi unutmayın, 
    # varsayalım ki o da aynı formatta:
    df2 = pd.read_csv('arkadasin_verisi.csv', sep=';', encoding='utf-8-sig') 

    # Birleştirme
    birlesmis_df = pd.concat([df1, df2], ignore_index=True)

    # Kaydetme (Excel uyumlu olması için yine sep=';' ile kaydediyoruz)
    birlesmis_df.to_csv('yeni_birlesmis_dosya.csv', index=False, sep=';', encoding='utf-8-sig')

    print("İşlem başarıyla tamamlandı!")

except Exception as e:
    print(f"Hata oluştu: {e}")