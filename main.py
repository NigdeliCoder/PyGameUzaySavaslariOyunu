#BM TASARIM ÇALIŞMASI-1 EMRE TURAÇ "PYGAME İLE MASAÜSTÜ OYUN GELİŞTİRİLMESİ"
#UZAY GEMİSİ SAVAŞLARI

#En başta projede gerekli olan temel python kütüphanelerini ve "pygame" için gerekli olan kütüphaneyi projeye dahil ettim.
import pygame
import os
import time
import random
import pygame, sys
from pygame import mixer

pygame.font.init()

from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3

root = Tk()
root.title("Uzay Gemisi Savaşları Kullanıcı Giriş / Kayıt Ekranı")

#Kullanıcı kayıt ve giriş işlemleri için gerekli arayüzün ve veritabanı tanımlarının yapılması
GENISLIK = 600
YUKSEKLIK = 450
EKRAN_GENISLIK = root.winfo_screenwidth()
EKRAN_YUKSEKLIK = root.winfo_screenheight()
x = (EKRAN_GENISLIK / 2) - (GENISLIK / 2)
y = (EKRAN_YUKSEKLIK / 2) - (YUKSEKLIK / 2)
root.geometry("%dx%d+%d+%d" % (GENISLIK, YUKSEKLIK, x, y))
root.resizable(0, 0)

#Veritabanı değişken adları tanıımlarının yapaılması
KULLANICI_AD = StringVar()
KULLANICI_SIFRE = StringVar()
KULLANICI_EMAIL = StringVar()
KULLANICI_YAS = StringVar()


#Veritabanının tanımlanması
def Veritabani():
    global conn, cursor
    conn = sqlite3.connect("kullanici.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `kullanici` (kullanici_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, kullanici_ad TEXT, kullanici_sifre TEXT, kullanici_email TEXT, kullanici_yas TEXT)")

#Çıkış işleminin tanımlanması
def Cikis():
    sonuc = tkMessageBox.askquestion('System', 'Çıkmak istediğinize emin misiniz?', icon="warning")
    if sonuc == 'yes':
        root.destroy()
        exit()

#Kullanıcı giriş formu ekranının tanımlanması
def GirisFormu():
    global GirisEkrani, sonuc1_etiket
    GirisEkrani = Frame(root)
    GirisEkrani.pack(side=TOP, pady=80)
    kullanici_ad_etiket = Label(GirisEkrani, text="Kullanici Adı:", font=('arial', 25), bd=18)
    kullanici_ad_etiket.grid(row=1)
    kullanici_sifre_etiket = Label(GirisEkrani, text="Şifre:", font=('arial', 25), bd=18)
    kullanici_sifre_etiket.grid(row=2)
    sonuc1_etiket = Label(GirisEkrani, text="", font=('arial', 18))
    sonuc1_etiket.grid(row=3, columnspan=2)
    kullanici_ad = Entry(GirisEkrani, font=('arial', 20), textvariable=KULLANICI_AD, width=15)
    kullanici_ad.grid(row=1, column=1)
    kullanici_sifre = Entry(GirisEkrani, font=('arial', 20), textvariable=KULLANICI_SIFRE, width=15, show="*")
    kullanici_sifre.grid(row=2, column=1)
    giris_butonu = Button(GirisEkrani, text="Giriş", font=('arial', 18), width=35, command=Giris)
    giris_butonu.grid(row=4, columnspan=2, pady=20)
    kayit_etiket = Label(GirisEkrani, text="Kayıt Ol", fg="Blue", font=('arial', 12))
    kayit_etiket.grid(row=0, sticky=W)
    kayit_etiket.bind('<Button-1>', KayitEkraniGecis)

