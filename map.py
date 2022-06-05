import pygame

level = [
        "00000000000",
        "02211111220",
        "02010101020",
        "02111111110",
        "01010101010",
        "02222222220",
        "01010101020",
        "01111111120",
        "02010101020",
        "02211111220",
        "00000000000"
    ]    # 0 wall, 1 box, 2 empty

level_int =[[0 for x in range(len(level))] for y in range(len(level))] #konwersja tablicy string na int
for i in range (0,len(level)):
    for j in range (0,len(level)):
        level_int[i][j] = int(level[i][j])

def mod(x, y, size): #update tablicy po wybuchu
    for line in level:
        for sign in line:
            if level_int[x-1][y] == 1:
                level_int[x - 1][y] = 2
            if level_int[x+1][y] == 1:
                level_int[x + 1][y] = 2
            if level_int[x][y-1] == 1:
                level_int[x][y - 1] = 2
            if level_int[x][y+1] == 1:
                level_int[x][y + 1] = 2
    generate_walls(size)

wall = pygame.image.load('img/block.png')#.convert()
box = pygame.image.load('img/box.png')#.convert()

def generate_walls(size):
    walls=[]
    boxes=[]
    x = y = 0
    for row in level_int:
        for col in row:
            if col == 0:
                walls .append(Wall((x, y), size))
            if col == 1:
                boxes.append(Box((x, y), size) )
            x += size
        y += size
        x = 0

    return walls, boxes

class Wall(object):

    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.image = pygame.transform.scale(wall, (size, size))

class Box(object):

    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.image = pygame.transform.scale(box, (size, size))