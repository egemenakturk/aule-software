---
title: "Eğitim katılım takibi: eğitim ve etkinlikleri Excel'de yönetmenin gizli maliyeti"
description: Kurum içi eğitim ve etkinliklerin davet, kayıt, yoklama, sertifika ve raporlama adımlarını Excel ve e-postayla yürütmenin gerçek maliyeti, bu maliyeti hesaplama yöntemi ve bir eğitim takip sisteminde olması gerekenler.
slug: egitim-katilim-takibi-excel
date: 2026-11-11
author: mert
category: İnsan kaynakları
order: 5
---

Çoğu kurumda insan kaynakları ekibi yılda onlarca eğitim ve etkinlik düzenler: oryantasyonlar, zorunlu eğitimler, liderlik programları, şirket buluşmaları. Bu organizasyonların büyük kısmı hâlâ aynı araçlarla yürür: bir Excel dosyası, bir e-posta kutusu ve bolca hatırlatma.

Bu yöntem çalışır; sorun da tam olarak burada başlar. Çalıştığı için kimse maliyetini sorgulamaz. Oysa eğitim katılım takibini elle yürütmenin bedeli, yıl sonunda bir ya da iki çalışanın tam zamanlı işine denk gelebilir. Bu yazıda bu maliyetin nerede saklandığını, kendi kurumunuz için nasıl hesaplayacağınızı ve iyi bir eğitim takip sisteminde nelerin olması gerektiğini anlatıyoruz.

## Bir eğitimin perde arkası

Katılımcının gözünden bir eğitim, bir davet e-postası ve birkaç saatlik bir oturumdur. İK ekibinin gözünden ise aşağıdaki adımların her biri ayrı bir iştir:

1. **Planlama.** Eğitim ihtiyacının toplanması, tarih, eğitmen ve kontenjanın belirlenmesi.
2. **Duyuru ve davet.** Hedef çalışan listesinin çıkarılması ve davetlerin gönderilmesi.
3. **Kayıt ve kontenjan.** Gelen yanıtların toplanması, kontenjan dolunca bekleme listesinin yönetilmesi.
4. **Hatırlatma ve değişiklikler.** Son dakika iptalleri, yer değiştirmeler, tarih güncellemeleri.
5. **Yoklama.** Eğitim günü katılımın kayda alınması.
6. **Sertifika.** Katılanlar için sertifikaların hazırlanması ve gönderilmesi.
7. **Değerlendirme.** Memnuniyet anketlerinin gönderilmesi ve sonuçların toplanması.
8. **Raporlama.** Çalışan başına eğitim saatleri, zorunlu eğitimlerin tamamlanma durumu, yönetime ve denetime sunulan raporlar.

Excel ve e-postayla çalışan bir ekipte bu adımların neredeyse hepsi elle yapılır ve çoğu birden fazla kez tekrarlanır.

## Gizli maliyet nerede saklanıyor?

Elle yürütülen bir eğitim sürecinde zaman, tek tek bakıldığında küçük görünen kayıplarda harcanır:

| Kayıp | Nasıl ortaya çıkar? |
|---|---|
| Tekrar veri girişi | Aynı katılımcı bilgisi davet listesine, kayıt tablosuna, yoklamaya ve sertifikaya ayrı ayrı yazılır |
| Eşleştirme | E-postayla gelen kayıtlar, sicil numarası ve departman bilgisi için İK sistemiyle elle eşleştirilir |
| Değişiklik yönetimi | Her iptal ya da tarih değişikliği, tüm listelerde ayrı ayrı güncellenir |
| Sertifika hazırlığı | Sertifikalar tek tek hazırlanır, isimler kontrol edilir ve tek tek gönderilir |
| Rapor derleme | Yıl sonu raporu için farklı dosyalardaki veriler birleştirilir, tutarsızlıklar ayıklanır |
| Kişiye bağımlılık | Hangi dosyanın güncel olduğunu yalnızca süreci yürüten kişi bilir; o kişi izne çıktığında süreç yavaşlar |

Bunlara bir de hata maliyeti eklenir. Yanlış kişiye gönderilen bir davet, eksik yazılmış bir sertifika ya da takipten kaçan bir zorunlu eğitim, düzeltme süresinin ötesinde itibar ve uyum riski de taşır.

## Kendi maliyetinizi hesaplayın

Bu maliyeti görmek için karmaşık bir analize gerek yok. Bir aylık ölçüm, yıllık tabloyu çıkarmaya yeter.

**1. Adımları ve süreleri yazın.** Yukarıdaki sekiz adımın her biri için, tek bir eğitimde harcanan ortalama süreyi not edin.

**2. Yıllık hacmi belirleyin.** Yılda kaç eğitim ve etkinlik düzenleniyor, ortalama kaç katılımcıyla?

**3. Saatlik maliyeti hesaplayın.** Süreci yürüten çalışanların işverene toplam maliyetini (maaş, yan haklar, sigorta primleri) yıllık çalışma saatine bölün.

**4. Formülü uygulayın.**

**Yıllık operasyonel maliyet** = eğitim başına toplam süre (saat) × yıllık eğitim sayısı × saatlik maliyet

Katılımcı sayısına bağlı adımlar (eşleştirme, sertifika gibi) için süreyi katılımcı başına hesaplayıp katılımcı sayısıyla çarpmak daha doğru sonuç verir.

Bu hesabı daha ayrıntılı yapmak isterseniz, adım adım yöntemi [departman süreçlerinin analizi rehberimizde](../departman-sureclerinin-analizi/) anlattık.

