---
title: "Departman süreçlerinin analizi: verimlilik fırsatları nasıl bulunur?"
description: Bir departmanın iş akışlarını haritalamak, zaman ve maliyet kayıplarını ölçmek, otomasyon fırsatlarını önceliklendirmek ve yatırımın geri dönüşünü hesaplamak için adım adım bir yöntem.
slug: departman-sureclerinin-analizi
date: 2026-11-09
author: mert
category: Süreç analizi
order: 2
---

Çoğu kurumda verimlilik kaybı tek bir büyük sorundan değil, gün içinde fark edilmeyen yüzlerce küçük adımdan doğar. Bir dosyanın mailden indirilip başka bir sisteme yazılması, bir onayın üç kişiden sırayla istenmesi, ay sonunda aynı raporun elle yeniden hazırlanması. Her biri birkaç dakika sürer; yıl sonunda ise bir ya da iki çalışanın tam zamanlı işine dönüşür.

Süreç analizi, bu görünmeyen yükü görünür ve ölçülebilir hâle getirme işidir. Bu yazıda bir departmanın süreçlerini nasıl analiz ettiğimizi, hangi verileri topladığımızı ve hangi fırsatın önce ele alınması gerektiğine nasıl karar verdiğimizi adım adım anlatıyoruz.

## Süreç analizi neden yazılımdan önce gelir?

Kötü tasarlanmış bir süreci otomatikleştirmek, onu yalnızca daha hızlı kötü hâle getirir. Yazılım yatırımlarının beklenen faydayı vermemesinin en yaygın nedeni teknik değildir: yanlış problem çözülmüştür.

Analiz üç soruya net cevap verir:

- **Zaman nereye gidiyor?** Hangi adımlar en çok çalışan saatini tüketiyor?
- **Hata nerede doğuyor?** Hangi adımlarda veri kayboluyor, tekrar ediliyor ya da yanlış giriliyor?
- **Değer nerede üretiliyor?** Hangi adımlar gerçekten uzmanlık gerektiriyor, hangileri yalnızca veri taşıma işi?

Bu sorulara cevap vermeden yazılım geliştirmeye başlamak, haritasız yola çıkmak gibidir.

## Adım 1: Kapsamı ve hedefi belirleyin

Analize "her şeye bakalım" diye başlamayın. Bir departman ve o departmanın en çok şikâyet edilen ya da en çok zaman tüketen iki veya üç süreci ile başlayın.

Hedefi de baştan yazın. Örneğin:

- Eğitim kayıt sürecinde çalışan başına harcanan zamanı azaltmak
- Sözleşme yenileme tarihlerinin kaçırılmasını önlemek
- Aylık raporlamanın hazırlanma süresini kısaltmak

Net bir hedef, analiz sırasında nelerin önemli olduğuna karar vermenizi kolaylaştırır.

## Adım 2: Süreci olduğu gibi haritalayın

Burada kritik ayrıntı şudur: Süreci **olması gerektiği gibi** değil, **gerçekte nasıl yürüdüğü** gibi haritalayın. Prosedür dokümanları çoğu zaman sahadaki gerçeği yansıtmaz.

Bunun için üç yöntemi birlikte kullanıyoruz:

1. **Birebir görüşmeler.** Süreci yürüten her rolden en az bir kişiyle konuşun. "Bu işi bana baştan sona anlatır mısınız?" sorusu, çoğu zaman yazılı prosedürde olmayan adımları ortaya çıkarır.
2. **Yanında izleme.** Çalışanın işi gerçekten yaparken yanında oturun. İnsanlar alışkanlık hâline gelmiş adımları anlatırken atlar; izlerken atlayamazsınız.
3. **Dijital izler.** Mail klasörleri, paylaşılan Excel dosyaları, sistem kayıtları ve form geçmişleri, sürecin ne sıklıkla ve hangi hacimde yürüdüğünü gösterir.