#Kullanıcı kayıt formu ekranının tanımlanması
def KayitFormu():
    global KayitEkrani, sonuc2_etiket
    KayitEkrani = Frame(root)
    KayitEkrani.pack(side=TOP, pady=40)
    kullanici_ad_etiket = Label(KayitEkrani, text="Kullanıcı Adı:", font=('arial', 18), bd=18)
    kullanici_ad_etiket.grid(row=1)
    kullanici_sifre_etiket = Label(KayitEkrani, text="Şifre:", font=('arial', 18), bd=18)
    kullanici_sifre_etiket.grid(row=2)
    kullanıcı_email_etiket = Label(KayitEkrani, text="E-mail:", font=('arial', 18), bd=18)
    kullanıcı_email_etiket.grid(row=3)
    kullanici_yas_etiket = Label(KayitEkrani, text="Yaş:", font=('arial', 18), bd=18)
    kullanici_yas_etiket.grid(row=4)
    sonuc2_etiket = Label(KayitEkrani, text="", font=('arial', 18))
    sonuc2_etiket.grid(row=5, columnspan=2)
    kullanici_ad = Entry(KayitEkrani, font=('arial', 20), textvariable=KULLANICI_AD, width=15)
    kullanici_ad.grid(row=1, column=1)
    kullanici_sifre = Entry(KayitEkrani, font=('arial', 20), textvariable=KULLANICI_SIFRE, width=15, show="*")
    kullanici_sifre.grid(row=2, column=1)
    kullanici_email = Entry(KayitEkrani, font=('arial', 20), textvariable=KULLANICI_EMAIL, width=15)
    kullanici_email.grid(row=3, column=1)
    kullanici_yas = Entry(KayitEkrani, font=('arial', 20), textvariable=KULLANICI_YAS, width=15)
    kullanici_yas.grid(row=4, column=1)
    giris_butonu = Button(KayitEkrani, text="Kayıt Ol", font=('arial', 18), width=35, command=Kaydol)
    giris_butonu.grid(row=6, columnspan=2, pady=20)
    giris_butonu = Label(KayitEkrani, text="Login", fg="Blue", font=('arial', 12))
    giris_butonu.grid(row=0, sticky=W)
    giris_butonu.bind('<Button-1>', GirisEkraniGecis)

#Giriş ekranı ile kayıt ekranı arasında geçiş yapısı tanımlanması
def GirisEkraniGecis(event=None):
    KayitEkrani.destroy()
    GirisFormu()

#Kayıt formu ekranı ile giriş formu ekranı arasında geçiş yapısının tanımlanması
def KayitEkraniGecis(event=None):
    GirisEkrani.destroy()
    KayitFormu()

#Kayıt işlevini tanımlayan ve kayıt verilerini veritabanına eklenmesinin sağlanması
def Kaydol():
    Veritabani()
    if KULLANICI_AD.get == "" or KULLANICI_SIFRE.get() == "" or KULLANICI_EMAIL.get() == "" or KULLANICI_YAS.get == "":
        sonuc2_etiket.config(text="Tüm alanları doldurunuz.", fg="orange")
    else:
        cursor.execute("SELECT * FROM `kullanici` WHERE `kullanici_ad` = ?", (KULLANICI_AD.get(),))
        if cursor.fetchone() is not None:
            sonuc2_etiket.config(text="Kullanıcı adı zaten kayıtlı", fg="red")
        else:
            cursor.execute("INSERT INTO `kullanici` (kullanici_ad, kullanici_sifre, kullanici_email, kullanici_yas) VALUES(?, ?, ?, ?)",
                           (str(KULLANICI_AD.get()), str(KULLANICI_SIFRE.get()), str(KULLANICI_EMAIL.get()), str(KULLANICI_YAS.get())))
            conn.commit()
            KULLANICI_AD.set("")
            KULLANICI_SIFRE.set("")
            KULLANICI_EMAIL.set("")
            KULLANICI_YAS.set("")
            sonuc2_etiket.config(text="Kayıt başarılı", fg="black")
        cursor.close()
        conn.close()

#Giriş işlevinin tanımlanması
def Giris():
    Veritabani()
    if KULLANICI_AD.get == "" or KULLANICI_SIFRE.get() == "":
        sonuc1_etiket.config(text="Tüm alanları doldurunuz!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `kullanici` WHERE `kullanici_ad` = ? and `kullanici_sifre` = ?",
                       (KULLANICI_AD.get(), KULLANICI_SIFRE.get()))
        if cursor.fetchone() is not None:
            sonuc1_etiket.config(text="Giriş Başarılı", fg="blue")
            root.destroy()
        else:
            sonuc1_etiket.config(text="Geçersiz/hatalı kullanıcı adı veya şifre girdiniz.", fg="red")


