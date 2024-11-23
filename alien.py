import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path='assets\\space invaders\\'+color+'.png'
        self.image=pygame.image.load(file_path).convert_alpha()
        self.rect= self.image.get_rect(topleft=(x,y))

    def update(self,direction):
        self.rect.x+=direction

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,width):
        super().__init__()
        self.image=pygame.image.load('assets\\space invaders\\extra.png')
        if side=='right':
            x=width+50
            self.speed=-3
        else:
            x=-50
            self.speed=3
        self.rect=self.image.get_rect(topleft=(x,30))

    def update(self):
        self.rect.x+=self.speed
