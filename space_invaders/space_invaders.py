import pygame
import random

pygame.init()

screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('Space Invanders')


laser_sound = pygame.mixer.Sound("assets/laser.wav")
laser_sound.set_volume(0.25)

bg = pygame.image.load("assets/bg.png")


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




class SpaceShipBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect(center=(x, y))


    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1
        self.counter = 0


    def update(self):
        self.counter += 1
        
        self.rect.x += self.direction * 1

        if self.counter == 100:
            self.direction *= -1
            self.counter = 0


        for bullet in spaceship_bullet_group:
            if self.rect.colliderect(bullet.rect):
                self.kill()
                bullet.kill()





spaceship = SpaceShip()

spaceship_group = pygame.sprite.Group()
spaceship_bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()


spaceship_group.add(spaceship)


def generate_aliens():
    for x in range(50, 550, 100):
        for y in range(100, 500, 100):
            alien = Alien(x, y)
            alien_group.add(alien)

generate_aliens()

clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spaceship_group.update()
    spaceship_bullet_group.update()
    alien_group.update()



    screen.blit(bg, (0,0))
    spaceship_group.draw(screen)
    spaceship_bullet_group.draw(screen)
    alien_group.draw(screen)

    clock.tick(60)
    pygame.display.update()