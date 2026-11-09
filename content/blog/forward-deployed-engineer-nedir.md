---
title: Forward Deployed Engineer nedir? Müşterinin yanında çalışan mühendis
description: Forward Deployed Engineer rolünün ne olduğu, nereden çıktığı, klasik yazılım ekibi ve danışmanlıktan farkı, yapay zekâ döneminde neden yeniden önem kazandığı ve kurumlara ne kazandırdığı.
slug: forward-deployed-engineer-nedir
date: 2026-11-09
author: egemen
category: Çalışma modeli
order: 4
---

Yazılım projelerinin önemli bir kısmı teknik nedenlerle değil, iletişim nedeniyle zorlanır. İş birimi ihtiyacını anlatır, analist bunu dokümana döker, geliştirici dokümanı okuyup kodu yazar. Her el değiştirmede bilginin bir kısmı kaybolur ve ortaya çıkan yazılım, teknik olarak doğru olsa bile sahadaki gerçek ihtiyacı tam karşılamaz.

**Forward Deployed Engineer**, yani Türkçeye en yakın ifadeyle sahaya konuşlanmış mühendis, bu kopukluğu ortadan kaldırmak için ortaya çıkmış bir roldür. Bu yazıda rolün ne olduğunu, nereden geldiğini, diğer modellerden farkını ve kurumlar için ne anlama geldiğini anlatıyoruz.

## Kısa tanım

Forward Deployed Engineer, müşterinin süreçlerini yerinde öğrenen, kullanıcılarla doğrudan çalışan ve bu öğrendiklerini aynı kişi olarak çalışan yazılıma dönüştüren mühendistir.

Bu tanımdaki kilit ifade **aynı kişi** ifadesidir. Analiz eden, tasarlayan, kodu yazan ve devreye alan arasında bir el değiştirme yoktur. Müşterinin sorununu dinleyen kişi, o sorunu çözen kodu da yazar.

## Rol nereden çıktı?

Rol, en çok veri analitiği şirketi Palantir ile özdeşleşmiştir. Palantir, karmaşık kurumsal ve kamu müşterilerine yazılım sunarken standart bir ürünün tek başına yeterli olmadığını gördü. Her müşterinin verisi, sistemleri ve iş yapış biçimi farklıydı. Çözüm, mühendisleri doğrudan müşterinin yanına göndermek oldu.

Bu mühendisler ürünü müşterinin gerçek problemine uyarlıyor, eksik kalan parçaları sahada yazıyor ve öğrendiklerini ürün ekibine geri taşıyordu. Zamanla bu yaklaşım, karmaşık kurumsal problemleri çözmenin etkili bir yolu olarak başka şirketler tarafından da benimsendi.

## Yapay zekâ döneminde neden yeniden gündemde?

Son yıllarda büyük yapay zekâ şirketleri de Forward Deployed Engineer ekipleri kurmaya başladı. Bunun nedeni basittir: Güçlü bir yapay zekâ modeline erişmek, onu bir kurumun gerçek iş akışına yerleştirmekle aynı şey değildir.

Bir modelin kurumda değer üretmesi için şunların çözülmesi gerekir:

- Model hangi veriye, hangi yetkiyle erişecek?
- Mevcut sistemlerle nasıl entegre olacak?
- Hangi adımda insan onayı gerekecek?
- Sonuçlar nasıl ölçülecek ve denetlenecek?

Bu soruların cevabı bir ürün dokümanında değil, kurumun içindedir. Forward Deployed Engineer, bu cevapları yerinde bulup çalışan bir sisteme dönüştüren kişidir.

## Klasik modellerden farkı

| | Klasik yazılım ekibi | Danışmanlık | Forward Deployed Engineer |
|---|---|---|---|
| Nerede çalışır? | Kendi ofisinde | Müşteride | Müşteride ve kullanıcıyla birlikte |
| Çıktısı | Spesifikasyona göre yazılım | Rapor ve öneri | Çalışan yazılım |
| İhtiyacı kimden öğrenir? | Dokümandan | Yöneticilerden | Süreci yürüten kişilerden |
| El değiştirme | Analist, tasarımcı, geliştirici arasında | Rapordan uygulama ekibine | Yok denecek kadar az |
| Geri bildirim döngüsü | Haftalar ya da aylar | Proje sonunda | Günler |

Klasik yazılım ekibi iyi tanımlanmış problemlerde verimlidir; ancak problem belirsizse spesifikasyon yanlış olur. Danışmanlık problemi iyi tanımlar; ancak çıktısı çoğu zaman uygulanmayı bekleyen bir rapordur. Forward Deployed Engineer ise problemi tanımlamakla çözmeyi tek bir kişide ya da küçük bir ekipte birleştirir.

## Bir Forward Deployed Engineer gün içinde ne yapar?

Rol, masa başı mühendislikten oldukça farklıdır. Tipik bir hafta şunları içerir:

