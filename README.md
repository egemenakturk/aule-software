# Aule Software

Aule Software'in kurumsal web sitesi: tek sayfalık, iki dilli (TR / EN), koyu ve açık temalı statik site. Derleme adımı yoktur; dosyalar olduğu gibi yayınlanır.

## Yerelde çalıştırma

```bash
python -m http.server 5173
```

Ardından `http://localhost:5173` adresini açın.

## Yapı

| Dosya | İçerik |
| --- | --- |
| `index.html` | Türkçe ana sayfa (`/`). Her metin bir `data-i18n` anahtarı taşır. |
| `en/index.html` | İngilizce sayfa (`/en/`). **Elle düzenlenmez**; `tools/build_en.py` üretir. |
| `assets/js/i18n.js` | İngilizce metinler (`EN` sözlüğü) ve betiklerin kullandığı mesajlar. İlk ziyarette Türkiye saat dilimindeki tarayıcılar `/`, diğerleri `/en/` sayfasına yönlendirilir; arama motoru ve önizleme botları yönlendirilmez. Dil seçimi kaydedilir. |
| `tools/build_en.py` | `index.html` + `i18n.js` → `en/index.html`; iki sayfanın yapısal verisini (kuruluş, hizmet, 8 soruluk SSS) görünen metinden üretir. |
| `robots.txt`, `sitemap.xml` | Arama motoru keşif dosyaları. |
| `assets/fonts/` | Kendi sunucumuzdan yüklenen Geist yazı tipleri (OFL). |
| `assets/js/main.js` | Animasyonlar, hizmet yolculuğu sekmeleri, sayaçlar, tema düğmesi, mobil menü ve form doğrulaması. |
| `assets/css/tokens.css` | Renk, yazı, boşluk ve köşe token'ları. Koyu tema varsayılandır, açık tema `data-theme="light"` ile gelir. |
| `assets/css/aule.css` | Bileşen stilleri (`.au-*`). |
| `404.html`, `gizlilik.html`, `kosullar.html` | Alt sayfalar. |

Tasarım kuralları ve bileşenler, Claude'daki **Aule Software** design system'inde belgelenmiştir.

## Metin değiştirirken

Türkçe metni `index.html`'de, İngilizcesini `assets/js/i18n.js`'te aynı anahtarla değiştirin, sonra:

```bash
python tools/build_en.py
```

## Yayından önce

- Alan adı `https://www.aulesoftware.com` olarak ayarlı (canonical, hreflang, sitemap, robots, paylaşım görselleri). Barındırmada çıplak alan adı (`aulesoftware.com`) ve `http` istekleri bu adrese 301 ile yönlendirilmeli.
- İletişim formu Web3Forms'a bağlıdır (`data-endpoint`, gizli `access_key` alanı). `data-fallback-email` niteliğine iletişim e-postası yazılırsa gönderim hatasında bu adres de gösterilir. `data-endpoint` boşaltılırsa form gönderim yapmaz ve "henüz aktif değil" uyarısı gösterir.
- Gizlilik politikası ve kullanım koşulları metinlerini ekleyin.
