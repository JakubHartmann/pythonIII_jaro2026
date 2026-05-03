import pygame


pygame.init()


try:
    image = pygame.image.load("assets/zeme.png")
    print("Obrazek nacten")
except:
    print("Stala se chyba")


print("Konec souboru")

