import pygame
import random
import sys
sys.setrecursionlimit(2000)

# Oyun tahtası boyutları
GENISLIK = 800
YUKSEKLIK = 600

# Renkler
SIYAH = (0, 0, 0)
YESIL = (0, 255, 0)

# Yılanın boyutları
YILAN_BOYUTU = 20

# FPS (Frame Per Second) ayarı
FPS = 60

# Pygame başlatılıyor
pygame.init()

# Oyun tahtası oluşturuluyor
tahta = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu")

# FPS kontrolcüsü oluşturuluyor
fps_kontrol = pygame.time.Clock()

# Yılanın başlangıç konumu
yilan_baslangic_x = GENISLIK // 2
yilan_baslangic_y = YUKSEKLIK // 2

# Yılanın başlangıç hızı ve yönü
yilan_hizi_x = YILAN_BOYUTU
yilan_hizi_y = 0

# Yılanın vücudu
yilan_vucut = []
yilan_uzunlugu = 1

# Yem oluşturuluyor
yem_x = round(random.randrange(0, GENISLIK - YILAN_BOYUTU) / 20.0) * 20.0
yem_y = round(random.randrange(0, YUKSEKLIK - YILAN_BOYUTU) / 20.0) * 20.0

# Yılanın DFS için yolu tutan stack
yol_stack = []

# DFS algoritması
def dfs(yilan_bas_x, yilan_bas_y, hedef_x, hedef_y, ziyaret_edilen):
    if (yilan_bas_x, yilan_bas_y) == (hedef_x, hedef_y):
        return True

    ziyaret_edilen.add((yilan_bas_x, yilan_bas_y))

    hareketler = [(YILAN_BOYUTU, 0), (-YILAN_BOYUTU, 0), (0, YILAN_BOYUTU), (0, -YILAN_BOYUTU)]

    for hareket in hareketler:
        yeni_x = yilan_bas_x + hareket[0]
        yeni_y = yilan_bas_y + hareket[1]

        if yeni_x >= GENISLIK or yeni_x < 0 or yeni_y >= YUKSEKLIK or yeni_y < 0:
            continue

        if (yeni_x, yeni_y) in yilan_vucut:
            continue

        if (yeni_x, yeni_y) in ziyaret_edilen:
            continue

        if dfs(yeni_x, yeni_y, hedef_x, hedef_y, ziyaret_edilen):
            yol_stack.append((hareket[0], hareket[1]))
            return True

    return False

# Yılanın hareketini güncelleme
def yilan_hareket():
    global yilan_baslangic_x, yilan_baslangic_y, yilan_hizi_x, yilan_hizi_y

    if not yol_stack:
        dfs(yilan_baslangic_x, yilan_baslangic_y, yem_x, yem_y, set())

    if yol_stack:
        hareket = yol_stack.pop()
        yilan_hizi_x, yilan_hizi_y = hareket[0], hareket[1]

    yilan_baslangic_x += yilan_hizi_x
    yilan_baslangic_y += yilan_hizi_y

# Skor değişkeni
skor = 0

# Skor metni için font ve boyut
font = pygame.font.Font(None, 36)

# Renk listesi
renk_listesi_yilan = [(0, 0, 255), (255, 255, 255), (255, 0, 0), (255, 255, 0), (255, 165, 0)]
renk_index_yilan = 0
yilan_rengi = renk_listesi_yilan[renk_index_yilan]

renk_listesi_tahta = [(169, 169, 169), (0, 0, 0), (139, 0, 0), (255, 182, 193), (255, 105, 180)]
renk_index_tahta = 0
tahta_rengi = renk_listesi_tahta[renk_index_tahta]

# Skor metnini ekranda gösterme fonksiyonu
def skor_goster():
    skor_metni = font.render("Skor: " + str(skor), True, YESIL)
    tahta.blit(skor_metni, (10, 10))

# Oyun döngüsü
oyun_devam_ediyor = True
while oyun_devam_ediyor:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            oyun_devam_ediyor = False

    # Yılanın hareketini güncelleme
    yilan_hareket()

    # Yılanın oyun tahtasından çıkmasını engelleme
    if yilan_baslangic_x >= GENISLIK or yilan_baslangic_x < 0 or yilan_baslangic_y >= YUKSEKLIK or yilan_baslangic_y < 0:
        oyun_devam_ediyor = True

    # Yılanın yemi yemesi durumu
    if yilan_baslangic_x == yem_x and yilan_baslangic_y == yem_y:
        yem_x = round(random.randrange(0, GENISLIK - YILAN_BOYUTU) / 20.0) * 20.0
        yem_y = round(random.randrange(0, YUKSEKLIK - YILAN_BOYUTU) / 20.0) * 20.0
        yilan_uzunlugu += 1
        skor += 1  # Skoru artırma

        # Yılan rengini değiştirme
        renk_index_yilan = (renk_index_yilan + 1) % len(renk_listesi_yilan)
        yilan_rengi = renk_listesi_yilan[renk_index_yilan]

        # Oyun tahtası rengini değiştirme
        renk_index_tahta = (renk_index_tahta + 1) % len(renk_listesi_tahta)
        tahta_rengi = renk_listesi_tahta[renk_index_tahta]

    tahta.fill(tahta_rengi)
    skor_goster()

    # Yılanın vücudu güncelleniyor
    yilan_bas = []
    yilan_bas.append(yilan_baslangic_x)
    yilan_bas.append(yilan_baslangic_y)
    yilan_vucut.append(yilan_bas)
    if len(yilan_vucut) > yilan_uzunlugu:
        del yilan_vucut[0]

    # Yılanın kendine çarpmasını kontrol etme
    for segment in yilan_vucut[:-1]:
        if segment == yilan_bas:
            oyun_devam_ediyor = True

    # Yılanın vücudu çiziliyor
    for segment in yilan_vucut:
        pygame.draw.rect(tahta, yilan_rengi, [segment[0], segment[1], YILAN_BOYUTU, YILAN_BOYUTU])

    # Yem çiziliyor
    pygame.draw.rect(tahta, YESIL, [yem_x, yem_y, YILAN_BOYUTU, YILAN_BOYUTU])

    # Ekran güncelleniyor
    pygame.display.update()

    # FPS ayarı
    fps_kontrol.tick(FPS)

# Oyun döngüsünden çıkıldığında pygame kapatılıyor
pygame.quit()
