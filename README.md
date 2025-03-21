# Metro Simulation with A* and BFS Algorithms

Bu proje, bir metro ağı üzerindeki istasyonlar arasında en az aktarmalı ya da en hızlı rotayı bulmak için BFS (Breadth-First Search) ve A* (A Star) algoritmalarını kullanır.

## 📌 Projenin Amacı

- Gerçek bir metro ağı gibi çalışan yönsüz, ağırlıklı bir grafik modeli oluşturmak.
- Kullanıcıdan alınan başlangıç ve varış istasyonları arasındaki:
  - **En az aktarma gerektiren rotayı (BFS ile)**
  - **En hızlı rotayı (A* algoritması ile)**
  hesaplamak.

## 🚉 Metro Ağı Modeli

Bu proje bir metro ağını **graf veri yapısı** ile modellemektedir.

- **İstasyonlar (Istasyon sınıfı)**: Grafın düğümleridir.
- **Bağlantılar (baglanti_ekle metodu)**: İstasyonlar arasındaki kenarları temsil eder. Her bağlantı, iki istasyon arasında gidilme süresini (dakika) içerir.
- **Hatlar**: Her istasyon bir metro hattına aittir. Aktarmalar hatlar arası geçişleri temsil eder.

## ⚙️ Kullanılan Algoritmalar

### 1. BFS (Breadth-First Search) - En Az Aktarma

en_az_aktarma_bul fonksiyonu, BFS algoritması kullanılarak iki istasyon arasında en az aktarma yapılacak rotayı bulur.

#### 🔍 Nasıl Çalışır?

- İlk olarak kuyruğa başlangıç istasyonu eklenir.
- Ziyaret edilen istasyonlar listesi tutulur.
- Her adımda:
  - Kuyruktan bir istasyon alınır.
  - Komşuları sıraya eklenir (ziyaret edilmediyse).
- Hedef istasyona ulaşıldığında durur.

#### 📌 Avantajı:
- Rota üzerindeki adım sayısını (yani aktarma sayısını) en aza indirir.
- Süre önemsizdir, sadece istasyon sayısı önemlidir.

### 2. A* (A Star) - En Hızlı Rota

en_hizli_rota_bul fonksiyonu, A* algoritması ile en kısa sürede hedefe ulaşacak rotayı bulur.

#### 🔍 A* Algoritması Nedir?

A* (A Star) algoritması, en kısa veya en düşük maliyetli yolu bulmak için kullanılan çok güçlü ve yaygın bir yol bulma (pathfinding) algoritmasıdır. 
Hem Dijkstra algoritması gibi güvenilir, hem de önsezi (heuristic) kullanarak aramayı akıllı şekilde daraltabilen bir yapıya sahiptir.

#### 🔣 Kullanılan Formül:

f(n) = g(n) + h(n)

g(n): Başlangıçtan n düğümüne kadar olan gerçek maliyet (toplam süre)
h(n): n düğümünden hedefe olan tahmini maliyet (heuristic)


> Bu projede h(n) = 0 olarak alınmıştır . İleride gerçek mesafe/tahmin fonksiyonu eklenebilir. O Alınma nedeni şuan prode gerçek mesafe bilgisi yok bu yüzden tahmin oluşturulamadı.

#### 🔄 Adımlar:

1. Başlangıç istasyonu open_set adı verilen öncelik kuyruğuna eklenir.
2. Her adımda en düşük f(n) değerine sahip düğüm seçilir.
3. Seçilen düğümün komşuları değerlendirilir.
4. Daha kısa süreli yollar bulunursa güncellenir.
5. Hedefe ulaşıldığında en kısa süreli rota döndürülür.

#### 📌 Avantajı:

- Süre açısından en optimum yolu bulur.
- Öncelik kuyruğu sayesinde daha az düğüm gezerek sonuca ulaşabilir.

## 📁 Dosya Yapısı


metro_simulation/
│
├── metro_simulation.py      # Ana Python dosyası (algoritmalar ve sınıflar)
├── README.md                # Bu dökümantasyon dosyası


## 🧪 Örnek Senaryolar

### Senaryo 1: AŞTİ → OSB


En az aktarmalı rota: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB
En hızlı rota (24 dakika): AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB


### Senaryo 2: Batıkent → Keçiören


En az aktarmalı rota: Batıkent -> Demetevler -> Gar -> Keçiören
En hızlı rota (21 dakika): Batıkent -> Demetevler -> Gar -> Keçiören


## 📚 Geliştirme Önerileri

- **Heuristic Geliştirme**: h(n) fonksiyonu istasyonlar arası coğrafi mesafe veya hat geçiş maliyeti ile tahmin edilebilir.
- **Grafiksel Arayüz**: Kullanıcı arayüzü ile metro haritası görselleştirilebilir.
- **Dosya Girişi**: JSON/CSV ile metro hattı tanımlanabilir.

## 👤 Geliştirici

 **Svetlin Yosifov**  
 Akbank python ve yapay zekaya giris bootcamp projesi

## 🧠 Sonuç

Bu proje, hem BFS hem A* algoritmalarını gerçek dünya senaryosu olan metro ulaşımında başarıyla uygulayarak rota optimizasyonu yapar.
Kod yapısı temiz, algoritmalar iyi belgelenmiştir ve genişletmeye uygundur.
