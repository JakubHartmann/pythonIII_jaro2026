import pygame
pygame.init()

screen=pygame.display.set_mode((800, 800))
running = True
pygame.image.load("assets/spaceship.png")


class Lod:
    def __init__(self,x,y):
        self.image=pygame.image.load("assets/spaceship.png")
        self.pos=(x,y)
        
        self.rect=self.image.get_rect(topright=(self.pos))

    def show(self):
        screen.blit(self.image,self.rect)

    def move(self):
        for event in pygame.event.get():
            if event.key == pygame.K_d:
                self.rect.x += 5
                

hrac=Lod(250,250)

while running:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    hrac.move()        
    
    hrac.show()
    pygame.display.update()