## Gerçek bir örnek: bir bankanın İK departmanı

Büyük bir bankanın insan kaynakları departmanı, yıl boyunca düzenlenen etkinlik ve eğitimleri tam olarak yukarıda anlatılan şekilde yürütüyordu. Etkinlik planlama, katılımcı takibi ve eğitim sertifikaları Excel ve e-posta üzerinden yönetiliyordu. Bu süreçleri iki çalışan yürütüyordu.

Kurum için intranet tabanlı, kuruma özel bir etkinlik yönetim platformu geliştirdik. Platformda otomatik davet, katılım takibi, sertifika oluşturma ve raporlama tek ekranda toplandı.

| Kalem | Tutar |
|---|---|
| Manuel süreçte yıllık operasyonel maliyet | 565.820 TL |
| Yazılım sonrası yıllık operasyonel maliyet | 132.185 TL |
| Yıllık tasarruf | 433.635 TL |
| Yazılım yatırımı | 350.000 TL |
| Geri dönüş süresi | Yaklaşık 10 ay |

Tasarrufun büyük kısmı tek bir özellikten değil, adımlar arasındaki el değiştirmelerin ortadan kalkmasından geldi. Çalışan bilgisi bir kez, doğrudan kurumun sisteminden alındığında; tekrar giriş, eşleştirme ve sertifika hazırlığı kendiliğinden kısaldı.

## Bir eğitim takip sisteminde olması gerekenler

Hazır bir ürün değerlendiriyor ya da kuruma özel bir sistem planlıyor olun, aşağıdaki listeyi bir kontrol listesi olarak kullanabilirsiniz:

- **Çalışan verisi tek kaynaktan.** Ad, sicil numarası, departman ve yönetici bilgisi elle girilmemeli, İK sisteminden ya da kurumsal dizinden gelmeli.
- **Kontenjan ve bekleme listesi.** Kontenjan dolduğunda kayıtlar otomatik olarak bekleme listesine alınmalı, iptal olduğunda sıradaki kişiye yer açılmalı.
- **Otomatik davet ve hatırlatma.** Davetler, takvim kayıtları ve hatırlatmalar sistemden gönderilmeli.
- **Kolay yoklama.** Eğitim günü katılım hızlıca kayda alınabilmeli.
- **Otomatik sertifika.** Katılımı onaylanan herkes için sertifika şablondan otomatik üretilip gönderilmeli.
- **Zorunlu eğitim takibi.** Kimin hangi zorunlu eğitimi tamamlamadığı görülebilmeli ve hatırlatma gönderilebilmeli.
- **Değerlendirme anketi.** Eğitim sonrası anket otomatik gönderilmeli, sonuçlar eğitimle ilişkilendirilmeli.
- **Hazır raporlar.** Çalışan başına eğitim saati, departman bazlı katılım ve tamamlanma oranları tek tıkla alınabilmeli.
- **Yetki ve kişisel veri güvenliği.** Kimin hangi veriyi görebileceği rol bazında belirlenmeli; kişisel veriler mevzuata uygun işlenmeli ve saklanmalı.

## Hazır eğitim yazılımı mı, kuruma özel sistem mi?

Piyasada çevrim içi eğitim içeriğini yönetmek için tasarlanmış çok sayıda hazır öğrenme yönetim sistemi var. Eğitimlerinizin büyük kısmı video ve çevrim içi modüllerden oluşuyorsa, bu ürünler çoğu zaman iyi bir başlangıçtır.

Kuruma özel bir sistem ise şu durumlarda öne çıkar:

- Eğitimlerin önemli bir kısmı yüz yüze yapılıyor ve organizasyon iş yükü yüksekse,
- Etkinlikler ve eğitimler aynı ekip tarafından, aynı süreçle yönetiliyorsa,
- Sistemin kurumun intraneti, İK sistemi ve kurumsal dizini ile entegre çalışması gerekiyorsa,
- Hazır bir ürün alınmış ama etrafında hâlâ Excel dosyaları ve e-posta zincirleri dönüyorsa.

İki seçeneği karşılaştırırken bakılması gereken kriterleri [hazır yazılım mı, kuruma özel yazılım mı rehberimizde](../hazir-yazilim-mi-kuruma-ozel-yazilim-mi/) ayrıntılı olarak ele aldık.

## Nereden başlamalı?

İlk adım yazılım seçmek değil, ölçmektir. Önümüzdeki bir ay boyunca düzenlenen eğitimlerde, yukarıdaki sekiz adımın her birine harcanan süreyi not edin. Ay sonunda elinizde hem yıllık maliyetin gerçekçi bir tahmini hem de en çok zamanın kaybolduğu adımların listesi olur. Bu liste, hangi çözümün size uygun olduğunu çoğu zaman kendiliğinden gösterir.

## Sonuç

> Eğitim ve etkinlikleri Excel ve e-postayla yönetmek, çalıştığı için maliyeti fark edilmeyen bir yöntemdir. Maliyet; tekrar veri girişinde, eşleştirmede, sertifika hazırlığında ve rapor derlemede saklanır.
>
> Bu adımları ölçtüğünüzde, eğitim katılım takibinin yıllık maliyeti çoğu zaman bir yazılım yatırımını bir yıl içinde karşılayacak büyüklüktedir.

Kendi eğitim süreçleriniz için bu hesabı birlikte yapmak isterseniz, kısa bir ön görüşmede başlayabiliriz.
