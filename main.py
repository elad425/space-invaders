import pygame, sys
from player import Player
import obstical
from alien import Alien,Extra
from random import choice,randint
from laser import Laser


class Game:
    def __init__(self):
        self.player_sprite=Player((width/2,height),width,5)
        self.player=pygame.sprite.GroupSingle(self.player_sprite)

        self.lives=3
        self.live_surface=pygame.transform.scale(pygame.image.load('assets\\space invaders\\player.png'),(25,15))
        self.live_x_pos=10

        self.shape=obstical.shape
        self.block_size=5
        self.blocks=pygame.sprite.Group()
        self.obs_pos=[num * (width/4) for num in range(4)]
        self.create_mulobs(width/12,height-120,*self.obs_pos)

        self.aliens=pygame.sprite.Group()
        self.alien_setup(rows=6,cols=8)
        self.extra=pygame.sprite.GroupSingle()
        self.extra_timer=randint(700,900)
        self.alien_direction=1
        self.alien_laser=pygame.sprite.Group()

        music=pygame.mixer.Sound('assets\\space invaders\\music.wav')
        music.set_volume(0.2)
        music.play(-1)
        self.laser_sound=pygame.mixer.Sound('assets\\space invaders\\audio_laser.wav')
        self.explosion_sound=pygame.mixer.Sound('assets\\space invaders\\audio_explosion.wav')
        self.font=pygame.font.Font('assets\\space invaders\\Pixeled.ttf',50)

    def create_obs(self,x_start,y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col=='x':
                    x=x_start+col_index*self.block_size+offset_x
                    y=y_start+row_index*self.block_size
                    block=obstical.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_mulobs(self,x_start,y_start,*offset):
        for offset_x in offset:
            self.create_obs(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_dis=60,y_dis=50,x_offset=70,y_offset=60):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x= col_index*x_dis+x_offset
                y= row_index*y_dis+y_offset
                if row_index==0: alien_sprite=Alien('yellow',x,y)
                elif 1<=row_index<=2:alien_sprite=Alien('green',x,y)
                else: alien_sprite=Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_pos_check(self):
        all_aliens=self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right>=width:
                self.alien_direction=-1
                self.alien_down(2)
            elif alien.rect.left<=0:
                self.alien_direction=1
                self.alien_down(2)

    def alien_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y+=distance

    def alien_shot(self):
        if self.aliens:
            random_alien= choice(self.aliens.sprites())
            laser_sprite=Laser(random_alien.rect.center,-4)
            self.alien_laser.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_timer-=1
        if self.extra_timer<=0:
            self.extra.add(Extra(choice(['right','left']),width))
            self.extra_timer = randint(700, 900)

    def collision_check(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.aliens,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.lives+=1

        if self.alien_laser:
            for laser in self.alien_laser:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives-=1
                    self.explosion_sound.play()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for life in range(self.lives-1):
            x=self.live_x_pos+(life*(self.live_surface.get_size()[0]+10))
            screen .blit(self.live_surface,(x,6))

    def victory(self):
        if not self.aliens.sprites():
            victory_massage=self.font.render('you won',False,(250,250,250))
            victory_rect=victory_massage.get_rect(center=(width/2,height/2))
            screen.blit(victory_massage,victory_rect)

    def game_over(self):
        if self.lives<=0:
            self.game_over_massage()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=height:
                self.game_over_massage()

    def game_over_massage(self):
        massage = self.font.render('game over', False, (250, 250, 250))
        rect = massage.get_rect(center=(width / 2, height / 2))
        screen.blit(massage, rect)

    def buff(self):
        if not self.blocks:
            Player.obs_destroy(self.player_sprite)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_pos_check()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_check()
        self.display_lives()
        self.buff()

        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.alien_laser.update()

        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_laser.draw(screen)
        self.extra.draw(screen)
        self.victory()
        self.game_over()


if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    game = Game()

    alienlasers=pygame.USEREVENT+1
    pygame.time.set_timer(alienlasers,1000)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==alienlasers:
                game.alien_shot()

        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
