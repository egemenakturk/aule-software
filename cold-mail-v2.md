# Aule Software: soğuk mail seti (v2)

Hazırlanma: 11 Kasım 2026
Kaynak: tanıtım sunumu + cold-email skill (v2.2.4)

`cold-mail.md` dosyasındaki ilk sürümden farkları:

- Mailler yarı yarıya kısaldı. İlk mailde 20 dakikalık görüşme istenmiyor; ilgi soran, tek satırla yanıtlanabilen bir soru var.
- Her mail, kuruma dair bir gözlemle açılıyor ve o gözlem doğrudan probleme bağlanıyor.
- Konu satırları 2-4 kelime, küçük harf, isim ve satış dili yok.
- Takip mailleri "gözden kaçmış olabilir" demiyor; her biri yeni bir kanıt ya da açı getiriyor.
- Gönderim ana alan adından değil, ikincil bir alan adından yapılıyor.

---

## 1. Göndermeden önce

**İkincil alan adı.** `aulesoftware.com` ile gönderim yapmayın; spam şikâyeti ana alan adının itibarını bozar. Benzer bir alan adı alın (ör. `auleyazilim.com`, `aule-software.com`), siteye yönlendirin ve oradan gönderin.

1. Alan adı başına 2-3 posta kutusu açın (Google Workspace ya da Microsoft 365), kişi adıyla: `egemen@`, `mert@`.
2. SPF, DKIM ve DMARC kayıtlarını kurun. DMARC başlangıç için `p=none`.
3. Posta kutularını 3-4 hafta ısıtın. Bu sürede soğuk gönderim yok.
4. Isınma bittikten sonra posta kutusu başına günde 20-30 mail ile başlayın.

**Liste.** Her yüklemeden hemen önce adresleri doğrulayın (Truelist, Hunter vb.). Geri dönme oranı %2'yi geçerse gönderimi durdurun ve listeye bakın.

**Takip.** Açılma ve tıklama takibini kapatın. Ölçtüğünüz tek şey yanıt.

**Biçim.** Düz metin. Görsel, ek, HTML yok. Mail başına en fazla bir link, ilk mailde hiç link yok.

**Hukuk.** 6563 sayılı Kanun'a göre tacirlere gönderilen ticari iletilerde önceden onay aranmaz, ancak her mailde gönderici kimliği, posta adresi ve ücretsiz ret imkânı bulunmalı (aşağıdaki imzada var). Adresleri kamuya açık kaynaklardan toplayın, "istemiyorum" diyenleri tüm kanallardan hemen çıkarın. Kesin değerlendirme için avukatınıza danışın.

---

## 2. Kişiselleştirme: gözlem nereden bulunur?

İlk cümle o kuruma özel olmalı ve problemle bağlantılı olmalı. Gözlem cümlesini silince mail hâlâ anlamlıysa gözlem işe yaramıyordur.

| Sinyal | Nerede | Hangi maile bağlanır |
|---|---|---|
| Eğitim uzmanı, İK operasyon ilanı | LinkedIn İş İlanları, Kariyer.net | İK |
| Akademi, eğitim programı, sertifika duyurusu | LinkedIn şirket sayfası, faaliyet raporu | İK |
| Hukuk müşaviri, sözleşme uzmanı ilanı | LinkedIn | Hukuk |
| Yeni tesis, satın alma, tedarikçi sayısında artış | KAP, basın bültenleri | Hukuk, satın alma |
| Dijital dönüşüm direktörü ataması, BT ekibi ilanları | LinkedIn, KAP | BT |
| Yöneticinin süreçlerle ilgili paylaşımı | LinkedIn | Hepsi |

Öncelik: case'lere yakın sektörler (bankacılık, enerji, sigorta, havacılık), 250 üzeri çalışan.

---

## 3. İlk mailler

### 3.1 İnsan kaynakları (en güçlü kanıt)

**Konu:** eğitim takibi

Merhaba {{Ad}} {{Hanım/Bey}},

