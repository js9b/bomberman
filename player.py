import pygame
from datetime import datetime
import map

class Player(object):

    def __init__(self, game, start, img_path):
        self.img = pygame.image.load(img_path)#.convert()
        self.size= game.size
        self.rect = pygame.Rect(start*self.size, start*self.size, self.size, self.size) #gracz
        self.set_bomb = 900 #900 można stawiać, 1000 wybuch, inny - odliczanie
        self.explosion = 90
        self.bomb_pos=[0,0]
        self.bomb_ex_pos = [0,0]
        self.game = game
        self.image = pygame.transform.scale(self.img, (self.size, self.size ))
        self.lives=1
        self.bomb_img = pygame.transform.scale(pygame.image.load("img/1.png"), (self.size, self.size))#
        self.bomb_ex_img = pygame.transform.scale(pygame.image.load("img/3.png"), (self.size, self.size))#srodek eksplozji
        self.bomb_ex2_img = pygame.transform.scale(pygame.image.load("img/4.png"), (self.size, self.size))#boki eksplozji

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in map.generate_walls(self.size)[0]: # map.l(self.size)[0] -  zwraca ściany
            self.check_walls(wall, dx, dy)

        for wall in map.generate_walls(self.size)[1]: #map.l(self.size)[0] -  zwraca boxy do rozbicia
            self.check_walls(wall, dx, dy)

    def check_walls(self, wall, dx, dy): #kolizja ze sciankami i boxami
        if self.rect.colliderect(wall.rect):
            if dx > 0:  # prawo
                self.rect.right = wall.rect.left
            if dx < 0:  # lewo
                self.rect.left = wall.rect.right
            if dy > 0:  # dol
                self.rect.bottom = wall.rect.top
            if dy < 0:  # gora
                self.rect.top = wall.rect.bottom

    def press(self):
        speed=2
        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            self.game.players[0].move(-speed, 0)
        if key[pygame.K_d]:
            self.game.players[0].move(speed, 0)
        if key[pygame.K_w]:
            self.game.players[0].move(0, -speed)
        if key[pygame.K_s]:
            self.game.players[0].move(0, speed)
        if key[pygame.K_z]:
            if self.game.players[0].set_bomb==900:
                self.game.players[0].set_bomb=1000

        if key[pygame.K_LEFT]:
            self.game.players[1].move(-speed, 0)
        if key[pygame.K_RIGHT]:
            self.game.players[1].move(speed, 0)
        if key[pygame.K_UP]:
            self.game.players[1].move(0, -speed)
        if key[pygame.K_DOWN]:
            self.game.players[1].move(0, speed)
        if key[pygame.K_SPACE]:
            if self.game.players[1].set_bomb==900:
                self.game.players[1].set_bomb=1000

    def set_b(self):
        for p in self.game.players:
            if p.set_bomb==1000: #stawianie bomby
                p.bomb_pos[0] = round(p.rect.x / self.size)
                p.bomb_pos[1] = round(p.rect.y / self.size)
                p.set_bomb =datetime.now().second

            if  datetime.now().second-p.set_bomb==2 or datetime.now().second-p.set_bomb==-58: # print("wybuch") bomby
                map.mod(p.bomb_pos[1],p.bomb_pos[0] , self.size)

                p.set_bomb = 900
                if p.explosion==90:
                    import copy
                    p.bomb_ex_pos = copy.copy(p.bomb_pos)
                    p.explosion = datetime.now().second

            if p.set_bomb != 900 and p.set_bomb!=1000: # "wypalanie" lontu
                self.game.screen.blit(p.bomb_img, (p.bomb_pos[0]*self.size, p.bomb_pos[1]*self.size, self.size, self.size))

            if datetime.now().second-p.explosion==1 or datetime.now().second-p.explosion==-59: #Flara znika, koniec eksplozji
                p.explosion = 90

            if p.explosion != 90 : #widoczna flara
                self.game.screen.blit(p.bomb_ex_img, (p.bomb_ex_pos[0] * self.size, p.bomb_ex_pos[1] * self.size, self.size, self.size))
                if p.rect.colliderect(pygame.Rect((p.bomb_ex_pos[0]) * self.size, p.bomb_ex_pos[1] * self.size, self.size,self.size)): #kolija z flarą
                    p.lives =0
                if map.level_int[p.bomb_ex_pos[1]][(p.bomb_ex_pos[0])-1]==2:
                    flar_rect = ((p.bomb_ex_pos[0] - 1) * self.size, p.bomb_ex_pos[1] * self.size, self.size, self.size)
                    self.draw_flar(flar_rect, 90, p)

                if map.level_int[p.bomb_ex_pos[1]][(p.bomb_ex_pos[0])+1]==2:
                    flar_rect=((p.bomb_ex_pos[0]+1)  * self.size, p.bomb_ex_pos[1] * self.size, self.size, self.size)
                    self.draw_flar(flar_rect, 270, p)

                if map.level_int[(p.bomb_ex_pos[1])-1][p.bomb_ex_pos[0]]==2:
                    flar_rect=((p.bomb_ex_pos[0])  * self.size, (p.bomb_ex_pos[1]-1) * self.size, self.size, self.size)
                    self.draw_flar(flar_rect, 0, p)

                if map.level_int[(p.bomb_ex_pos[1])+1][p.bomb_ex_pos[0]]==2:
                    flar_rect=((p.bomb_ex_pos[0])  * self.size, (p.bomb_ex_pos[1]+1) * self.size, self.size, self.size)
                    self.draw_flar(flar_rect, 180, p)

    def draw_flar(self, flar_rect, angle, p):
        self.game.screen.blit(pygame.transform.rotate(p.bomb_ex2_img, angle), (flar_rect))
        for pl in self.game.players:
            if pl.rect.colliderect(pygame.Rect(flar_rect)):
                pl.lives = 0