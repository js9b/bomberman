import pygame, sys, pygame_menu
import map
from player import Player

class Game():
    def __init__(self):
        self.players =[]
        self.size = 60
        self.start = 0
        self.bg_col = [(50, 150, 30), (50,50,250),(0,0,0)]
        self.bg_col_option = 0
        self.players.append(Player(self, 1, "img/pf0.png"))
        self.players.append(Player(self, 9, "img/pf1.png"))

        self.screen = pygame.display.set_mode((self.size * len(map.level), self.size * len(map.level)))

        pygame.init()

        while self.start==0: #menu

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)

            menu = pygame_menu.Menu('Boomberman', self.size*11, self.size*11, theme=pygame_menu.themes.THEME_BLUE)
            menu.add.selector('Background color ', [('Green', 0), ('Blue', 1), ('Black', 2)], onchange=self.set_color)
            menu.add.button('Play', self.start_game)
            menu.add.button('Quit', pygame_menu.events.EXIT)
            menu.mainloop(self.screen)

    def start_game(self):

        self.start = 1
        while self.start==1: #game

            pygame.time.Clock().tick(90)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)

            walls = map.generate_walls(self.size)[0]  #  walls
            boxes = map.generate_walls(self.size)[1]  #  boxes

            self.screen.fill(self.bg_col[self.bg_col_option])
            for wall in walls:
                self.screen.blit(wall.image, wall.rect)

            for box in boxes:
                self.screen.blit(box.image, box.rect)

            for p in self.players:
                p.press()
                self.screen.blit(p.image, p.rect)
                p.set_b()
                if (p.lives==0):

                    self.start=2
                    self.end_game()
            pygame.display.flip()

    def end_game(self):
        font = pygame.font.Font('freesansbold.ttf', self.size * 2)
        text = font.render('Koniec gry', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.size * 11 // 2, self.size * 11 // 2)
        while self.start == 2:
            pygame.time.Clock().tick(10)
            self.screen.blit(text, textRect)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
            # sys.exit(0)
            pygame.display.flip()

    def set_color(self, a, b):
        self.bg_col_option = b

Game()