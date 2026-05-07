"""
Komentare jsou pouze pro lektory, deti je nemusi cist ani psat.
Jsou pro lepsi pochopeni a rychlejsi vysvetleni co se kde deje
POZOR: Cesty k souborum davat pomoci `Copy relative path` nebo `Copy path`
"""

import pygame

# Zakladni konstanty
# Vysvetlete detem, proc pouzivame velka pismena (konvence pro konstanty)
# a proc je lepsi mit cisla na jednom miste (snadna zmena rozliseni hry, rychlosti).
SIRKA = 1000
VYSKA = 700
FPS = 60

# Barvy
# V pocitacich se barvy michaji ze tri zelemntu: Cervena (Red), Zelena (Green), Modra (Blue) -> RGB.
# Kazda slozka ma hodnotu 0-255. (255, 255, 255) je vsechno naplno = bila. (0, 0, 0) je tma = cerna.
BILA = (255, 255, 255)
CERNA = (0, 0, 0)
CERVENA = (255, 0, 0)
ZLUTA = (255, 255, 0)

# Fyzikalni konstanty
# GRAVITACE: Kazdy snimek se pricte k rychlosti padu.
# Cim vyssi cislo, tim rychleji pada.
# Tip pro deti: Zkuste zmenit na 0.1 (mesic) nebo 2.0 (jupiter).
GRAVITACE = 0.8

# SILA_SKOKU: Zaporne cislo, protoze v Pygame je Y=0 nahore a Y=1000 dole.
# Skok tedy zmensi Y (posun nahoru).
SILA_SKOKU = -16
VELIKOST_DLAZDICE = 50

# Mapa levelu
LEVEL_1 = [
    "....................",
    "....................",
    "....................",
    "......C.............",
    "......W.............",
    ".P....W...E.........",
    ".....WWWWWW.........",
    "...W......W...E.....",
    ".W..R..C.H..WWWWW...",
    "WWWWWWWWWWWWWWWWWWWW",
]

LEVEL_2 = [
    "....................",
    "....................",
    "....................",
    "......E.............",
    ".....WWW....C.......",
    ".P...C....WWWW......",
    "...WWW..............",
    "..........E...E.....",
    ".W...R...WWWWWWWW...",
    "WWWWWWWWWWWWWWWWWWWW",
]

SEZNAM_LEVELU = [LEVEL_1, LEVEL_2]
aktualni_level = 0

pygame.init()
# Vytvoreni okna (Surface), do ktereho budeme kreslit.
obrazovka = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Nas instagramater")
# Hodiny nam hlidaji rychlost hry, aby bezela stejne rychle na vsech PC.
hodiny = pygame.time.Clock()

pygame.mixer.init()


pygame.mixer.init()


# Funkce pro bezpecne nacitani zvuku
# Ucite deti osetrovat chyby (try-except) - kdyz soubor chybi, hra nespadne,
# jen nebude hrat zvuk. To je pro hrace lepsi nez pád hry.
def nacist_zvuk(cesta):
    try:
        return pygame.mixer.Sound(cesta)
    except:
        # Pokud soubor neexistuje nebo je poskozeny, program by spadl s chybou.
        # Blok 'except' tuto chybu zachyti a misto toho vypise nase hlaseni.
        # To je dulezite pro "user experience" - hrac vidi, co se stalo, a hra bezi dal (i kdyz bez zvuku).
        print(f"{cesta} nenalezena, proto nemas zvuky")
        return None


zvuk_mince = nacist_zvuk("assets/coin.wav")
zvuk_skok = nacist_zvuk("assets/jump.wav")
zvuk_powerup = nacist_zvuk("assets/powerup.wav")
zvuk_zraneni = nacist_zvuk("assets/hurt.wav")


