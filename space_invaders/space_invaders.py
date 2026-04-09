import pygame 

pygame.init()

screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('Space Invanders')


laser_sound = pygame.mixer.Sound("assets/laser.wav")
laser_sound.set_volume(0.25)


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/spaceship.png")
        self.rect = self.image.get_rect(center=(300,600))
        self.last_shot = pygame.time.get_ticks()

 
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        now = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and now - self.last_shot > 500:
            self.last_shot = now
            laser_sound.play()
            spaceship_bullet_group.add(SpaceShipBullet(self.rect.centerx, self.rect.centery))

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.fill("Orange")


class SpaceShipBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect(center=(x, y))


    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()



spaceship = SpaceShip()

spaceship_group = pygame.sprite.Group()
spaceship_bullet_group = pygame.sprite.Group()

spaceship_group.add(spaceship)

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spaceship_group.update()
    spaceship_bullet_group.update()



    screen.fill("Black")
    spaceship_group.draw(screen)
    spaceship_bullet_group.draw(screen)

    clock.tick(60)
    pygame.display.update()