Haritada her adım için şunları not edin: kim yapıyor, hangi araçla yapıyor, girdi nereden geliyor, çıktı nereye gidiyor ve adım ne kadar sürüyor.

> Haritalamada en değerli bulgular genellikle "bunu ayrıca bir Excel'de de takip ediyoruz" ya da "o kısmı her seferinde mailden kontrol ediyorum" cümlelerinin arkasında saklıdır. Bu ifadeler, resmi sistemin çözmediği bir boşluğa işaret eder.

## Adım 3: Zamanı ve maliyeti ölçün

Haritayı çıkardıktan sonra her adıma bir maliyet yazın. Kesin sayılar şart değildir; makul tahminler bile önceliklendirme için yeterlidir.

Basit bir formül kullanıyoruz:

**Yıllık adım maliyeti** = işlem başına süre (saat) × yıllık işlem sayısı × çalışan saatlik maliyeti

Çalışan saatlik maliyeti hesaplanırken yalnızca brüt maaş değil, işverenin toplam maliyeti esas alınmalıdır. Sigorta primleri, yan haklar ve ofis giderleri dahil edildiğinde gerçek maliyet çoğu zaman brüt maaşın belirgin şekilde üzerindedir.

Ölçerken şu tabloyu doldurmak işinizi kolaylaştırır:

| Adım | İşlem başına süre | Yıllık hacim | Sorumlu rol | Hata ya da tekrar sıklığı |
|---|---|---|---|---|
| Katılımcı listesini mailden toplama | | | | |
| Listeyi İK sistemiyle eşleştirme | | | | |
| Sertifika hazırlama ve gönderme | | | | |
| Aylık raporu hazırlama | | | | |

Hata maliyetini de unutmayın. Elle girilen bir verinin yanlış çıkması, yalnızca düzeltme süresine değil, bazen yanlış bir karara, gecikmiş bir ödemeye ya da kaçırılmış bir yasal süreye mal olur.

## Adım 4: Kayıp türlerini sınıflandırın

Ölçtüğünüz adımları, kaybın türüne göre gruplayın. Bu sınıflandırma, hangi çözümün uygun olduğunu da gösterir.

- **Veri taşıma.** Bilginin bir sistemden diğerine elle aktarılması. Entegrasyonla çözülür.
- **Bekleme.** Onay, imza ya da bilgi beklenen adımlar. İş akışı ve otomatik bildirimlerle çözülür.
- **Tekrar.** Aynı bilginin birden fazla yere girilmesi. Tek bir veri kaynağıyla çözülür.
- **Takip yükü.** Tarihlerin, durumların ve sorumluların elle izlenmesi. Hatırlatma ve panolarla çözülür.
- **Raporlama.** Dağınık verilerin her dönem yeniden derlenmesi. Otomatik raporlarla çözülür.
- **Uzmanlık işi.** Değerlendirme, karar ve müzakere gerektiren adımlar. Bunlar otomatikleştirilmez; desteklenir.

Son madde önemlidir. Amaç insanı süreçten çıkarmak değil, uzmanların zamanını veri taşıma işinden kurtarıp gerçekten değer ürettikleri işe ayırmaktır.

## Adım 5: Fırsatları önceliklendirin

Tüm fırsatları aynı anda ele almak hem bütçeyi hem de ekibin değişime uyum kapasitesini zorlar. Önceliklendirmek için her fırsatı iki eksende değerlendirin:

| | Düşük efor | Yüksek efor |
|---|---|---|
| **Yüksek etki** | Önce bunları yapın | Planlayın ve aşamalara bölün |
| **Düşük etki** | Fırsat buldukça yapın | Şimdilik ertelemek mantıklı |

Etkiyi değerlendirirken yalnızca kazanılan saatlere değil, şu sorulara da bakın:

- Bu adım hata yaptığında sonucu ne kadar ağır oluyor?
- Bu adım bir kişiye bağımlı mı? O kişi izne çıktığında süreç duruyor mu?
- Bu adım müşteriyi ya da diğer departmanları bekletiyor mu?
- Mevzuat ya da denetim açısından bir risk taşıyor mu?