# Pomocna funkce pro nacitani obrazku
# Zde se stara i o zmenu velikosti (transform.scale) a nahradni reseni.
# convert_alpha() je dulezite pro pruhlednost (napr. pruhledne okoli postavicky).
# transform.scale() zmensi/zvetsi obrazek na pozadovanou velikost dlazdice.
def nacist_obrazek(cesta, sirka, vyska, pripsana_barva):
    try:
        obrazek = pygame.image.load(cesta).convert_alpha()
        return pygame.transform.scale(obrazek, (sirka, vyska))
    except (FileNotFoundError, pygame.error):
        # Pokud obrazek chybi, vytvorime barevny obdelnik jako nahradu.
        print("POZOR! Pouzivam pripsanou barvu!")
        pozadi = pygame.Surface((sirka, vyska))
        pozadi.fill(pripsana_barva)
        return pozadi


# Hlavni funkce pro generovani levelu z textove mapy (pole stringu)
# Vysvetlete princip mrizky: Prochazime radek po radku, znak po znaku.
# Radek nam dava Y souradnici (radek 0 je nahore), sloupec dava X souradnici.
# Vynasobenim VELIKOST_DLAZDICE ziskame presne pixely na obrazovce.
# Kazdy znak reprezentuje jiny herni objekt na techto souradnicich.
def nacist_level(mapa):
    nove_platformy = []
    novi_nepratele = []
    nove_mince = []
    nove_powerupy = []
    hrac = Hrac()
    for radek_index, radek in enumerate(mapa):
        for sloupec_index, znak in enumerate(radek):
            x = sloupec_index * VELIKOST_DLAZDICE
            y = radek_index * VELIKOST_DLAZDICE

            if znak == "W":
                p = Platform(x, y, VELIKOST_DLAZDICE, VELIKOST_DLAZDICE)
                nove_platformy.append(p)

            elif znak == "E":
                n = Nepritel(x, y, x - 100, x + 100)
                novi_nepratele.append(n)

            elif znak == "C":
                m = Mince(x, y)
                nove_mince.append(m)

            elif znak == "P":
                hrac.rect.x = x
                hrac.rect.y = y

            elif znak == "H":
                p = Powerup(x, y, "heal")
                nove_powerupy.append(p)

            elif znak == "R":
                p = Powerup(x, y, "rychlost")
                nove_powerupy.append(p)

    return hrac, nove_platformy, novi_nepratele, nove_mince, nove_powerupy


