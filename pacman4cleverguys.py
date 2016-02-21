import sys
import pygame
from pygame.locals import *
from math import floor
import random

TileSize = 32
MapSize = 18

class Obman:


    name = 'default'
    obman_path = './resources/themes/' + name
    pacman = obman_path + '/pacman.png'
    pacman_right=obman_path + '/pacman_right.png'
    pacman_left=obman_path + '/pacman_left.png'
    pacman_down=obman_path + '/pacman_down.png'
    pacman_up=obman_path + '/pacman_up.png'
    ghost = obman_path + '/ghost.png'
    wall = obman_path + '/wall.png'
    dot = obman_path + '/Burger.png'
    background = obman_path + '/background.png'
    eat_bonus = obman_path + '/pill.png'
    bonus = obman_path + '/coffee.png'


def init_window():
    pygame.init()
    pygame.display.set_mode((MapSize * TileSize, MapSize * TileSize))
    pygame.display.set_caption('Pacman')


def draw_backgfloor(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * TileSize, floor(y) * TileSize, TileSize, TileSize )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    ghosts = []
    num = 3
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.ghost, x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0
    def decide(self):
        x, y = int(self.x), int(self.y)
        if y == int(pacman.y):
            for X in range(x, 16):
                if isinstance(MAP.map[y][X], Wall): break
                if X == int(pacman.x):
                    return 1 if not EatBonus.eat_bonus else 3
            for X in reversed(range(x)):
                if isinstance(MAP.map[y][X], Wall): break
                if X == int(pacman.x):
                    return 3 if not EatBonus.eat_bonus else 1
        if x == int(pacman.x):
            for Y in range(y, 16):
                if isinstance(MAP.map[Y][x], Wall): break
                if Y == int(pacman.y):
                    return 2 if not EatBonus.eat_bonus else 4
            for Y in reversed(range(y)):
                if isinstance(MAP.map[Y][x], Wall): break
                if Y == int(pacman.y):
                    return 4 if not EatBonus.eat_bonus else 2
            
            
    def game_tick(self):
        super(Ghost, self).game_tick()
        
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)
        
        decision = self.decide()
        if decision: self.direction = decision
        
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= MapSize-1:
                self.x = MapSize-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= MapSize-1:
                self.y = MapSize-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                    self.x = 0
                    self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        if floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(self.y)  and EatBonus.eat_bonus:
              Ghost.ghosts.remove(self)
        self.set_coord(self.x, self.y)
        if floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(self.y)  and not(EatBonus.eat_bonus):
            sys.exit(0)
        
def draw_ghosts(screen):
    for g in Ghost.ghosts:
        g.draw(screen)
        
def tick_ghosts():
    for g in Ghost.ghosts:
        g.game_tick()

class Pacman(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.pacman, x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0
    def __get_direction(self):
        return self.__direction;
    def __set_direction(self, d):
        self.__direction = d
        if d == 1:
            self.image = pygame.image.load(Obman.pacman_right)
        elif d == 2:
            self.image = pygame.image.load(Obman.pacman_down)
        elif d == 3:
            self.image = pygame.image.load(Obman.pacman_left)
        elif d == 4:
            self.image = pygame.image.load(Obman.pacman_up)
        elif d != 0:
            raise ValueError("invalid direction detected")
    direction = property(__get_direction, __set_direction)
    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= MapSize-1:
                self.x = MapSize-1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= MapSize-1:
                self.y = MapSize-1
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
        self.set_coord(self.x, self.y)
        if isinstance(MAP.map[int(self.y)][int(self.x)], Dot):
            MAP.map[int(self.y)][int(self.x)] = None
            MAP.food-=1
        if isinstance(MAP.map[int(self.y)][int(self.x)], Bonus):
            MAP.map[int(self.y)][int(self.x)] = None  
            pacman.velocity = 10.0/10.0  
        if isinstance(MAP.map[int(self.y)][int(self.x)], BadBonus):
            MAP.map[int(self.y)][int(self.x)] = None  
            Ghost.num = 10 
        if isinstance(MAP.map[int(self.y)][int(self.x)], EatBonus)  == True:
            MAP.map[int(self.y)][int(self.x)] = None
            EatBonus.eat_bonus = 1
             

class Wall(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.wall, x, y)
class Dot(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.dot, x, y)
        
def is_wall(x, y):
    return isinstance(MAP.map[int(y)][int(x)], Wall)
def create_walls(coords):
    Wall.walls = [Wall(2, 4)]

class Map:
    food=0
    def __init__(self, filename):
        self.map = []
        f=open(filename, 'r')
        txt = f.readlines()
        f.close()
        #read
        for y in range(len(txt)):
            self.map.append([])  
            for x in range(len(txt[y])):
                if '#' in txt[y][x]:     #if this cell is a wall
                    self.map[-1].append(Wall(x, y)) #add a wall tile to the end of that line
                elif '.' in txt[y][x]:   #if this cell is a piece of food
                    self.map[-1].append(Dot(x, y))  #add a dot tile to the end of that line
                    self.food+=1
                elif txt[y][x] == "+":
                    self.map[-1].append(Bonus(x, y))
                elif txt[y][x] == "&":
                    self.map[-1].append(EatBonus(x, y)) 
                else:                    #if the tile is empty
                    self.map[-1].append(None) #add Nothing
    def draw(self, screen):
        for y in range(len(self.map)):#for each line starting from the top
            for x in range(len(self.map[y])):#for each tile of that line
                if self.map[y][x]: #if something is on that tile
                    self.map[y][x].draw(screen) #draw that   
                    
class Bonus(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.bonus, x, y)      
 

class BadBonus(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.bad_bonus, x, y) 
    
class EatBonus(GameObject):
    eat_bonus = None
    def __init__(self, x, y):
        GameObject.__init__(self, Obman.eat_bonus, x, y)                    
def create_ghost():
    Ghost.ghosts = [Ghost(1, 1) for a in range (Ghost.num)]
        

def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE) or MAP.food==0:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0
    
if __name__ == '__main__':
    init_window()
    global MAP
    MAP = Map('map.txt')
    pacman = Pacman(13, 5)
    backgfloor = pygame.image.load(Obman.background)
    screen = pygame.display.get_surface()
    create_ghost()


    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(50)
        tick_ghosts()
        pacman.game_tick()
        draw_backgfloor(screen, backgfloor)
        pacman.draw(screen)
        draw_ghosts(screen)
        MAP.draw(screen)
        pygame.display.update()
