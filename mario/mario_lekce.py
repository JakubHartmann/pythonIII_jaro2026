import pygame


VYSKA_OBRAZOVKY = 700
SIRKA_OBRAZOVKY = 1000

VELIKOST_KOSTKY = 50


pygame.init()


screen = pygame.display.set_mode((SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY))


def load_image(path, width, height):
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (width, height)).convert_alpha()
    except:
        image = pygame.surface.Surface((width, height))
        image.fill("Brown")
    

    return image


LEVEL_1 = [
    "....................",
    "....................",
    ".WWWWWW.............",
    "....................",
    ".............WWWW...",
    "....................",
    ".....WWWWWW.........",
    "....................",
    "............WWWWW...",
    "WWWWWWWWWWWWWWWWWWWW",
]


def generate_level(level):
    platforms = []

    for index_radku, radek in enumerate(level):
        for index_sloupce, policko in enumerate(radek):
            if policko == "W":
                platform = Platform(index_sloupce * VELIKOST_KOSTKY, index_radku * VELIKOST_KOSTKY)
                platforms.append(platform)

    return platforms
        






class Platform:
    def __init__(self, x, y):
        self.image = load_image("assets/zeme.png", VELIKOST_KOSTKY, VELIKOST_KOSTKY)
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self):
        screen.blit(self.image, self.rect)



class Player:
    def __init__(self, x, y):
        self.image = load_image("assets/hrac.png", VELIKOST_KOSTKY, 75)
        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(x, y))



    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= 7
            self.image = self.image_left
            

        if keys[pygame.K_d]:
            self.rect.x += 7
            self.image = self.image_right



    def draw(self):
        screen.blit(self.image, self.rect)


bg = load_image("assets/levely/pozadi.png", SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY)
platforms = generate_level(LEVEL_1)
player = Player(100, 100)

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    player.update()

    screen.blit(bg, (0, 0))

    for platform in platforms:
        platform.draw()


    clock.tick(60)
    player.draw()

    pygame.display.update()



