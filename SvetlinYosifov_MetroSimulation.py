""" 
Bu kod, bir metro ağı oluşturmak ve ardından belirli iki istasyon arasında en az aktarma yaparak veya
en hızlı şekilde seyahat etmek için gerekli olan rota ve süreyi bulmak için kullanılır.
"""
from collections import defaultdict, deque #deque modülü ilk giren ilk çıkar mantığı ile çalışır
import heapq #heapq modülü öncelik kuyruğu yapısını sağlar, en küçük elemanı çıkartır
from typing import Dict, List, Optional, Tuple 


class Istasyon: #Istasyon sınıfı oluşturuldu amacı istasyonların özelliklerini ve komşularını tutmak
    def __init__(self, idx: str, ad: str, hat: str):    
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (Istasyon, sure) tuple'ları listesi

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int): #komsu_ekle fonksiyonu oluşturuldu
        self.komsular.append((istasyon, sure))   #komsular listesine istasyon ve süre eklendi

    def __repr__(self): #repr fonksiyonu ile istasyonların ad ve hat bilgileri döndürüldü
        return f"{self.ad} ({self.hat})"


class MetroAgi: #MetroAgi sınıfı oluşturuldu amacı istasyonları ve hatları tutmak
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}  
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None: #istasyon_ekle ile hatta bulunan istasyonlar eklendi
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

        #bağlantı ekleme fonksiyonu ile istasyonlar arasındaki bağlantılar eklendi
    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None: 
        ist1 = self.istasyonlar[istasyon1_id]
        ist2 = self.istasyonlar[istasyon2_id]
        ist1.komsu_ekle(ist2, sure)
        ist2.komsu_ekle(ist1, sure)

        #BFS algoritması kullanarak en az aktarma yaparak rota bulan fonksiyon ile rota bulundu
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]: 
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: #başlangıç ve hedef istasyonlar kontrol edildi
            return None
        baslangic = self.istasyonlar[baslangic_id] #başlangıç istasyonu belirlendi
        hedef = self.istasyonlar[hedef_id]  #hedef istasyonlar belirlendi
        ziyaret_edildi = set() #ziyaret edilen istasyonlar set yapısında oluşturuldu
        kuyruk = deque([(baslangic, [baslangic])]) #kuyruk yapısı oluşturuldu
        while kuyruk: #kuyruk boş olana kadar döngü çalıştı
            istasyon, rota = kuyruk.popleft()   #kuyruktan istasyon ve rota çekildi
            if istasyon == hedef: #eğer istasyon hedefe eşitse rota döndürüldü
                return rota
            if istasyon in ziyaret_edildi:  #eğer istasyon ziyaret edildiyse döngü devam etti
                continue 
            ziyaret_edildi.add(istasyon)    #ziyaret edilen istasyonlar set yapısına eklendi
            for komsu, _ in istasyon.komsular: 
                if komsu not in ziyaret_edildi: #eğer komşu ziyaret edilmediyse kuyruğa eklendi
                    kuyruk.append((komsu, rota + [komsu]))
        return None #rota bulunamazsa None döndürüldü


        # A* algoritması kullanarak en hızlı rotayı bulan fonksiyon ile en hızlı rota bulundu
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: #başlangıç ve hedef istasyonlar kontrol edildi
            return None #başlangıç ve hedef istasyonlar yoksa None döndürüldü
        baslangic = self.istasyonlar[baslangic_id]  #başlangıç istasyonu belirlendi
        hedef = self.istasyonlar[hedef_id] #hedef istasyonu belirlendi
        ziyaret_edildi = set()  #ziyaret edilen istasyonlar set yapısında oluşturuldu
        pq = [(0, id(baslangic), baslangic, [baslangic])] #öncelik kuyruğu oluşturuldu
        while pq: #öncelik kuyruğu boş olana kadar döngü çalıştı
            toplam_sure, _, istasyon, rota = heapq.heappop(pq) #öncelik kuyruğundan istasyon ve rota çekildi
            if istasyon == hedef: #eğer istasyon hedefe eşitse rota ve toplam süre döndürüldü  
                return rota, toplam_sure 
            if id(istasyon) in ziyaret_edildi: #eğer istasyon ziyaret edildiyse döngü devam etti
                continue
            ziyaret_edildi.add(id(istasyon)) #ziyaret edilen istasyonlar set yapısına eklendi   
            for komsu, sure in istasyon.komsular: #komsular ve süreler döngü ile gezildi
                if id(komsu) not in ziyaret_edildi: #eğer komşu ziyaret edilmediyse öncelik kuyruğuna eklendi
                    heapq.heappush(pq, (toplam_sure + sure, id(komsu), komsu, rota + [komsu])) 
        return None
    
if __name__ == "__main__": 
    metro = MetroAgi() #MetroAgi sınıfından metro nesnesi oluşturuldu
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===") 
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:") #AŞTİ'den OSB'ye gitmek için en az aktarma ve en hızlı rota bulundu
    rota = metro.en_az_aktarma_bul("M1", "K4") #en_az_aktarma_bul fonksiyonu ile en az aktarma yaparak rota bulundu
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota)) #rota yazdırıldı
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4") #en_hizli_rota_bul fonksiyonu ile en hızlı rota bulundu
    if sonuc:
        rota, sure = sonuc #rota ve süre değişkenlerine atandı
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))  #rota ve süre yazdırıldı
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 

    # Senaryo 4: Kızılay'dan Keçiören'e
    print("\n4. Kızılay'dan Keçiören'e:")
    rota = metro.en_az_aktarma_bul("K1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("K1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