# Trida predstavujici Hrace
# Obsahuje veškerou logiku pro pohyb, vykreslování a stav hráče (životy, powerupy).
class Hrac:
    def __init__(self):
        # self.rect = pygame.Rect(100, 300, 32, 32)
        # nacteme jeho obrazek
        self.sirka = 50
        self.vyska = 50
        self.image_vlevo = nacist_obrazek(
            "assets/hrac.png",
            self.sirka,
            self.vyska,
            CERVENA,
        )

        self.image_vpravo = pygame.transform.flip(self.image_vlevo, True, False)
        self.image = self.image_vlevo

        # pygame.Rect(x, y, sirka, vyska) nam vytvori neviditelny obdelnik kolem obrazku.
        # Pomaha nam se 2 vecmi:
        # 1. Pozice: Kde se hrac nachazi (self.rect.x, self.rect.y)
        # 2. Kolize: Zjisteni, jestli se dotyka jineho obdelniku (nepritele, zdi)
        # Rect je zakladni stavebni kamen pro fyziku v Pygame.
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300

        self.rychlost_x = 0
        self.rychlost_y = 0
        self.na_zemi = False

        self.zivoty = 3

        self.zakladni_rychlost = 5
        self.rychlost_behu = self.zakladni_rychlost
        self.cas_do_konce_powerupu = 0

        self.cas_do_konce_powerupu = 0

    # Metoda pro zpracování vstupu z klávesnice
    # Vysvetlete rozdil mezi jednorazovym stiskem (event) a drzenim klavesy.
    # pygame.key.get_pressed() vraci seznam vsech klaves a True/False
    # jestli jsou zrovna zmackle.
    # To se hodi pro plynuly pohyb (drzim sipku doprava -> postava bezi).
    def ovladani(self):
        tlacitka = pygame.key.get_pressed()

        # Pohyb do stran
        self.rychlost_x = 0
        if tlacitka[pygame.K_d] and self.rect.right < SIRKA:
            self.rychlost_x = self.rychlost_behu
            self.image = self.image_vpravo
        if tlacitka[pygame.K_a] and self.rect.left > 0:
            self.rychlost_x = -self.rychlost_behu
            self.image = self.image_vlevo

        # Gravitace - pohyb nahoru/dolu
        # Skok je mozny jen kdyz jsme na zemi (nemuzeme skakat ve vzduchu).
        # Vysvetlit: Proc kontrolujeme 'and self.na_zemi'? Aby neslo litat.
        if tlacitka[pygame.K_SPACE] and self.na_zemi:
            self.rychlost_y = SILA_SKOKU
            self.na_zemi = False
            if zvuk_skok:
                zvuk_skok.play()

    # Hlavni fyzikalni smycka hrace
    # Zde se aplikuje gravitace a pohyb. Vola se v kazdem snimku hry.
    def update(self):
        # 1. Aplikuj gravitaci (kazdy snimek padame rychleji...
        # ... dokud nenarazime na zem)
        self.rychlost_y += GRAVITACE
        # 2. Pohni obdelnikem (Rect) o spocitanou rychlost
        self.rect.x += self.rychlost_x
        self.rect.y += self.rychlost_y

        # Jednoducha kontrola, aby hrac nepropadl podlahou herního okna (dno obrazovky)
        if self.rect.bottom >= VYSKA:
            self.rect.bottom = VYSKA
            self.rychlost_y = 0
            self.na_zemi = True
        else:
            self.na_zemi = False

        # pokud powerup bezi
        if self.cas_do_konce_powerupu > 0:
            # tak pocitej cas od zacatku do konce powerupu
            if pygame.time.get_ticks() > self.cas_do_konce_powerupu:
                # skonci powerup (reset rychlosti)
                self.rychlost_behu = self.zakladni_rychlost
                self.cas_do_konce_powerupu = 0
                print("Rychlost vyprsela")

    def draw(self, pozadi):
        # pygame.draw.rect(pozadi, CERVENA, self.rect)
        pozadi.blit(self.image, self.rect)


class Platform:
    def __init__(self, x, y, sirka, vyska):
        # Platforma je jednoducha - ma jen obrazek a pozici (rect).
        # Nepohybuje se, takze nepotrebuje update() metodu, jen draw().
        self.image = nacist_obrazek(
            "assets/platform.png",
            sirka,
            vyska,
            (140, 70, 20),
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, pozadi):
        pozadi.blit(self.image, self.rect)


class Nepritel:
    def __init__(self, x, y, start_x, konec_x):
        self.image_vpravo = nacist_obrazek(
            "assets/nepritel.png",
            VELIKOST_DLAZDICE,
            VELIKOST_DLAZDICE,
            (0, 0, 255),
        )
        self.image_vlevo = pygame.transform.flip(self.image_vpravo, True, False)
        self.image = self.image_vpravo
        self.rect = self.image.get_rect()
        # souradnice kde se nachazi
        self.rect.x = x
        self.rect.y = y

        # hranice od-do kam muze chodit
        # Nepritel si pamatuje, kde se narodil (start_x) a kam az muze dojit (konec_x).
        self.start_x = start_x
        self.konec_x = konec_x
        self.rychlost = 2
        self.smer = 1  # 1 = doprava, -1 = doleva

    def update(self):
        # self.rect.x znamena ze pro nas objekt (Nepritele) menime x-ovou souradnici
        # Prictenim rychlosti se posune bud doprava (+2) nebo doleva (-2).
        self.rect.x += self.rychlost * self.smer

        # hlidkovani ze strany na stranu
        # Kdyz dojde na konec sve trasy (konec_x), otoci se (smer = -1)
        # a zmeni obrazek na levy.
        if self.rect.x >= self.konec_x:
            self.smer = -1
            self.image = self.image_vlevo
        elif self.rect.x <= self.start_x:
            self.smer = 1
            self.image = self.image_vpravo

    def draw(self, pozadi):
        pozadi.blit(self.image, self.rect)


