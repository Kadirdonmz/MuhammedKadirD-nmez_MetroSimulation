# MuhammedKadirDonmez_MetroSimulation
# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)

## Proje Tanımı
Bu proje, bir metro ağında iki istasyon arasındaki en hızlı ve en az aktarmalı rotayı bulan bir simülasyon geliştirmeyi amaçlamaktadır. Proje kapsamında BFS (Breadth-First Search) ve A* algoritmaları kullanılarak farklı rota optimizasyonları gerçekleştirilecektir.

## Kullanılan Teknolojiler ve Kütüphaneler
- **Python 3.x**
- **collections** (deque veri yapısı için)
- **heapq** (A* algoritmasında öncelik kuyruğu için)

## Neden BFS ve A* Algoritmalarını Kullandık?
Metro simülasyonu için en uygun algoritmaları seçerken, verimli rota hesaplaması ve yolcu deneyimi ön planda tutulmuştur.

- **BFS (Breadth-First Search) Algoritması:**  
  BFS, graf üzerindeki düğümler arasında en kısa kenar sayısını bulmak için kullanılan bir tekniktir. Metro istasyonları genellikle düğümler olarak temsil edilir ve iki istasyon arasındaki geçişler kenar olarak kabul edilir. BFS’in en büyük avantajı, ağırlıksız bir graf için en kısa yolun garanti edilmesidir. Bu yüzden **en az aktarmalı rota** bulmak için idealdir.

- **A* (A-Star) Algoritması:**  
  A* algoritması, en kısa veya en hızlı rotayı bulmak için hem geçmiş maliyeti (g(n)) hem de tahmini maliyeti (h(n)) hesaba katan bir algoritmadır. Metro istasyonları arasındaki yolculuk süreleri farklı olduğu için, **en hızlı rota** hesaplamalarında BFS yetersiz kalır. A*, öncelik kuyruğu ve heuristik fonksiyon kullanarak daha verimli bir çözüm sunar.

## Algoritmaların Çalışma Mantığı
### BFS Algoritması (En Az Aktarmalı Rota)
- Bir kuyruk yapısı oluşturulur (collections.deque kullanılır).
- Ziyaret edilen istasyonlar takip edilir.
- Komşu istasyonlar keşfedilir ve en kısa rota belirlenir.

### A* Algoritması (En Hızlı Rota)
- Bir öncelik kuyruğu oluşturulur (heapq kullanılır).
- Ziyaret edilen istasyonlar takip edilir.
- Toplam süre hesaplanarak en hızlı rota belirlenir.
- Mevcut heuristic fonksiyonu, istasyon listesindeki indeks farkına dayalı olarak tahmini mesafe hesaplar.

### Örnek Kullanım ve Test Sonuçları
```sh
Başlangıç istasyonunun numarasını girin: 1
Hedef istasyonunun numarasını girin: 9
✔️ En az aktarmalı rota: Yenikapı (M1) -> Aksaray (M1) -> Taksim (M2) -> Levent (M2) -> Mecidiyeköy (M7)
🚀 En hızlı rota: Yenikapı (M1) -> Aksaray (M1) -> Taksim (M2) -> Zincirlikuyu (M2) -> Mecidiyeköy (M7)
⌛ Tahmini Süre: 32 dakika
```

## Kod Yapısı ve Sınıflar
### Istasyon Sınıfı
- Metro istasyonlarını temsil eder.
- Her istasyon bir **ad** ve **hat** bilgisine sahiptir.
- `komsu_ekle()` metodu ile bağlantı eklenir.

### MetroAgi Sınıfı
- Metro ağını ve istasyonlar arasındaki bağlantıları saklar.
- `istasyon_ekle()` metodu ile yeni istasyon eklenir.
- `baglanti_ekle()` metodu ile istasyonlar arası bağlantı eklenir.
- `en_az_aktarma_bul()` BFS algoritmasını kullanarak en az aktarmalı rotayı bulur.
- `en_hizli_rota_bul()` A* algoritmasını kullanarak en hızlı rotayı bulur.

## Projeyi Geliştirme Fikirleri
- Daha geniş bir metro ağı ekleyerek test etmek.
- Grafiksel bir arayüz ekleyerek rota görselleştirmesi yapmak.
- Gerçek zamanlı trafik durumu ve gecikmelerle simülasyonu güncellemek.
