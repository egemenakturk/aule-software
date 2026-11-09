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
| `tools/build_en.py` | `index.html` + `i18n.js` → `en/index.html` ve yasal sayfalar; iki sayfanın yapısal verisini (kuruluş, hizmet, 8 soruluk SSS) görünen metinden üretir. |
| `content/blog/*.md` | Blog yazılarının kaynağı (yalnızca Türkçe). |
| `blog/` | Blog dizini, yazı sayfaları ve `rss.xml`. **Elle düzenlenmez**; `tools/build_blog.py` üretir. |
| `tools/build_blog.py` | Yazıları HTML'e çevirir; `index.html`'deki "Son yazılar" bölümünü ve `sitemap.xml`'i günceller. `build_en.py` bunu kendisi çağırır. |
| `robots.txt`, `sitemap.xml` | Arama motoru keşif dosyaları. `sitemap.xml` üretilir. |
| `assets/fonts/` | Kendi sunucumuzdan yüklenen Geist yazı tipleri (OFL). |
| `assets/js/main.js` | Animasyonlar, hizmet yolculuğu sekmeleri, sayaçlar, tema düğmesi, mobil menü ve form doğrulaması. |
| `assets/css/tokens.css` | Renk, yazı, boşluk ve köşe token'ları. Koyu tema varsayılandır, açık tema `data-theme="light"` ile gelir. |
| `assets/css/aule.css` | Bileşen stilleri (`.au-*`). |
| `404.html` | İki dilli hata sayfası. |
| `gizlilik/`, `kosullar/`, `en/privacy/`, `en/terms/` | Yasal sayfalar (noindex). **Elle düzenlenmez**; metinler `tools/build_en.py` içindeki `LEGAL` listesinden üretilir. |

Tasarım kuralları ve bileşenler, Claude'daki **Aule Software** design system'inde belgelenmiştir.

## Metin değiştirirken

Türkçe metni `index.html`'de, İngilizcesini `assets/js/i18n.js`'te aynı anahtarla değiştirin, sonra:

```bash
python tools/build_en.py
```

## Blog yazısı eklerken

`content/blog/` altına bir `.md` dosyası ekleyin ve `python tools/build_en.py` çalıştırın. Dosyanın başı:

```
---
title: Yazının başlığı
description: Arama sonuçlarında ve kartlarda görünen 1-2 cümlelik özet.
slug: url-de-gorunecek-ad
date: 2026-11-09
author: egemen        # ya da mert (yazarlar build_blog.py içindeki AUTHORS'ta)
category: Süreç analizi
order: 5              # isteğe bağlı; aynı tarihli yazıların sırası
---
```

Gövdede `##` ve `###` başlıklar (içindekilere `##` girer), `-` ve `1.` listeler, `**kalın**`, `[bağlantı](../diger-yazi/)`, boru tabloları ve `>` ile vurgu kutusu kullanılabilir. Başlıkta iki nokta varsa değeri tırnak içine alın.

## Yayından önce

- Alan adı `https://www.aulesoftware.com` olarak ayarlı (canonical, hreflang, sitemap, robots, paylaşım görselleri). Barındırmada çıplak alan adı (`aulesoftware.com`) ve `http` istekleri bu adrese 301 ile yönlendirilmeli.
- İletişim formu Web3Forms'a bağlıdır (`data-endpoint`, gizli `access_key` alanı). `data-fallback-email` niteliğine iletişim e-postası yazılırsa gönderim hatasında bu adres de gösterilir. `data-endpoint` boşaltılırsa form gönderim yapmaz ve "henüz aktif değil" uyarısı gösterir.
- Gizlilik politikası ve kullanım koşulları metinlerini ekleyin.
