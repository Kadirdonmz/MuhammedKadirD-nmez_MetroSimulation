from collections import deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, ad: str, hat: str):
        # İstasyonun adı ve hattını belirler
        self.ad = ad
        self.hat = hat
        # Komşu istasyonlarla bağlantılarını tutan liste
        self.komsular: List[Tuple['Istasyon', int]] = []

    def __repr__(self):
        # İstasyonun adını ve hattını yazdırmak için
        return f"{self.ad} ({self.hat})"

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        # Komşu istasyon ekler (geçiş süresi ile birlikte)
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        # İstasyonları ve hatları tutan sözlükler
        self.istasyonlar: Dict[int, Istasyon] = {}
        self.numara_istasyon: Dict[str, List[int]] = {}

    def istasyon_ekle(self, numara: int, ad: str, hat: str) -> None:
        # Yeni bir istasyon ekler
        if numara not in self.istasyonlar:
            istasyon = Istasyon(ad, hat)
            self.istasyonlar[numara] = istasyon
            if ad not in self.numara_istasyon:
                self.numara_istasyon[ad] = []
            self.numara_istasyon[ad].append(numara)

    def baglanti_ekle(self, num1: int, num2: int, sure: int) -> None:
        # İki istasyon arasında bağlantı ekler
        istasyon1 = self.istasyonlar[num1]
        istasyon2 = self.istasyonlar[num2]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_num: int, hedef_num: int) -> Optional[List[Istasyon]]:
        # BFS algoritması ile en az aktarmalı rotayı bulur
        if baslangic_num not in self.istasyonlar or hedef_num not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_num]
        hedef = self.istasyonlar[hedef_num]
        kuyruk = deque([(baslangic, [baslangic])])  # Kuyruk: (mevcut istasyon, yol)
        ziyaret_edildi = set()  # Ziyaret edilen istasyonlar
        
        while kuyruk:
            mevcut, yol = kuyruk.popleft()
            if mevcut == hedef:
                return yol  # Hedefe ulaşıldığında yolu döndür
            
            for komsu, _ in mevcut.komsular:
                if (komsu, komsu.hat) not in ziyaret_edildi:
                    ziyaret_edildi.add((komsu, komsu.hat))
                    kuyruk.append((komsu, yol + [komsu]))  # Yeni istasyonları kuyruğa ekle
        
        return None

    def heuristic(self, istasyon: Istasyon, hedef: Istasyon) -> int:
        # A* algoritması için heuristic fonksiyonu (istasyonlar arasındaki tahmini mesafe)
        istasyonlar_listesi = list(self.istasyonlar.values())
        return abs(istasyonlar_listesi.index(istasyon) - istasyonlar_listesi.index(hedef))

    def en_hizli_rota_bul(self, baslangic_num: int, hedef_num: int) -> Optional[Tuple[List[Istasyon], int]]:
        # A* algoritması ile en hızlı rotayı ve süresini bulur
        if baslangic_num not in self.istasyonlar or hedef_num not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_num]
        hedef = self.istasyonlar[hedef_num]
        pq = [(0, 0, id(baslangic), baslangic, [baslangic])]  # (g_cost, h_cost, istasyon id'si, istasyon, yol)
        ziyaret_edildi = {}  # Ziyaret edilen istasyonlar ile geçiş süresi
        
        while pq:
            toplam_sure, heuristik_deger, _, mevcut, yol = heapq.heappop(pq)
            
            if mevcut == hedef:
                return yol, toplam_sure  # Hedefe ulaşıldığında rota ve süreyi döndür

            if (mevcut, mevcut.hat) in ziyaret_edildi and ziyaret_edildi[(mevcut, mevcut.hat)] <= toplam_sure:
                continue

            ziyaret_edildi[(mevcut, mevcut.hat)] = toplam_sure
            
            for komsu, gecis_suresi in mevcut.komsular:
                ekstra_sure = 7 if mevcut.hat != komsu.hat else 0  # Hat değişikliği için ek süre
                g_cost = toplam_sure + gecis_suresi + ekstra_sure
                h_cost = self.heuristic(komsu, hedef)  # Heuristic değeri (tahmini mesafe)
                heapq.heappush(pq, (g_cost, h_cost, id(komsu), komsu, yol + [komsu]))  # Komşuyu kuyruğa ekle

        return None

def main():
    metro = MetroAgi()

    # İstasyonları ekle
    istasyonlar = [
        (1, "Yenikapı", "M1"), (2, "Aksaray", "M1"), (3, "Taksim", "M2"),
        (4, "Levent", "M2"), (5, "Kadıköy", "M4"), (6, "Ayrılık Çeşmesi", "M4"),
        (7, "Üsküdar", "M5"), (8, "Altunizade", "M5"), (9, "Mecidiyeköy", "M7"),
        (10, "Şişli", "M7"), (11, "Mahmutbey", "M7"), (12, "Bağcılar", "M1"),
        (13, "Atatürk Havalimanı", "M1"), (14, "Halkalı", "Marmaray"),
        (15, "Gayrettepe", "M2"), (16, "Zincirlikuyu", "M2"), (17, "Söğütlüçeşme", "Marmaray")
    ]

    for numara, ad, hat in istasyonlar:
        metro.istasyon_ekle(numara, ad, hat)

    # Bağlantıları ekle
    baglantilar = [
        (1, 2, 3), (2, 3, 5), (3, 4, 4), (4, 9, 6),
        (5, 6, 3), (6, 7, 2), (7, 8, 4), (8, 9, 5),
        (9, 10, 2), (10, 11, 4), (11, 12, 5), (12, 13, 6), (13, 14, 8),
        (4, 15, 2), (15, 16, 3), (16, 9, 2), (6, 17, 5), (17, 14, 6)
    ]

    for num1, num2, sure in baglantilar:
        metro.baglanti_ekle(num1, num2, sure)

    print("\n=== Metro Simülasyonu ===")
    print("\nMevcut istasyonlar:")
    for num, istasyon in metro.istasyonlar.items():
        print(f"{num}: {istasyon.ad} ({istasyon.hat})")
    
    try:
        # Kullanıcıdan başlangıç ve hedef istasyonu al
        baslangic = int(input("\nBaşlangıç istasyonunun numarasını girin: "))
        hedef = int(input("Hedef istasyonunun numarasını girin: "))
        
        if baslangic not in metro.istasyonlar or hedef not in metro.istasyonlar:
            print("❌ Geçersiz istasyon numarası!❌ ")
            return
        
        print("\n=== Sonuçlar ===\n")
        
        # En az aktarmalı rotayı bul
        rota = metro.en_az_aktarma_bul(baslangic, hedef)
        if rota:
            print("✔️ En az aktarmalı rota: " + " -> ".join([f"{ist.ad} ({ist.hat})" for ist in rota]))
        
        # En hızlı rotayı ve tahmini süreyi bul
        hizli_rota, hizli_sure = metro.en_hizli_rota_bul(baslangic, hedef)
        if hizli_rota:
            print("🚀 En hızlı rota: " + " -> ".join([f"{ist.ad} ({ist.hat})" for ist in hizli_rota]))
            print(f"⌛ Tahmini Süre: {hizli_sure} dakika")
    except ValueError:
        print("❌ Geçerli bir sayı girin!❌ ")

if __name__ == "__main__":
    main()