class Mince:
    def __init__(self, x, y):
        self.image = nacist_obrazek(
            "assets/mince.png", 30, 30, ZLUTA
        )
        self.rect = self.image.get_rect()
        self.rect.x = x + 10
        self.rect.y = y + 10

    def draw(self, pozadi):
        pozadi.blit(self.image, self.rect)


class Powerup:
    # Powerup je specialni - muze mit ruzne efekty (typ = "heal" nebo "rychlost").
    # Podle typu mu nastavime jiny obrazek a barvu.
    def __init__(self, x, y, typ):
        self.typ = typ
        barva = (0, 255, 0)
        powerup_cesta = "assets/powerup.png"

        if self.typ == "heal":
            barva = (255, 192, 103)  # ruzova
            powerup_cesta = "assets/zivoty.png"
        elif self.typ == "rychlost":
            barva = (255, 255, 0)
            powerup_cesta = "assets/rychlost.png"

        self.image = nacist_obrazek(powerup_cesta, 30, 30, barva)
        self.rect = self.image.get_rect()
        self.rect.x = x + 10
        self.rect.y = y + 10

    def draw(self, pozadi):
        pozadi.blit(self.image, self.rect)


# Nahradni kod pro zacatky==================
# mario = Hrac()
# platformy = [
#     Platform(0, VYSKA - 40, SIRKA, 40),
#     Platform(200, 400, 150, 40),
#     Platform(500, 300, 150, 40),
# ]
# tapeta = nacist_obrazek(
#     r"/home/david/Documents/PODZIM2025/assets/levely/pozadi.png", SIRKA, VYSKA, CERNA
# )
# ====================


mario, platformy, nepratele, mince, powerupy = nacist_level(
    SEZNAM_LEVELU[aktualni_level]
)
font_skore = pygame.font.Font(None, 36)
skore = 0


def nacist_tapetu(aktualni_level):
    # nacteni dalsiho obrazku levelu
    if aktualni_level == 0:
        return nacist_obrazek(
            "assets/levely/pozadi.png",
            SIRKA,
            VYSKA,
            CERNA,
        )
    elif aktualni_level == 1:
        return nacist_obrazek(
            "assets/levely/atlantida.png",
            SIRKA,
            VYSKA,
            CERNA,
        )
    return None