{{Kurum}}'un {{gözlem: bu yıl iki eğitim uzmanı ilanı açtığını / yeni liderlik akademisini duyurduğunu}} gördüm. Bu ölçekte davet, yoklama ve sertifika işi çoğu kurumda Excel ve e-postayla yürüyor ve maliyeti hiç hesaplanmıyor.

Bir bankanın İK ekibinde bu işi iki kişi yürütüyordu. Kuruma özel bir platformla yıllık maliyet 565 bin TL'den 132 bin TL'ye indi, yatırım 10 ayda geri döndü.

Aynı hesabı {{Kurum}} için çıkarmamın işinize yarar mı?

Egemen

---

### 3.2 Hukuk

**Konu:** sözleşme yenilemeleri

Merhaba {{Ad}} {{Hanım/Bey}},

{{gözlem: {{Kurum}}'un son bir yılda üç yeni tesis devreye aldığını}} gördüm. Tedarikçi sayısı arttıkça yenileme tarihlerini Excel'den takip etmek zorlaşıyor ve bir tanesi kaçınca maliyeti yüksek oluyor.

Bir enerji şirketinin hukuk ekibi için yenileme hatırlatmaları ve dava takvimi olan bir sistem kurduk. Yıllık takip maliyeti 851 bin TL'den 284 bin TL'ye indi.

Sizin ekipte bu takip bugün nasıl yürüyor, merak ettim. Konuşmaya değer mi?

Egemen

---

### 3.3 BT ve dijital dönüşüm

**Konu:** departman talepleri

Merhaba {{Ad}} {{Hanım/Bey}},

{{gözlem: Dijital dönüşüm direktörlüğüne geçtiğinizi gördüm, tebrikler.}} Bu rolde ilk aylarda departmanlardan küçük yazılım talepleri yağıyor ve çoğu ana sistemlerin arkasında sıraya giriyor.

Biz bu talepleri BT ekibinin yükünü artırmadan karşılıyoruz. Mevcut sistemlere entegre geliştiriyoruz, kaynak kod ve dokümantasyon size devrediliyor. Gerçek veri geliştirme araçlarına hiç verilmiyor.

Bekleme listesindeki taleplerden birini birlikte değerlendirmek ister misiniz?

Egemen

---

### 3.4 Genel müdürlük ve operasyon (departman belli değilse)

**Konu:** elle yürüyen raporlar

Merhaba {{Ad}} {{Hanım/Bey}},

{{gözlem: {{Kurum}}'un faaliyet raporunda operasyonel verimliliğin bu yılın önceliği olarak geçtiğini}} gördüm. Bizim gördüğümüz kayıp genelde sistemlerin arasında: aynı veri bir yerden alınıp başka yere elle yazılıyor ve aynı rapor her ay sıfırdan hazırlanıyor.

Bir bankanın İK'sında ve bir enerji şirketinin hukuk departmanında bu adımları ölçüp yazılımla kaldırdık. İki projede de yatırım 10 ayda geri döndü.

{{Kurum}}'da en çok zaman alan süreci bulmak için kısa bir analiz işinize yarar mı?

Egemen

---

## 4. Takip mailleri

Aralıklar giderek açılıyor: 1. gün ilk mail, 4. gün takip 1, 9. gün takip 2, 17. gün kapanış. Her mail tek başına okunabilir; önceki maile atıf yok. Takipleri aynı konuya yanıt olarak gönderin.

### Takip 1 (4. gün): hesabın nasıl yapıldığı

Merhaba {{Ad}} {{Hanım/Bey}},

Tasarruf rakamlarını nasıl hesapladığımızı soran çok oluyor. Her adımın süresini, hacmini ve bunu yapan kişinin saat maliyetini ölçüyoruz, sonra yıla vuruyoruz. Eğitim takibi için hesabın tamamını burada açtık:

https://www.aulesoftware.com/blog/egitim-katilim-takibi-excel/

{{Kurum}}'daki bir süreç için aynı tabloyu çıkarmamı ister misiniz?

Egemen

### Takip 2 (9. gün): her iş yazılım gerektirmez

Merhaba {{Ad}} {{Hanım/Bey}},

Analizlerimizin bir kısmı "burada hazır ürün yeterli" önerisiyle bitiyor. Muhasebe, bordro gibi standart süreçlerde genelde doğru seçim de bu. Kuruma özel yazılımı yalnızca sistemler arasında elle yürüyen ve sizi diğerlerinden ayıran süreçler için öneriyoruz. Ürettiğimiz kodun ve verinin sahibi de siz oluyorsunuz, lisans ücreti yok.

{{Kurum}}'da hangi tarafa düşen bir süreç olduğunu birlikte görmek ister misiniz?

Egemen

### Kapanış (17. gün)

Merhaba {{Ad}} {{Hanım/Bey}},

Bu konuda size son yazışım. Zamanlama uygun değilse ya da konu başka bir ekipteyse, doğru kişinin adını yazmanız bile çok yardımcı olur.

İyi çalışmalar,
Egemen

Kapanıştan sonra bu kişiye bu kampanyadan tekrar yazmayın. 3-4 ay sonra yeni bir sinyal çıkarsa (yeni ilan, atama, KAP açıklaması) yeni bir sırayla dönebilirsiniz.

---

## 5. LinkedIn ile birlikte

- İlk mailden 1-2 gün önce kişinin bir paylaşımına anlamlı bir yorum yazın, sonra notsuz bağlantı isteği gönderin.
- Bağlantı kabul edilirse mesajda mailin kopyasını değil, tek cümlelik bir soru yazın.
- **Herhangi bir kanaldan yanıt gelirse tüm kanallarda sırayı durdurun.** Mail sırası devam ederken LinkedIn'den yanıt veren birine takip maili gitmesin.

---

## 6. Yanıt gelince

| Yanıt | Ne yapılır |
|---|---|
| Olumlu | Aynı saat içinde yanıtlayın. İki somut zaman önerin (ör. "Salı 14.00 ya da Perşembe 10.30") ve takvim linki ekleyin. |
| Bilgi istiyor | Soruyu kısaca yanıtlayın, sunumu PDF olarak ekleyin, görüşme önerin. |
| İtiraz ("BT ekibimiz yapıyor") | Kabul edin, BT'nin bekleme listesindeki talepleri sorun. |
| Şimdi değil | Teşekkür edin, sordukları ayı not edip o zaman yazın. |
| Başka kişiye yönlendirme | Yönlendireni anarak yeni kişiye yazın ("{{Ad}} Bey size yazmamı önerdi"). |
| İstemiyorum | Tüm listelerden hemen çıkarın, yanıt vermeyin. |

---

## 7. İngilizce (yabancı yöneticiler için)

**Subject:** training admin

Hi {{First name}},

Saw that {{Company}} {{observation: launched a new leadership academy this year}}. At that scale, invitations, attendance and certificates usually run on spreadsheets and email, and nobody puts a number on it.

At a bank's HR team, two people were doing this work. With a custom platform, the annual cost went from TRY 566k to TRY 132k, and the investment paid back in 10 months.

Would it help if I ran the same numbers for {{Company}}?

Egemen

---

## İmza

```
Egemen Doğuş Aktürk
Kurucu Ortak, Aule Software
Eğitim Mah., 34722 Kadıköy / İstanbul

Bu mesaj ticari bilgilendirme amaçlıdır. Tekrar almak istemezseniz
"istemiyorum" yazarak yanıtlamanız yeterli.
```

İlk mailde imzaya web sitesi linki koymayın (link sayısı sıfır kalsın). Mert için aynı imza, kendi adıyla.

## Ölçüm

Haftalık tablo: gönderilen, geri dönen, yanıt, olumlu yanıt, görüşme. Hedef yanıt oranı %3-5. 100 mailden sonra %2'nin altındaysa önce gözlem cümlesini, sonra kanıtı, en son konu satırını değiştirin. Geri dönme %2'yi, spam şikâyeti %0,1'i geçerse o posta kutusundan gönderimi durdurun.
