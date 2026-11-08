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
| `index.html` | Ana sayfa. Türkçe metinler burada, her metin bir `data-i18n` anahtarı taşır. |
| `assets/js/i18n.js` | İngilizce metinler (`EN` sözlüğü) ve dil seçimi. Türkiye saat diliminden gelen ziyaretçi Türkçe, diğerleri İngilizce görür; seçim kaydedilir ve `?lang=tr|en` ile paylaşılabilir. |
| `assets/js/main.js` | Animasyonlar, hizmet yolculuğu sekmeleri, sayaçlar, tema düğmesi, mobil menü ve form doğrulaması. |
| `assets/css/tokens.css` | Renk, yazı, boşluk ve köşe token'ları. Koyu tema varsayılandır, açık tema `data-theme="light"` ile gelir. |
| `assets/css/aule.css` | Bileşen stilleri (`.au-*`). |
| `404.html`, `gizlilik.html`, `kosullar.html` | Alt sayfalar. |

Tasarım kuralları ve bileşenler, Claude'daki **Aule Software** design system'inde belgelenmiştir.

## Yayından önce

- `index.html` içindeki `{{site_url}}` değerlerini gerçek alan adıyla değiştirin ve `assets/og-image.png` ekleyin.
- İletişim formunun `data-endpoint` niteliğine bir form servisinin adresini yazın. Boşken form demo modunda çalışır ve gönderim yapmaz.
- Gizlilik politikası ve kullanım koşulları metinlerini ekleyin.