GirisFormu()

#Menü çubuğu ilevlerinin tanımlanması
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Cikis)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


if __name__ == '__main__':
    root.mainloop()

#Oyun yapısı ile ilgili kodların başlangıcı
pygame.init()
mixer.init()
mixer.music.load('sesler/interstellarmaintheme.mp3')
mixer.music.play(-1)

#Oyunun oynanacağı masaüstü pencereye ait geenişlik,yükseklik ve çözünürlük ayarlarının yapılması
GENISLIK, YUKSEKLIK = 750 , 750
EKRAN = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Uzay Gemisi Savaşları")

#Oyuna ait grafiklerin projeye dahil edilmesi
KIRMIZI_DUSMAN_UZAY_GEMISI = pygame.image.load(os.path.join("grafikler", "kirmizi_dusman_uzay_gemisi.png"))
YESIL_DUSMAN_UZAY_GEMISI = pygame.image.load(os.path.join("grafikler", "yesil_dusman_uzay_gemisi.png"))
MAVI_DUSMAN_UZAY_GEMISI = pygame.image.load(os.path.join("grafikler", "mavi_dusman_uzay_gemisi.png"))

#Oyuncu uzay gemisine ait grafiklerin projeye dahil edilmesi
OYUNCU_UZAY_GEMISI = pygame.image.load(os.path.join("grafikler", "oyuncu_uzay_gemisi.png"))

#Lazerlere ait grafiklerin projeye dahil edilmesi
KIRMIZI_LAZER = pygame.image.load(os.path.join("grafikler", "kirmizi_lazer.png"))
YESIL_LAZER = pygame.image.load(os.path.join("grafikler", "yesil_lazer.png"))
MAVI_LAZER = pygame.image.load(os.path.join("grafikler", "mavi_lazer.png"))
OYUNCU_LAZER = pygame.image.load(os.path.join("grafikler", "oyuncu_lazer.png"))

#Oyun arkaplan grafiğinin proje ye dahil edilmesi
ARKAPLAN = pygame.transform.scale(pygame.image.load(os.path.join("grafikler", "arkaplan_uzay.jpg")), (GENISLIK, YUKSEKLIK))
Menu = pygame.image.load(os.path.join("grafikler", "menu.jpg"))

#lazerlere ait sınıfın tanımlanarak Python'un nesneye yönelimli programlama özelliğinden faydalandım.
#Lazer sınıfında x,y yer yön koordinatları grafik için img değişkeni tanımladım.
class Lazer:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

#Çizdirme işlevi için gerekli tanımlamaların yapılması
    def cizdir(self, window):
        window.blit(self.img, (self.x, self.y))

#Hareket işlevi için gerekli tanımlamaların yapılması(Hız parametresi ile birlikte)
    def hareket(self, hiz):
        self.y += hiz

#Pencere dışı durumlarla ilgili yükseklik ayarını kontrol edecek yapının tanımlanması
    def ekran_disi(self, height):
        return not(self.y <= height and self.y >= 0)


#Oyundaki çarpışma durumları için gerekli tanımlamaların yapılması
    def carpisma(self, obj):
        return carpisma_durumu(self, obj)

#skor tanımları


#Oyundaki uzay gemileri ile ilgili kodlarda kullanılacak Gemi sınıfının tanımlanması ve ilgili parametrelerin eklenmesi
class Gemi:
    M = 30

    def __init__(self, x, y, can=100):
        self.x = x
        self.y = y
        self.can = can
        self.gemi_img = None
        self.lazer_img = None
        self.lazerler = []
        self.m_sayac = 0

    def cizdir(self, window):
        window.blit(self.gemi_img, (self.x, self.y))
        for lazer in self.lazerler:
            lazer.cizdir(window)


#Lazerlere hareket işlevini kazandıran yapının tanımlanması
    def hareket_lazerler(self, hiz, obj):
        self.m()
        for lazer in self.lazerler:
            lazer.hareket(hiz)
            if lazer.ekran_disi(YUKSEKLIK):
                self.lazerler.remove(lazer)
            elif lazer.carpisma(obj):
                obj.can -= 5
                self.lazerler.remove(lazer)

    def m(self):
        if self.m_sayac >= self.M:
            self.m_sayac = 0
        elif self.m_sayac > 0:
            self.m_sayac += 1

