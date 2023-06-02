import pygame
from random import *
from collections import defaultdict
import time
import os
pygame.init()
'''WIDTH = 1280
HEIGHT = 720
FPS = 60'''

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GREY = (196, 196, 196)

back_color = (179, 233, 179)
wall_color = BLACK

class Game:
    def __init__(self,
                 caption,
                 #back_image_filename,
                 fps):
        #self.background_image = \
            #pygame.image.load(back_image_filename)
        self.fps = fps
        self.game_over = False
        self.game_over_all = 0
        self.objects = pygame.sprite.Group()
        self.text_objects = []
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.walls_list = [  #33x19
            '111111111111111111111111111111111',
            '111111.....................111111',
            '111111.111.1.1.111.1.1.111.111111',
            '1..........1.1.1...1.1..........1',
            '1.11111111.111.1.1.111.11111111.1',
            '1..........1.1.1.....1.....1....1',
            '1.1111.111.1.1.1.1.111.111.1111.1',
            '1...............................1',
            '1111.11.11.1.111.111.11111.1111.1',
            '...........1.1..x..1.1...........',
            '1.1111.11111.1111111.1.11111.1111',
            '1..........1....................1',
            '1.11111111.1111.1111111111.1111.1',
            '1.1.............................1',
            '1.11111111.11111.11111111111111.1',
            '1...............................1',
            '111111.1111111.11111111111.111111',
            '111111.....................111111',
            '111111111111111111111111111111111'
        ]
    def update(self):
        self.objects.update()
        for i in self.text_objects:
            i.update()
    def draw(self):
        self.display.fill(back_color)
        self.objects.draw(self.display)
        for i in self.text_objects:
            i.draw(self.display)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        for object in self.objects:
            object.set_start_pos()
        if not self.game_over_all: self.game_over = False
        while not self.game_over and text_joke_counter.joke_counter<number_of_jokes:
            #self.display.blit(self.background_image, (0, 0))
            self.clock.tick(self.fps)
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()


    def handle(self, key):
        if key == pygame.K_ESCAPE:
            self.game_over = True
            self.game_over_all = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img, img2):
        pygame.sprite.Sprite.__init__(self)
        self.x_start = x
        self.y_start = y
        self.img = img
        self.img2 = img2
        self.size = 35
        self.image = self.img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.key = None
        self.speed = 2
        self.move = [0, 0]
        self.moving = [0, 0]

    def set_start_pos(self):
        self.rect.center = (self.x_start, self.y_start)

    def coord(self, a):
        if a=='x': return int(self.rect.centerx//40)
        if a=='y': return int(self.rect.centery//40)

    def nextto_wall(self):
        if (self.rect.centerx%40==0 and self.rect.centery%40==0) and game.walls_list[self.coord('y')+self.move[1]][self.coord('x')+self.move[0]] == '1' and (game.walls_list[self.coord('y')+self.moving[1]][self.coord('x')+self.moving[0]]=='1' or self.moving == [0, 0]):
            return True
        else:
            return False

    def motion(self):
        if (self.rect.centerx%40==0 and self.rect.centery%40==0) and game.walls_list[self.coord('y')+self.move[1]][self.coord('x')+self.move[0]] == '1':
            if game.walls_list[self.coord('y')+self.moving[1]][self.coord('x')+self.moving[0]]=='1':
                self.moving = [0, 0]
        elif (self.rect.centerx%40==0 and self.rect.centery%40==0) or \
                (self.move[0]==self.moving[0] or self.move[1]==self.moving[1]):
            self.moving = self.move
        self.rect.x+=self.moving[0]*self.speed
        self.rect.y+=self.moving[1]*self.speed

    def update(self):
        if self.moving == [1, 0]:
            self.image = self.img2
        elif self.moving == [-1, 0]:
            self.image = self.img
        self.image.set_colorkey(WHITE)
        if self.rect.centerx <= 0: self.rect.centerx = game.WIDTH
        elif self.rect.centerx >= game.WIDTH: self.rect.centerx = 0
        self.motion()

    def handle(self, key):
        self.key = key
        if self.key == None: self.move = [0, 0]
        if self.key == pygame.K_UP: self.move = [0, -1]
        if self.key == pygame.K_DOWN: self.move = [0, 1]
        if self.key == pygame.K_LEFT: self.move = [-1, 0]
        if self.key == pygame.K_RIGHT: self.move = [1, 0]

class Student(pygame.sprite.Sprite):
    def __init__(self, x, y, img, img2):
        pygame.sprite.Sprite.__init__(self)
        self.x_start = x
        self.y_start = y
        self.img = img
        self.img2 = img2
        self.size = 35
        self.image = self.img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.key = None
        self.speed = 2
        self.move = [0, 0]
        self.moving = [0, 0]
        self.moves = [[0,-1], [0,1], [-1,0], [1,0]]
        self.seewall = 0

    def set_start_pos(self):
        self.rect.center = (self.x_start, self.y_start)

    def coord(self, a):
        if a=='x': return int(self.rect.centerx//40)
        if a=='y': return int(self.rect.centery//40)

    def see_player(self):
        self.seewall = 0
        if self.rect.centerx == player.rect.centerx:
            for i in range(min(player.coord('y'), self.coord('y')), max(player.coord('y'), self.coord('y'))):
                if '1' in game.walls_list[i][self.coord('x')]:
                    self.seewall = 1
            if self.seewall == 1:
                return False
            else:
                return True
        elif self.rect.centery == player.rect.centery and self.coord('x')>player.coord('x'):
            if '1' not in game.walls_list[self.coord('y')][player.coord('x'):self.coord('x')]:
                return True
        elif self.rect.centery == player.rect.centery and self.coord('x')<player.coord('x'):
            if '1' not in game.walls_list[self.coord('y')][self.coord('x'):player.coord('x')]:
                return True
        else:
            return False

    def motion(self):
        if (self.rect.centerx%40==0 and self.rect.centery%40==0) and game.walls_list[self.coord('y')+self.move[1]][self.coord('x')+self.move[0]] == '1':
            if game.walls_list[self.coord('y')+self.moving[1]][self.coord('x')+self.moving[0]]=='1':
                self.moving = [0, 0]
        elif (self.rect.centerx%40==0 and self.rect.centery%40==0) or \
                (self.move[0]==self.moving[0] or self.move[1]==self.moving[1]):
            self.moving = self.move
        self.rect.x+=self.moving[0]*self.speed
        self.rect.y+=self.moving[1]*self.speed

    def random_move(self, r=3):
        if 40<=self.rect.centerx<=game.WIDTH-40:
            for i in range(-1, 2, 2):
                if (self.rect.centerx%40==0 and self.rect.centery%40==0) and game.walls_list[self.coord('y')+i][self.coord('x')] != '1':
                    if randint(1,r)==1 and self.move!=[0, -i]: self.move = [0, i]
            for i in range(-1, 2, 2):
                if (self.rect.centerx%40==0 and self.rect.centery%40==0) and game.walls_list[self.coord('y')][self.coord('x')+i] != '1':
                    if randint(1,r)==1 and self.move!=[-i, 0]: self.move = [i, 0]

    def update(self):
        if abs(self.rect.centerx - player.rect.centerx) < (self.size + player.size) // 4 and abs(
                player.rect.centery-self.rect.centery) < (self.size + player.size) // 3:
            game.game_over = True
        if self.moving == [1, 0]:
            self.image = self.img2
        elif self.moving == [-1, 0]:
            self.image = self.img
        self.image.set_colorkey(WHITE)
        if self.rect.centerx <= 0: self.rect.centerx = game.WIDTH
        elif self.rect.centerx >= game.WIDTH: self.rect.centerx = 0
        if self.move == [0, 0] or self.moving == [0, 0]:
            self.move = self.moves[randint(0,3)]
        self.random_move()
        if self.see_player():

            self.move = [player.rect.centerx-self.rect.centerx, player.rect.centery-self.rect.centery]
            for i in range(2):
                if self.move[i]>1: self.move[i]=1
                if self.move[i]<-1: self.move[i]=-1
            self.random_move(10)
        self.motion()



    def handle(self, key):
        self.key = key

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.x_start, self.y_start = x, y
        self.image = pygame.Surface((size, size))
        self.image.fill(wall_color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.key = None

    def set_start_pos(self):
        self.rect.center = (self.x_start, self.y_start)

    def update(self):
        self.rect.x+=0
        self.rect.y+=0

    def handle(self, key):
        self.key = key

class Joke(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.x_start = x
        self.y_start = y
        self.img = img
        self.size = 20
        self.image = img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.taken = 0

    def set_start_pos(self):
        self.rect.center = (self.x_start, self.y_start)

    def coord(self, a):
        if a=='x': return int(self.rect.centerx//40)
        if a=='y': return int(self.rect.centery//40)

    def is_taken(self):
        if abs(self.rect.centerx-player.rect.centerx)<5 and abs(self.rect.centery-player.rect.centery)<5:
            self.taken = 1
            self.image.fill(back_color)


    def update(self):
        self.is_taken()
        if self.taken == 1:
            self.image.fill(back_color)

    def handle(self, key):
        self.key = key

class TextObject:
    def __init__(self,
                 x,
                 y,
                 text,
                 color,
                 back_color,
                 font_name,
                 font_size):
        self.x_start = x
        self.y_start = y
        self.text = text
        self.color = color
        self.back_color = back_color
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.textSurfaceObj = self.font.render(self.text, True, self.color, self.back_color)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (self.x_start, self.y_start)

    def draw(self, display):
        self.textSurfaceObj = self.font.render(self.text, True, self.color, self.back_color)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (self.x_start, self.y_start)
        display.blit(self.textSurfaceObj, self.textRectObj)

    def update(self):
        pass

class TextJokeCounter(TextObject):
    def __init__(self,
                 x,
                 y,
                 text,
                 color,
                 back_color,
                 font_name,
                 font_size):
        self.x_start = x
        self.y_start = y
        self.text = text
        self.color = color
        self.back_color = back_color
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.textSurfaceObj = self.font.render(self.text, True, self.color, self.back_color)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (self.x_start, self.y_start)
        self.joke_counter = 0

    def update(self):
        self.joke_counter = 0
        for i in jokes:
            self.joke_counter+=i.taken
        self.text = 'JOKES:'+str(self.joke_counter)

def pic(picture):
    return pygame.image.load(os.path.join(img_folder, picture+'.png')).convert()

game = Game('NaimRun', 60)
lifes = 3


joke1 = Joke(3*40, 13*40, pic('joke1'))
game.objects.add(joke1)
joke2 = Joke(12*40, 3*40, pic('joke2'))
game.objects.add(joke2)
joke3 = Joke(28*40, 5*40, pic('joke3'))
game.objects.add(joke3)
joke4 = Joke(20*40, 3*40, pic('joke4'))
game.objects.add(joke4)
joke5 = Joke(game.WIDTH//2-2*40, game.HEIGHT//2, pic('joke5'))
game.objects.add(joke5)
joke6 = Joke(game.WIDTH//2+2*40, game.HEIGHT//2, pic('joke6'))
game.objects.add(joke6)
joke7 = Joke(6*40, 17*40, pic('joke7'))
game.objects.add(joke7)
joke8 = Joke(26*40, 17*40, pic('joke8'))
game.objects.add(joke8)

jokes = pygame.sprite.Group(joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8)
number_of_jokes = 0
for i in jokes:
    number_of_jokes+=1




player = Player(game.WIDTH/2, game.HEIGHT/2+2*40, pic('naim'), pic('naim_r'))
game.objects.add(player)

student1 = Student(game.WIDTH/2-1*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student1)
student2 = Student(game.WIDTH/2-2*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student2)
student3 = Student(game.WIDTH/2+1*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student3)
student4 = Student(game.WIDTH/2+2*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student4)
student5 = Student(game.WIDTH/2-1*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student5)
student6 = Student(game.WIDTH/2-2*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student6)
student7 = Student(game.WIDTH/2+1*40, game.HEIGHT/2, pic('akmal'), pic('akmal_r'))
game.objects.add(student7)

text_joke_counter = TextJokeCounter(1160, 55, '0', GREEN, None,  'Consolas', 30)
game.text_objects.append(text_joke_counter)
text_lifes = TextObject(120, 50, '| '*lifes, GREEN, None, 'Consolas', 60)
game.text_objects.append(text_lifes)
text_game_over = TextObject(game.WIDTH//2, game.HEIGHT//2, ' GAME OVER! ', RED, BLACK, 'Consolas', 80)
text_you_won = TextObject(game.WIDTH//2, game.HEIGHT//2, ' YOU WON! ', GREEN, BLACK, 'Consolas', 80)
walls_list = game.walls_list
walls=[]
for i in range(len(walls_list)):
    for j in range(len(walls_list[i])):
        if walls_list[i][j] == '1':
            walls.append(Wall(j * 40, i * 40, 40))

for stena in walls:
    game.objects.add(stena)

game.keydown_handlers[pygame.K_ESCAPE].append(game.handle)
game.keydown_handlers[pygame.K_UP].append(player.handle)
game.keydown_handlers[pygame.K_DOWN].append(player.handle)
game.keydown_handlers[pygame.K_LEFT].append(player.handle)
game.keydown_handlers[pygame.K_RIGHT].append(player.handle)


while lifes and text_joke_counter.joke_counter<number_of_jokes:
    game.run()
    if text_joke_counter.joke_counter<number_of_jokes: lifes-=1
    text_lifes.text = ('| '*lifes)
    time.sleep(min(lifes, 1-game.game_over_all))

if game.game_over_all == 0:
    if lifes == 0:
        game.text_objects.append(text_game_over)
    else:
        game.text_objects.append(text_you_won)
    game.update()
    game.draw()
    pygame.display.flip()
time.sleep(3*(1-game.game_over_all))
pygame.quit()

