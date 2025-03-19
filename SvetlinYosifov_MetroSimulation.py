from collections import defaultdict, deque # Kuyruk ve sözlük veri yapıları için
import heapq # Öncelik kuyruğu veri yapısı için
from typing import Dict, List, Set, Tuple, Optional  # Tür belirleme için kullanılır



class Istasyon: # İstasyon sınıfı
    def __init__(self, idx: str, ad: str, hat: str): # İstasyon sınıfı için __init__ fonksiyonu 
        self.idx = idx # İstasyon id'si atanır
        self.ad = ad    # İstasyon adı atanır
        self.hat = hat  # İstasyonun bağlı olduğu hat adı atanır
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları listesi oluşturulur ve boş bir liste atanır

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int): # İstasyon sınıfı için komsu_ekle fonksiyonu
        self.komsular.append((istasyon, sure)) # İstasyonun komsular listesine (istasyon, süre) tuple'ı eklenir

class MetroAgi:
    def __init__(self): # MetroAgi sınıfı için __init__ fonksiyonu
        self.istasyonlar: Dict[str, Istasyon] = {} # istasyonlar sözlüğü istasyon id'si ile eşleşir ve istasyon nesnesini içerir
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list) # hatlar sözlüğü hat adı ile eşleşir ve istasyon listesini içerir

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None: # İstasyon ekleme fonksiyonu 
        if id not in self.istasyonlar: # Eğer istasyonlar sözlüğünde istasyon id'si yoksa
            istasyon = Istasyon(idx, ad, hat)  # İstasyon nesnesi oluşturulur
            self.istasyonlar[idx] = istasyon # İstasyonlar sözlüğüne istasyon id'si ile eşleşir ve istasyon nesnesi atanır
            self.hatlar[hat].append(istasyon) # Hatlar sözlüğüne hat adı ile eşleşir ve istasyon nesnesi eklenir

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None: # Bağlantı ekleme fonksiyonu
        istasyon1 = self.istasyonlar[istasyon1_id] # İstasyonlar sözlüğünden istasyon1_id'ye karşılık gelen istasyon nesnesi alınır
        istasyon2 = self.istasyonlar[istasyon2_id] # İstasyonlar sözlüğünden istasyon2_id'ye karşılık gelen istasyon nesnesi alınır
        istasyon1.komsu_ekle(istasyon2, sure) # İstasyon1'in komsular listesine (istasyon2, süre) tuple'ı eklenir
        istasyon2.komsu_ekle(istasyon1, sure) # İstasyon2'nin komsular listesine (istasyon1, süre) tuple'ı eklenir
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        #BFS algoritması kullanarak en az aktarmalı rotayı bulur 
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: # Eğer başlangıç ve hedef istasyonlar sözlükte yoksa 
            return None #Bu, geçersiz girişlerin önüne geçmek için yapılan bir kontroldür ve none döndürülür
        baslangic = self.istasyonlar[baslangic_id] # Başlangıç istasyonu alınır
        hedef = self.istasyonlar[hedef_id] # Hedef istasyonu alınır
        ziyaret_edildi = {baslangic} # Ziyaret edilen istasyonlar kümesi oluşturulur ve başlangıç istasyonu eklenir
        kuyruk = deque([(baslangic, [baslangic])]) # Kuyruk oluşturulur ve başlangıç istasyonu ve başlangıç istasyonu listesi eklenir
        while kuyruk: # Kuyruk boş olana kadar
            istasyon, rota = kuyruk.popleft() # Kuyruktan bir istasyon ve o istasyona giden rota alınır
            if istasyon == hedef: # Eğer istasyon hedef istasyon ise
                return rota # Rota döndürülür
            for komsu, _ in istasyon.komsular: # İstasyonun komsuları üzerinde dolaşılır
                if komsu not in ziyaret_edildi: # Eğer komsu ziyaret edilmediyse
                    ziyaret_edildi.add(komsu) # Komsu ziyaret edildi olarak işaretlenir
                    kuyruk.append((komsu, rota + [komsu])) # Kuyruğa komsu ve komsuya giden rota eklenir
        return None # Rota bulunamazsa None döndürülür  
    
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        #A* algoritması kullanarak en hızlı rotayı bulur
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: # Eğer başlangıç ve hedef istasyonlar sözlükte yoksa
            return None
        baslangic = self.istasyonlar[baslangic_id] # Başlangıç istasyonu alınır
        hedef = self.istasyonlar[hedef_id] # Hedef istasyonu alınır
        ziyaret_edildi = set() # Ziyaret edilen istasyonlar kümesi oluşturulur
        pq = [(0, id(baslangic), baslangic, [baslangic])] # Öncelik kuyruğu oluşturulur ve başlangıç istasyonu ve başlangıç istasyonu listesi eklenir
        while pq:
            _, _, istasyon, rota = heapq.heappop(pq) # Öncelik kuyruğundan bir istasyon ve o istasyona giden rota alınır
            if istasyon == hedef: # Eğer istasyon hedef istasyon ise
                toplam_sure = sum(sure for _, sure in rota) # Rota üzerindeki süreler toplanır
                return rota, toplam_sure # Rota ve toplam süre döndürülür
            if id(istasyon) in ziyaret_edildi: # Eğer istasyon ziyaret edildiyse
                continue # Sonraki adıma geçilir
            ziyaret_edildi.add(id(istasyon)) # İstasyon ziyaret edildi olarak işaretlenir
            for komsu, sure in istasyon.komsular: # İstasyonun komsuları üzerinde dolaşılır
                if id(komsu) not in ziyaret_edildi: # E
                    heapq.heappush(pq, (sure, id(komsu), komsu, rota + [komsu])) # Öncelik kuyruğuna komsu, komsuya giden rota ve toplam süre eklenir
        return None # Rota bulunamazsa None döndürülür      

        
        """En az aktarmalı rotayı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. BFS algoritmasını kullanarak en az aktarmalı rotayı bulun
        3. Rota bulunamazsa None, bulunursa istasyon listesi döndürün
        4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın
        
        İpuçları:
        - collections.deque kullanarak bir kuyruk oluşturun, HINT: kuyruk = deque([(baslangic, [baslangic])])
        - Ziyaret edilen istasyonları takip edin
        - Her adımda komşu istasyonları keşfedin
        """
        # TODO: Bu fonksiyonu tamamlayın
        pass 
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: # Eğer başlangıç ve hedef istasyonlar sözlükte yoksa
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = {baslangic}        


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. A* algoritmasını kullanarak en hızlı rotayı bulun
        3. Rota bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) tuple'ı döndürün
        4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın
        
        İpuçları:
        - heapq modülünü kullanarak bir öncelik kuyruğu oluşturun, HINT: pq = [(0, id(baslangic), baslangic, [baslangic])]
        - Ziyaret edilen istasyonları takip edin
        - Her adımda toplam süreyi hesaplayın
        - En düşük süreye sahip rotayı seçin
        """
        # TODO: Bu fonksiyonu tamamlayın
        pass
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
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
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
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