#Atış işlevine dair yapının tanımlanması
    def atis(self):
        if self.m_sayac == 0:
            lazer = Lazer(self.x, self.y, self.lazer_img)
            self.lazerler.append(lazer)
            self.m_sayac = 1

#Genişlik verisini almayı sağlayan tanımlama
    def get_width(self):
        return self.gemi_img.get_width()

#Yükseklik verisini almayı sağlayan tanımlama
    def get_height(self):
        return self.gemi_img.get_height()


#Oyunda yer alan oyuncuya ait sınıfın tanımlanması ve Gemi sınıfı ile bağlantı kurulması
class Oyuncu(Gemi):
    def __init__(self, x, y, can=100):
        super().__init__(x, y, can)
        self.gemi_img = OYUNCU_UZAY_GEMISI
        self.lazer_img = OYUNCU_LAZER
        self.mask = pygame.mask.from_surface(self.gemi_img)
        self.max_can = can

    def hareket_lazerler(self, hiz, objs):
        self.m()
        for lazer in self.lazerler:
            lazer.hareket(hiz)
            if lazer.ekran_disi(YUKSEKLIK):
                self.lazerler.remove(lazer)
            else:
                for obj in objs:
                    if lazer.carpisma(obj):
                        objs.remove(obj)
                        if lazer in self.lazerler :
                            self.lazerler.remove(lazer)

    #Aralarda oyunda oluşan durumları ekranda göstermek için cizdir tanımlamasının kullanılması
    def cizdir(self, window):
        super().cizdir(window)
        self.can_cubugu(window)

#Oyuncu gemisine ait can değerini gösteren çubuğun tanımlanması
    def can_cubugu(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.gemi_img.get_height() + 10, self.gemi_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.gemi_img.get_height() + 10, self.gemi_img.get_width() * (self.can/self.max_can), 10))

#Dusman sınıfının tanımlanması ve Gemi sınıfndan bağlantı kurulması
class Dusman(Gemi):
    RENKLER = {
                "red": (KIRMIZI_DUSMAN_UZAY_GEMISI, KIRMIZI_LAZER),
                "green": (YESIL_DUSMAN_UZAY_GEMISI, YESIL_LAZER),
                "blue": (MAVI_DUSMAN_UZAY_GEMISI, MAVI_LAZER)
                }
#renklere ait tanımlamaların yapılması
    def __init__(self, x, y, renk, can=100):
        super().__init__(x, y, can)
        self.gemi_img, self.lazer_img = self.RENKLER[renk]
        self.mask = pygame.mask.from_surface(self.gemi_img)

    def hareket(self, hiz):
        self.y += hiz

    def atis(self):
        if self.m_sayac == 0:
            lazer = Lazer(self.x-20, self.y, self.lazer_img)
            self.lazerler.append(lazer)
            self.m_sayac = 1

