import pygame
import random

pygame.init()

SIRKA_POLICKA = 20
NAHORU = (0, -1)
DOLU = (0, 1)
DOLEVA = (-1, 0)
DOPRAVA = (1, 0)

SIRKA_OBRAZOVKY = 800
VYSKA_OBRAZOVKY = 700

class Had():
    def __init__(self):
        self.telo = [(100,100), (120,100), (140, 100), (140, 120), (140, 100)]
        self.smer = NAHORU
        self.pocitadlo = 0


    def ukaz(self):
        for cast in self.telo:
            pygame.draw.rect(okno, "green", (cast[0], cast[1], SIRKA_POLICKA, SIRKA_POLICKA))
            pygame.draw.rect(okno, "black", (cast[0], cast[1], SIRKA_POLICKA, SIRKA_POLICKA), 1)



    def pohni_se(self):
        self.pocitadlo += 1

        if self.pocitadlo >= 10:
            hlava = self.telo[0]
            nove_x = hlava[0] + self.smer[0] * SIRKA_POLICKA
            nove_y = hlava[1] + self.smer[1] * SIRKA_POLICKA

            self.telo.insert(0, (nove_x, nove_y))
            if not self.kolize_s_jidlem():
                self.telo.pop()

            self.pocitadlo = 0

        
    def kolize_s_jidlem(self):
        hlava = pygame.rect.Rect(self.telo[0][0], self.telo[0][1], SIRKA_POLICKA, SIRKA_POLICKA)
        if hlava.colliderect(jidlo.rect):
            jidlo.generuj_jidlo()
            return True
        
        return False


    def naraz(self):
        hlava = self.telo[0]
        if hlava[0] < 0 or hlava[0] > SIRKA_OBRAZOVKY - SIRKA_POLICKA or hlava[1] < 0 or hlava[1] > VYSKA_OBRAZOVKY - SIRKA_POLICKA:
            return True
        
        hlava = self.telo[0]
        for index, cast in enumerate(self.telo):
            if index == 0:
                continue
            if cast[0] == hlava[0] and cast[1] == hlava[1]:
                return True
        
        return False


class Jidlo():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rect = None
        self.generuj_jidlo()


    def generuj_jidlo(self):
        self.x = random.randint(0, (SIRKA_OBRAZOVKY // SIRKA_POLICKA) - 1) * SIRKA_POLICKA
        self.y = random.randint(0, (VYSKA_OBRAZOVKY // SIRKA_POLICKA) - 1) * SIRKA_POLICKA

        while (self.x, self.y) in had.telo:
            self.x = random.randint(0, (SIRKA_OBRAZOVKY // SIRKA_POLICKA) - 1) * SIRKA_POLICKA
            self.y = random.randint(0, (VYSKA_OBRAZOVKY // SIRKA_POLICKA) - 1) * SIRKA_POLICKA

        self.rect = pygame.rect.Rect(self.x, self.y, SIRKA_POLICKA, SIRKA_POLICKA)


    def ukaz(self):
        pygame.draw.rect(okno, "red", (self.x, self.y, SIRKA_POLICKA, SIRKA_POLICKA))
        pygame.draw.rect(okno, "black", (self.x, self.y, SIRKA_POLICKA, SIRKA_POLICKA), 1)






okno = pygame.display.set_mode((SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY))
hodiny = pygame.time.Clock()

had = Had()
jidlo = Jidlo()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and had.smer != DOLU:
                had.smer = NAHORU
            if event.key == pygame.K_s and had.smer != NAHORU:
                had.smer = DOLU
            if event.key == pygame.K_a and had.smer != DOPRAVA:
                had.smer = DOLEVA
            if event.key == pygame.K_d and had.smer != DOLEVA:
                had.smer = DOPRAVA


    had.pohni_se()
    konec = had.naraz()

    okno.fill("Orange")
    had.ukaz()
    jidlo.ukaz()

    if konec:
        running = False


    hodiny.tick(60)
    pygame.display.update()