- **Kullanıcıyı izlemek.** Süreci yürüten çalışanın yanında oturup işin gerçekte nasıl yapıldığını görmek
- **Veriyi anlamak.** Kurumun sistemlerindeki verinin yapısını, kalitesini ve sınırlarını incelemek
- **Hızlı prototip.** Gördüğü sorunu birkaç gün içinde çalışan bir ilk sürüme dönüştürmek
- **Birlikte denemek.** Prototipi kullanıcıyla birlikte gerçek işte kullanıp aksayan yerleri görmek
- **Sağlamlaştırmak.** İşe yarayan çözümü güvenlik, test ve bakım standartlarına uygun hâle getirmek
- **Devretmek.** Kullanıcıları eğitmek ve kurumun ekibine bilgi aktarmak

Bu döngünün en değerli tarafı hızdır. Yanlış anlaşılmış bir ihtiyaç, aylar sonra teslim edilen bir yazılımda değil, ilk haftanın prototipinde fark edilir.

## Bu rol için hangi yetkinlikler gerekir?

Forward Deployed Engineer, iyi bir yazılım mühendisinin tüm teknik becerilerine sahip olmalıdır. Ancak rolü farklı kılan, teknik becerinin yanında aranan özelliklerdir:

- **İş dilini konuşabilmek.** Bir İK uzmanıyla, bir avukatla ya da bir finans yöneticisiyle onların terimleriyle konuşabilmek
- **Belirsizlikle çalışabilmek.** Net bir spesifikasyon beklemeden, gözlemden yola çıkarak problemi tanımlayabilmek
- **Önceliklendirme.** Her isteği değil, en çok değer üretecek olanı önce yapabilmek
- **Sahiplenme.** Kodun yazılmasıyla değil, kullanıcının işinin gerçekten kolaylaşmasıyla kendini sorumlu hissetmek
- **Kurumsal disiplin.** Güvenlik, mevzuat ve denetim gerekliliklerini baştan tasarıma dahil etmek

## Kurumlar için ne anlama gelir?

Forward Deployed yaklaşımı, kurumlar için üç somut fayda sağlar.

**Doğru problem çözülür.** İhtiyaç, süreci yürütenlerden yerinde öğrenildiği için yazılım, gerçek iş akışına oturur. Teslimattan sonra "bunu böyle istememiştik" cümlesi duyulmaz.

**Değer daha erken görünür.** Aylar süren bir analiz ve geliştirme döngüsü yerine, ilk çalışan sürüm haftalar içinde kullanıcının önüne gelir. Yatırımın işe yarayıp yaramadığı erken görülür.

**Bilgi kurumda kalır.** Mühendis yalnızca yazılım teslim etmez; kurumun ekibini eğitir, süreci belgeler ve kaynak kodu devreder. Kurum, tedarikçiye bağımlı hâle gelmez.

## Hangi durumlarda doğru modeldir?

Bu yaklaşım her proje için gerekli değildir. Şu durumlarda özellikle değerlidir:

- Süreç karmaşık, istisnası bol ve yazılı olarak tam tanımlanmamışsa
- Birden fazla departman ve sistem işin içindeyse
- Kullanıcıların ne istediğini tarif etmesi zorsa, ama gördüklerinde hemen fark edebiliyorlarsa
- Yapay zekâ gibi yeni bir teknolojinin kurumun iş akışına nasıl yerleşeceği henüz belli değilse

Buna karşılık, gereksinimleri net ve standart olan bir iş için klasik bir geliştirme modeli ya da hazır bir ürün çoğu zaman daha uygundur.

## Aule'nin çalışma modeliyle bağlantısı

Aule'yi kurarken benimsediğimiz yaklaşım, bu modelin kurum ölçeğine uyarlanmış hâlidir. Her projeye departmanın içinde, süreci yürüten kişilerle birlikte yaptığımız bir analizle başlıyoruz. Analizi yapan ekip, yazılımı geliştiren ve devreye alan ekiple aynıdır. Kullanıcı eğitimi ve yıllık bakım da aynı ekibin sorumluluğundadır.

Bu yöntemin ilk adımını, yani bir departmanın süreçlerini yerinde nasıl analiz ettiğimizi, [departman süreçlerinin analizi rehberimizde](../departman-sureclerinin-analizi/) ayrıntılı olarak anlattık.

## Sonuç

> Forward Deployed Engineer, müşterinin süreçlerini yerinde öğrenip bunu doğrudan çalışan yazılıma dönüştüren mühendistir. Analiz ile geliştirme arasındaki el değiştirmeyi ortadan kaldırarak doğru problemin, daha kısa sürede çözülmesini sağlar.
>
> Yapay zekâ döneminde bu rol yeniden önem kazandı, çünkü teknolojiye erişmek kolaylaştı; onu bir kurumun gerçek işine yerleştirmek ise hâlâ sahada, kullanıcıyla birlikte yapılan bir iş.
