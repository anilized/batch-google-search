# Tor IP Rotator + Script Runner

Bu proje Tor ağı üzerinden her 10 saniyede bir IP adresinizi değiştirir ve her IP değişiminden sonra `script.py` dosyasını çalıştırır.

## Gereksinimler
- Python 3.10 veya üzeri
- Python kütüphaneleri:
  ```bash
  pip install requests[socks] stem
  ```

##  Kurulum
1. Komut satırında Tor’u başlatın:
   ```bash
   cd C:\tor
   tor.exe -f torrc
   ```

## Kullanım
Rotator’ı başlatın:
```bash
python tor_rotate.py
```

## ✅ Açıklama
- IP adresi her değiştiğinde `search_once_google.py` çalıştırılır.
- `script.py`, istekleri Tor ağı üzerinden gönderir.
- `queries.csv` icerisindeki queryler ile arama yapar
- Konsolda her IP değişiminde yeni IP yazdırılır.

## 📄 Örnek
```
[+] New Tor IP: 185.220.100.xxx
[i] Running script.py...
[✓] Script finished.
```