## Adım 6: Yatırımın geri dönüşünü hesaplayın

Önceliklendirdiğiniz fırsat için bir iş gerekçesi hazırlayın. Kullandığımız temel hesap şöyledir:

**Yıllık tasarruf** = mevcut yıllık operasyonel maliyet − yazılım sonrası yıllık operasyonel maliyet

**Geri dönüş süresi (ay)** = yazılım yatırımı ÷ yıllık tasarruf × 12

Gerçek bir projeden örnek verelim. Bir bankanın insan kaynakları departmanında etkinlik ve eğitim süreçlerini iki çalışan yürütüyordu: kayıtlar mailden toplanıyor, katılımcılar elle eşleştiriliyor, raporlar her dönem yeniden hazırlanıyordu.

| Kalem | Tutar |
|---|---|
| Manuel süreçte yıllık operasyonel maliyet | 565.820 TL |
| Yazılım sonrası yıllık operasyonel maliyet | 132.185 TL |
| Yıllık tasarruf | 433.635 TL |
| Yazılım yatırımı | 350.000 TL |
| Geri dönüş süresi | Yaklaşık 10 ay |

Bu hesap, yatırım kararını bir tercih olmaktan çıkarıp ölçülebilir bir iş kararına dönüştürür. Yönetime sunulan tablo artık "yeni bir sistem istiyoruz" değil, "bu yatırım kendini bir yıl dolmadan amorti ediyor" olur.

Hesaplamaya dahil edilmesi gereken ancak çoğu zaman unutulan bir kalem de yıllık bakım ve destek maliyetidir. Gerçekçi bir iş gerekçesi, bu maliyeti yazılım sonrası operasyonel maliyetin içinde gösterir.

## Adım 7: Ölçülebilir başarı kriterleri belirleyin

Projeye başlamadan önce, başarının neye benzeyeceğini sayılarla yazın. Örneğin:

- Eğitim kayıt işlemi başına süre belirli bir hedefin altına inecek
- Kaçırılan sözleşme yenileme tarihi sayısı sıfıra inecek
- Aylık rapor, elle derleme olmadan tek tıkla alınabilecek

Bu kriterler, yazılım devreye alındıktan birkaç ay sonra yapılacak değerlendirmenin temelini oluşturur. Ölçmediğiniz bir iyileşmeyi yönetime gösteremezsiniz.

## Sık yapılan hatalar

- **Yalnızca yöneticilerle konuşmak.** Süreci en iyi bilenler, onu her gün yürütenlerdir.
- **İstisnaları görmezden gelmek.** Sürecin yüzde sekseni basit olabilir; zamanın çoğunu ise kalan istisnalar tüketir.
- **Mevcut süreci olduğu gibi dijitalleştirmek.** Analiz, gereksiz adımları ortadan kaldırma fırsatıdır. Gereksiz bir onay adımını yazılıma taşımak yerine kaldırmayı düşünün.
- **Değişim yönetimini atlamak.** En iyi yazılım bile kullanıcılar benimsemezse fayda üretmez. Eğitim ve geçiş planı, projenin parçası olmalıdır.

## Sonuç

> Verimlilik fırsatlarını bulmanın yolu, süreci gerçekte nasıl yürüdüğü hâliyle haritalamak, her adımın zaman ve maliyetini ölçmek, kayıpları türlerine göre sınıflandırmak ve etkisi en yüksek fırsattan başlamaktır.
>
> İyi bir analizin sonunda elinizde yalnızca bir yazılım fikri değil, geri dönüş süresi hesaplanmış bir iş gerekçesi olur.

Analiz sonucunda hazır bir ürünün yeterli olduğu da ortaya çıkabilir. Bu kararı nasıl vereceğinizi [hazır yazılım mı, kuruma özel yazılım mı rehberimizde](../hazir-yazilim-mi-kuruma-ozel-yazilim-mi/) ele aldık.