tapeta = nacist_tapetu(aktualni_level)
# Toto je srdce hry, ktere bezi stale dokola (např. 60x za sekundu).
hra_bezi = True
while hra_bezi:
    # 1. Zpracovani udalosti (napr. stisk krizku pro zavreni okna)
    # Pygame si pamatuje vsechny udalosti (kliknuti, klavesy), ktere se staly od minuleho snimku.
    # Musime je projit a zkontrolovat, jestli hrac nechce hru vypnout.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hra_bezi = False

    mario.ovladani()
    mario.update()

    # prozatimni konec levelu
    if mario.rect.right >= SIRKA:
        aktualni_level += 1
        # pokud mame aktualni_level mensi nez pocet levelu v seznamu
        if aktualni_level < len(SEZNAM_LEVELU):
            # nacitame dalsi level v poradi
            mario, platformy, nepratele, mince, powerupy = nacist_level(
                SEZNAM_LEVELU[aktualni_level]
            )
            # ====================
            tapeta = nacist_tapetu(aktualni_level=aktualni_level)
            # ====================
        else:
            print("VYHRAL JSI")
            hra_bezi = False

    for nepritel in nepratele:
        nepritel.update()

    # 2. Reseni kolizi
    # Je dulezite kontrolovat kolize az po pohybu (update), abychom hrace "vytlacili" z prekazky.
    # kolize hrac vs plaforma
    # Princip: Projdeme vsechny plosiny a zeptame se: "Dotykam se te?" (colliderect)
    mario.na_zemi = False
    for platforma in platformy:
        if mario.rect.colliderect(platforma.rect):
            # Detekce dopadu shora:
            # Puvodne jsem byl nad plosinou (bottom < top)
            # a pohybuji se smerem dolu (rychlost_y > 0)
            if mario.rect.bottom < platforma.rect.bottom and mario.rychlost_y > 0:
                mario.rect.bottom = platforma.rect.top
                mario.rychlost_y = 0
                mario.na_zemi = True

    # Detekce stretu s nepritelem
    # Rozlisujeme skok na hlavu (zniceni nepritele) vs. naraz ze strany (zraneni hrace).
    # kolize nepritel vs hrac
    for nepritel in nepratele:
        if mario.rect.colliderect(nepritel.rect):
            # jak mario pada? Zvetsuje se je Y
            # jak zjistim ze dopadl na nepritele? coliderect
            # kam musi dopadnout na nepritele? rect.bottom -> rect.centery+20
            # Pokud padame shora (rychlost_y > 0) a jsme spodkem tela nad stredem
            # nepritele, je to skok na hlavu.
            if mario.rychlost_y > 0 and mario.rect.bottom < nepritel.rect.centery + 20:
                nepratele.remove(nepritel)
                # Odraz se od nepritele nahoru
                mario.rychlost_y = -14
            else:
                # Jinak jsme do nej narazili ze strany -> zraneni
                mario.zivoty -= 1
                if zvuk_zraneni:
                    zvuk_zraneni.play()
                if mario.zivoty <= 0:
                    print("GAME OVER")
                    hra_bezi = False
                else:
                    # mario umrel -> restart
                    print("Jauvajs, to to boli")
                    mario.rect.x = 100
                    mario.rect.y = 300

    # kolize hrac vs mince
    # mince.copy() = mince[:]
    for m in mince[:]:
        if mario.rect.colliderect(m.rect):
            mince.remove(m)
            skore += 10
            if zvuk_mince:
                zvuk_mince.play()

    # kolize s powerupy
    # Tady vidime vyhodu trid - muzeme se zeptat powerupu "jaky jsi typ?" (p.typ)
    for p in powerupy[:]:
        if mario.rect.colliderect(p.rect):
            powerupy.remove(p)
            if zvuk_powerup:
                zvuk_powerup.play()

            if p.typ == "heal":
                mario.zivoty += 1
                print(f"Tvoje zivoty: {mario.zivoty}")
            elif p.typ == "rychlost":
                mario.rychlost_behu += 3
                # Nastavime casovac - aktualni cas + 5000 milisekund (5 sekund)
                mario.cas_do_konce_powerupu = pygame.time.get_ticks() + 5000

    # ====================
    # 3. Vykreslovani (Rendering)
    # Poradi je dulezite! Nejdriv pozadi, pak objekty (aby byly videt "na" pozadi).
    # ====================
    if tapeta:
        # blit(co, kam) - nekresli obrazek na pozadi na souradnice [0, 0] (levy horni roh)
        obrazovka.blit(tapeta, (0, 0))
    else:
        # Kdyz nemame obrazek, vybarvime obrazovku cernou barvou (smazeme minuly snimek)
        obrazovka.fill(CERNA)
    # ====================

    for platformu in platformy:
        platformu.draw(obrazovka)

    for nepritel in nepratele:
        nepritel.draw(obrazovka)

    for m in mince:
        m.draw(obrazovka)

    for p in powerupy:
        p.draw(obrazovka)

    text = font_skore.render(f"Skore: {skore}", True, CERVENA)
    obrazovka.blit(text, (10, 10))

    mario.draw(obrazovka)
    # Preklopeni bufferu - zobrazeni toho, co jsme nakreslili
    # Pocitac si pripravuje snimek v pameti a az je hotovy, 'flipne' ho na monitor.
    # Diky tomu nevidime problikavani vykreslovani.
    pygame.display.flip()
    # Pockej chvilku, abychom meli stabilnich 60 snimku za vterinu (FPS)
    hodiny.tick(FPS)

# Uklid po sobe - zavreni okna a vypnuti Pygame
pygame.quit()
