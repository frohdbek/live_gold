import requests
from bs4 import BeautifulSoup
import os

# --- AYARLAR ---
TOKEN = os.getenv('TELEGRAM_TOKEN', 'TOKEN_BURAYA')
CHAT_ID = os.getenv('CHAT_ID', 'ID_BURAYA')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def altin_fiyatini_cek():
    url = "https://altin.doviz.com/ziraat-bankasi/gram-altin"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        fiyat_elementi = soup.find("span", {"data-socket-attr": "ask"})
        if fiyat_elementi:
            fiyat_ham = fiyat_elementi.text.strip()
            return float(fiyat_ham.replace(".", "").replace(",", "."))
    except Exception as e:
        print(f"Veri çekilemedi: {e}")
    return None

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def main():
    guncel_fiyat = altin_fiyatini_cek()
    if not guncel_fiyat: return

    eski_fiyat_dosyasi = "last_price.txt"
    eski_fiyat = None

    # Hafızayı kontrol et
    if os.path.exists(eski_fiyat_dosyasi):
        with open(eski_fiyat_dosyasi, "r") as f:
            try:
                eski_fiyat = float(f.read().strip())
            except:
                eski_fiyat = None

    # MANTIK: Sadece düştüyse (1 kuruş bile olsa) mesaj at
    if eski_fiyat is not None:
        if guncel_fiyat < eski_fiyat:
            fark = round(eski_fiyat - guncel_fiyat, 2)
            rapor = (
                f"📉 *FİYAT DÜŞTÜ!*\n\n"
                f"💰 *Güncel:* {guncel_fiyat} TL\n"
                f"🔙 *Önceki:* {eski_fiyat} TL\n"
                f"🔻 *Düşüş:* {fark} TL\n\n"
                f"Aşağı yönlü hareket başladı!"
            )
            mesaj_gonder(rapor)
        else:
            print(f"Düşüş yok. Güncel: {guncel_fiyat}, Eski: {eski_fiyat}")

    # Yeni fiyatı her durumda kaydet (Yükselse de düşse de hafıza güncellenir)
    with open(eski_fiyat_dosyasi, "w") as f:
        f.write(str(guncel_fiyat))

if __name__ == "__main__":
    main()
