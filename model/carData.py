import pandas as pd
import time
import random 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- AYARLAR ---
# Mevcut dosyanın tam adı
MEVCUT_DOSYA_ADI = "ARABAM_VERI_SETI_EXCEL_UYUMLU kopyası.csv" 

# Çekilecek 5 Hedef Marka
MARKALAR_LISTESI = [
    "audi", 
    "bmw", 
    "citroen", 
    "ford", 
    "mercedes-benz"
]

HEDEF_VERI_SAYISI = 160  # Marka başına çekilecek ilan sayısı
MAX_SAYFA_PER_MARKA = 10 # 160 ilan için ortalama sayfa sayısı

# --- SELENIUM KURULUMU ---
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=options)
tum_yeni_veriler = []

print(f"VERİ ÇEKME OPERASYONU BAŞLIYOR... Hedef: Marka başı {HEDEF_VERI_SAYISI} ilan.")
print(f"Çekilecek Markalar: {', '.join(MARKALAR_LISTESI)}")

# --- ANA DÖNGÜ ---
for marka in MARKALAR_LISTESI:
    print(f"\n===== {marka.upper()} TARANIYOR =====")
    
    toplanan_linkler = []
    sayfa = 1
    
    # 1. ADIM: İlan Linklerini Topla
    while len(toplanan_linkler) < HEDEF_VERI_SAYISI and sayfa <= MAX_SAYFA_PER_MARKA:
        url = f"https://www.arabam.com/ikinci-el/otomobil/{marka}?page={sayfa}"
        driver.get(url)
        time.sleep(random.uniform(2.5, 4.5))
        
        try:
            # İlan linklerini bul
            ilanlar = driver.find_elements(By.CSS_SELECTOR, "tr.listing-list-item a.listing-text-new")
            if not ilanlar:
                ilanlar = driver.find_elements(By.CSS_SELECTOR, "a.link-overlay")
            
            if not ilanlar:
                print(f"Sayfa {sayfa}'de ilan bulunamadı.")
                break
                
            for ilan in ilanlar:
                link = ilan.get_attribute("href")
                if link and link not in toplanan_linkler:
                    toplanan_linkler.append(link)
                    if len(toplanan_linkler) >= HEDEF_VERI_SAYISI:
                        break
            
            print(f"Sayfa {sayfa} bitti. Toplam bulunan link: {len(toplanan_linkler)}")
            sayfa += 1
            
        except Exception as e:
            print(f"Sayfa tarama hatası: {e}")
            break

    # 2. ADIM: Detaylara Git
    print(f"--> {marka.upper()} detayları çekiliyor... ({len(toplanan_linkler)} Adet)")
    
    for i, link in enumerate(toplanan_linkler):
        try:
            driver.get(link)
            time.sleep(random.uniform(1.5, 3)) # Engel yememek için bekleme
            
            veri = {"Link": link}
            
            # Fiyatı Al
            try:
                fiyat = driver.find_element(By.CSS_SELECTOR, "div[data-testid='product-price']").text
            except:
                try:
                    fiyat = driver.find_element(By.CSS_SELECTOR, "div.product-price").text
                except:
                    fiyat = None
            veri["Fiyat"] = fiyat

            # Özellikleri Al
            ozellikler = driver.find_elements(By.CSS_SELECTOR, "ul.w-100 li")
            if not ozellikler:
                ozellikler = driver.find_elements(By.CSS_SELECTOR, "div.property-item")

            for ozellik in ozellikler:
                text = ozellik.text
                if "\n" in text: parts = text.split("\n")
                else: parts = text.split(" ", 1)
                
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = parts[-1].strip()
                    
                    if "Marka" in key: veri["Marka"] = val
                    elif "Seri" in key: veri["Seri"] = val
                    elif "Model" in key and "Yılı" not in key: veri["Model"] = val
                    elif "Yıl" in key: veri["Yıl"] = val
                    elif "Kilometre" in key: veri["Kilometre"] = val
                    elif "Vites" in key: veri["Vites"] = val
                    elif "Yakıt" in key: veri["Yakıt"] = val
                    elif "Kasa" in key: veri["Kasa Tipi"] = val
                    elif "Renk" in key: veri["Renk"] = val
                    elif "Motor Hacmi" in key: veri["Motor Hacmi"] = val
                    elif "Motor Gücü" in key: veri["Motor Gücü"] = val
                    elif "Durumu" in key: veri["Araç Durumu"] = val
                    elif "Boya" in key or "Değişen" in key: veri["Boya-değişen"] = val
                    elif "Tarihi" in key: veri["İlan Tarihi"] = val
            
            tum_yeni_veriler.append(veri)
            
            if (i+1) % 20 == 0:
                print(f"  {i+1} ilan tamamlandı...")

        except Exception as e:
            continue
    
    # Ara kayıt (Her marka bitişinde güvenlik kaydı)
    df_gecici = pd.DataFrame(tum_yeni_veriler)
    df_gecici.to_csv("yedek_kayit_5_marka.csv", sep=";", index=False, encoding="utf-8-sig")

# --- BİRLEŞTİRME VE KAYDETME ---
print("\nVeri çekme bitti. Dosyalar birleştiriliyor...")
df_yeni = pd.DataFrame(tum_yeni_veriler)

try:
    # Eski dosyayı oku (Separatör noktalı virgül olduğu için sep=";" kullanıyoruz)
    df_eski = pd.read_csv(MEVCUT_DOSYA_ADI, delimiter=";")
    print(f"Eski dosya okundu: {len(df_eski)} kayıt.")
    
    # Yeni ve eski veriyi birleştir
    df_toplam = pd.concat([df_eski, df_yeni], ignore_index=True)
    
    # Sütunları düzenle
    sutun_sirasi = [
        "Fiyat", "Marka", "Seri", "Model", "Yıl", "Kilometre", 
        "Vites", "Yakıt", "Renk", 
        "Motor Hacmi", "Motor Gücü", "Kasa Tipi", 
        "İlan Tarihi", "Boya-değişen", "Araç Durumu", "Link"
    ]
    
    # Sadece mevcut sütunları seç
    mevcut_sutunlar = [col for col in sutun_sirasi if col in df_toplam.columns]
    df_toplam = df_toplam[mevcut_sutunlar]

    # Kaydet
    df_toplam.to_csv(MEVCUT_DOSYA_ADI, sep=";", index=False, encoding="utf-8-sig")
    print(f"\nBAŞARILI! '{MEVCUT_DOSYA_ADI}' dosyasına {len(tum_yeni_veriler)} yeni kayıt eklendi.")
    print(f"Toplam kayıt sayısı: {len(df_toplam)}")

except FileNotFoundError:
    print(f"HATA: '{MEVCUT_DOSYA_ADI}' bulunamadı. Lütfen dosya ismini kontrol et.")
    # Dosya yoksa bile yeni verileri kaybetmemek için yeni dosya oluşturur
    df_yeni.to_csv("yeni_cekilen_veriler.csv", sep=";", index=False, encoding="utf-8-sig")
    print("Yeni veriler 'yeni_cekilen_veriler.csv' olarak kaydedildi.")

driver.quit()