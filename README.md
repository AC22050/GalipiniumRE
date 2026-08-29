# GalipiniumRE — Amnesic Secure Core Browser
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/AC22050/GalipiniumRE)


![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![GUI Framework](https://img.shields.io/badge/GUI-PyQt6%20%2F%20QtWebEngine-green.svg)
![Security Mode](https://img.shields.io/badge/Security-Amnesic%20Mode-red.svg)
![License](https://img.shields.io/badge/License-The%20Unlicense-brightgreen.svg)

**GalipiniumRE**, gelişmiş tarayıcı parmak izi (fingerprinting) engelleme, donanım düzeyinde izleme koruması, DNS/WebRTC sızıntı önleme ve bellek tabanlı (amnesic) çalışma mimarisine sahip ultra güvenli bir ağ tarayıcısıdır.

## Legal Disclaimer / Sorumluluk Reddi

**Disclaimer:** This software (`GalipiniumRE`) is provided for educational, digital privacy, and authorized security research purposes only. It is designed as an advanced anti-surveillance, anti-fingerprinting, and privacy-focused browser tool.

The author (**AC22050**) is **NOT** responsible for any misuse, illegal activities, or damage caused by this software. By downloading, compiling, or using this tool, you acknowledge that you assume total responsibility and legal liability for all actions performed with it.

It is the end user's sole responsibility to obey all applicable local, state, and federal laws while utilizing this software.
---
## Yasal Uyarı ve Sorumluluk Reddi (Disclaimer)

**DİKKAT:** Bu yazılım (`GalipiniumRE`), yalnızca eğitim, dijital gizlilik araştırmaları ve yetkilendirilmiş güvenlik incelemeleri amacıyla geliştirilmiştir. Gelişmiş anti-fingerprinting, gözetim karşıtı (anti-surveillance) ve mahremiyet odaklı bir tarayıcı aracıdır.

Yazılımın geliştiricisi (**AC22050**), bu programın kötüye kullanımı, yasa dışı faaliyetler veya herhangi bir sistem hasarından dolayı **hiçbir koşulda sorumlu tutulamaz**. Bu yazılımı kaynak kod olarak veya derlenmiş ikili (binary) biçimde indiren, kopyalayan ya da kullanan her kullanıcı; doğabilecek tüm hukuki ve cezai sorumluluğu peşinen kabul etmiş sayılır.

Yazılımı kullanırken yürürlükteki tüm yerel ve ulusal yasalara uymak münhasıran son kullanıcının sorumluluğundadır.
---

## 📌 Öne Çıkan Özellikler

- **Amnesic (Hafızasız) Mimari:** Oturum kapatıldığında veya tarayıcı sonlandırıldığında hiçbir çerez (cookie), LocalStorage, geçmiş (history) veya HTTP önbelleği disk üzerinde depolanmaz. Her oturum temiz bir bellek alanı üzerinde yürütülür.
- **Donanım ve FPU Seviyesinde Yanıltma (`fakefpu.py`):** İşlemci zamanlama analizi (timing attacks) ve FPU (Floating Point Unit) parmak izi çıkarma girişimlerine karşı sanal FPU katmanı sunar.
- **Ağ ve Sentetik TCP/IP Katmanı (`faketcpip.py`):** Paket başlıklarını ve soket davranışlarını simüle ederek Derin Paket İncelemesi (DPI) ve ağ seviyesindeki parmak izi çıkarma işlemlerini engeller.
- **Sanal WebGL ve Tuval Koruyucusu (`fakewebgl.py`):** Tuval (Canvas) ve WebGL işleme çağrılarına rastgele gürültü (noise) enjekte ederek grafik tabanlı cihaz tanımlamasını imkansız hale getirir.
- **DNS & WebRTC Sızıntı Koruması:** Gerçek IP adresinizin WebRTC STUN/TURN sorguları veya varsayılan sistem DNS'i üzerinden sızmasını donanım ve yazılım düzeyinde engeller.
- **Sertleştirilmiş Chromium Çekirdeği:** Güvenlik açıklarını ve arka plan veri sızıntılarını önlemek için onlarca özel Chromium bayrağı (flags) ile yapılandırılmıştır.
- **Virtual Javascript Spoof Layer:** Bu JavaScript katmanı; tarayıcı, ekran, donanım ve eklenti bilgilerini (parmak izi verilerini) sahte değerlerle maskeleyerek web sitelerinin gerçek sisteminizi tespit etmesini engeller ve gizliliğinizi korur.
---

## 📂 Proje Yapısı

```
GalipiniumRE/
├── galipiniumRE-1.0.py    # Ana uygulama ve PyQt6 GUI arayüzü
├── fakefpu.py             # Donanım FPU simülasyonu ve parmak izi koruması
├── faketcpip.py           # Sentetik TCP/IP paket yapılandırması & DPI engelleme
├── fakewebgl.py           # WebGL & Canvas gürültü/maskeleme modülü
├── LICENSE                # The Unlicense (Kamu Malı) Lisansı
└── README.md              # Proje dokümantasyonu
└── install.sh             # Linux sistemler için indirme betiği.
└── install.bat            # Windows sistemler için indirme betiği.
```

---

## 🚀 Kurulum

### Gereksinimler

- **Python 3.10** veya üzeri
- `pip` paket yöneticisi

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/AC22050/GalipiniumRE.git
cd GalipiniumRE
```

### 2. Gerekli Bağımlılıkları Yükleyin

```bash
pip install PyQt6 PyQt6-WebEngine cryptography numpy
```

---

## 💻 Kullanım

Uygulamayı başlatmak için ana betiği çalıştırmanız yeterlidir:

```bash
python galipiniumRE-1.0.py
```

### Temel Kontroller
- **Yeni Sekme:** `+` butonuna basın veya menüyü kullanın.
- **Gizlilik Araması:** Adres çubuğuna yazılan sorgular otomatik olarak takip yapmayan DuckDuckGo üzerinden aratılır.
- **Oturum Sıfırlama:** Tarayıcı kapatıldığı anda tüm RAM verisi boşaltılır ve iz bırakmadan sonlanır.

---

## 🛡️ Sertleştirilmiş Chromium Güvenlik Bayrakları

GalipiniumRE arka planda QtWebEngine ile çalışırken aşağıdaki sertleştirilmiş güvenlik ayarlarını uygular:

| Bayrak / Yapılandırma | Açıklama |
| :--- | :--- |
| `--disable-reading-from-canvas` | Canvas okuma işlemlerini engelleyerek iz sürmeyi durdurur. |
| `--disable-webrtc` | IP sızıntılarını önlemek için WebRTC veri kanallarını kısıtlar. |
| `--no-referrers` | HTTP Referer başlıklarının gönderilmesini engeller. |
| `--incognito` | Tüm oturumu bellek üstünde (incognito mode) yürütür. |

---

## 📄 Lisans

Bu proje **The Unlicense** kapsamındadır. Tamamen özgür yazılımdır ve kamu malı (Public Domain) olarak yayınlanmıştır. Kopyalayabilir, değiştirebilir, dağıtabilir ve ticari amaçlarla kullanabilirsiniz.

Daha fazla detay için [LICENSE](LICENSE) dosyasına göz atabilirsiniz.
