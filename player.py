import pygame,os
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,width,speed):
        super().__init__()
        self.image=pygame.transform.scale(pygame.image.load('assets\\space invaders\\player.png').convert_alpha(),(50,30))
        self.rect=self.image.get_rect(midbottom=pos)
        self.speed=speed
        self.screen_width=width
        self.ready=True
        self.laser_time=0
        self.laser_cooldown=600
        self.laser_sound=pygame.mixer.Sound('assets\\space invaders\\audio_laser.wav')

        self.lasers=pygame.sprite.Group()

    def get_input(self):
        keys=pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.rect.right<self.screen_width:
            self.rect.x+=self.speed
        elif keys[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x-=self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready=False
            self.laser_sound.play()
            self.laser_time=pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_time>=self.laser_cooldown:
                self.ready=True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center))

    def obs_destroy(self):
        self.laser_cooldown=100

    def update(self):
        self.get_input()
        self.recharge()
        self.lasers.update()