#Çarpışma durumu ile ilgili gerekli tanımlamaların yapılması
def carpisma_durumu(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None



#main yapısının tanımlanması ve içerisinde gerekli değişkenleri ve oyunun başındaki değişken değerlerinin tanımlanması.
def main():
    calistir = True
    skor = 0
    FPS = 60
    seviye = 0
    kacirilan_dusman = 0
    main_font = pygame.font.SysFont("comicsans", 30)
    yanma_durumu_font = pygame.font.SysFont("comicsans", 60)

    dusmanlar = []
    dalga_boyutu = 5
    dusman_hiz = 1

    oyuncu_hiz = 5
    lazer_hiz = 5

    oyuncu = Oyuncu(300, 630)

    clock = pygame.time.Clock()

    yanma_durumu = False
    yanma_durumu_sayac = 0

    #oyunda değişen durumlardan sonra ekrana yeni durum yazdırılıyor.
    def yeniden_cizdir():
        EKRAN.blit(ARKAPLAN, (0,0))
        kacirilan_dusman_etiket = main_font.render(f"Kaçırılan düşman: {kacirilan_dusman}", 1, (255,255,255))
        skor_etiket = main_font.render(f"Skor: {skor}", 1, (255,255,255))
        seviye_etiket = main_font.render(f"Seviye: {seviye}", 1, (255,255,255))

        EKRAN.blit(kacirilan_dusman_etiket, (10, 10))
        EKRAN.blit(skor_etiket, (GENISLIK - skor_etiket.get_width() - 10, 70))
        EKRAN.blit(seviye_etiket, (GENISLIK - seviye_etiket.get_width() - 10, 10))

        for dusman in dusmanlar:
            dusman.cizdir(EKRAN)

        oyuncu.cizdir(EKRAN)

#Oyunun bitme durumu ile ilgili mantıksal tanımlamaların yapılması
        if yanma_durumu:
            yanma_durumu_etiket = yanma_durumu_font.render("Oyun Sona Erdi.!", 1, (255,255,255))
            EKRAN.blit(yanma_durumu_etiket, (GENISLIK/2 - yanma_durumu_etiket.get_width()/2, 350))

        pygame.display.update()

#calistir mantuksal durumuna göre while döngüsü ile oyun oynanış kodlarının sürekli çalıştırılması
    while calistir:
        clock.tick(FPS)
        yeniden_cizdir()

        if kacirilan_dusman == 10 or oyuncu.can <= 0:
            yanma_durumu = True
            yanma_durumu_sayac += 1

        if yanma_durumu:
            if yanma_durumu_sayac > FPS * 3:
                calistir = False
            else:
                continue

        if len(dusmanlar) == 0:
            seviye += 1


            dalga_boyutu += 5
            for i in range(dalga_boyutu):
                dusman = Dusman(random.randrange(50, GENISLIK-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                dusmanlar.append(dusman)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

#Oyuna ait kontrol tuşlarının tanımlanması
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] and oyuncu.x - oyuncu_hiz > 0:
            oyuncu.x -= oyuncu_hiz
        if tuslar[pygame.K_RIGHT] and oyuncu.x + oyuncu_hiz + oyuncu.get_width() < GENISLIK:
            oyuncu.x += oyuncu_hiz
        if tuslar[pygame.K_UP] and oyuncu.y - oyuncu_hiz > 0:
            oyuncu.y -= oyuncu_hiz
        if tuslar[pygame.K_DOWN] and oyuncu.y + oyuncu_hiz + oyuncu.get_height() + 15 < YUKSEKLIK:
            oyuncu.y += oyuncu_hiz
        if tuslar[pygame.K_SPACE]:
            oyuncu.atis()
            atis_ses = mixer.Sound('sesler/atis.wav')
            atis_ses.play()

        for dusman in dusmanlar[:]:
            dusman.hareket(dusman_hiz)
            dusman.hareket_lazerler(lazer_hiz, oyuncu)

            if random.randrange(0, 2*60) == 1:
                dusman.atis()

            if carpisma_durumu(dusman, oyuncu):
                oyuncu.can -= 5
                skor +=10
                dusmanlar.remove(dusman)
            elif dusman.y + dusman.get_height() > YUKSEKLIK :
                kacirilan_dusman += 1
                skor -=10
                dusmanlar.remove(dusman)

        oyuncu.hareket_lazerler(-lazer_hiz, dusmanlar)
#oyunun işleyişine dair menünün tanımlanması




def main_menu():
    baslik_font = pygame.font.SysFont("comicsans", 40)
    aciklama_font = pygame.font.SysFont("comicsans", 20)

    calistir = True
    while calistir:

        EKRAN.blit(Menu, (0,0))

        baslik_etiket = baslik_font.render("UZAY GEMİSİ SAVAŞLARI", 1, (255,255,255))
        basla_etiket = baslik_font.render("Oynamak için fareyi tıklatın.", 1, (255,255,255))
        kontol_etiket = aciklama_font.render("Yön tuşları ile hareket edebilir ve SPACE BAR ile ateş edebilirsin.", 1, (255,255,255))

        EKRAN.blit(baslik_etiket, (YUKSEKLIK/2 - baslik_etiket.get_width()/2, 170))
        EKRAN.blit(basla_etiket, (YUKSEKLIK/2 - basla_etiket.get_width()/2, 350))
        EKRAN.blit(kontol_etiket, (YUKSEKLIK/2 - kontol_etiket.get_width()/2, 550))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calistir = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()

