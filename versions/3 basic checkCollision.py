#!python3.9
"""
RACINGCAR GAME
by: William Giles

This is a simple racing game made in Python with Pygame.
The game is a single player game where the player must
avoid the obstacles and reach the finish line.
Version 3.0
"""

from ast import Global
import random
from tkinter import Widget
import pygame
from pygame.locals import *
import math

GRID = 2
WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH * GRID, HEIGHT * GRID))
pygame.display.set_caption("Racingcar462 Game")

pygame.font.init()
font1Size = math.floor(25 * GRID)
font2Size = math.floor(20 * GRID)
font1 = pygame.font.SysFont("comicsans", font1Size)
font2 = pygame.font.SysFont("comicsans", font2Size)

FPS = 60
RUN = True


PREGAME = 0
GAME = 1
END = 2
RESET = 3

STATE = PREGAME


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


obstacles = []
availableObsicles = []
score = 0

def imageScale(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))


class Car(object):
    def __init__(self, image, scale):
        self.image = imageScale(image, GRID * scale)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.x = WIDTH / 2 - self.width / GRID / 2
        self.y = HEIGHT - 10 - self.height / GRID
    

    def draw(self):
        WIN.blit(self.image, (self.x * GRID, self.y * GRID))


class YourCar(Car):
    def __init__(self, image, *, scale=1):
        super().__init__(image, scale)


    def draw(self):
        WIN.blit(self.image, (self.x * GRID, self.y * GRID))

    def updete(self):
        global STATE

        keys = pygame.key.get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            self.x -= 2 * GRID
        elif keys[K_RIGHT] or keys[K_d]:
            self.x += 2 * GRID

        offset = 10

        if self.x < offset:
            self.x = offset
        elif self.x > WIDTH - self.width / GRID - offset:
            self.x = WIDTH - self.width / GRID - offset

        if self.checkCollision():
            print("Collision")
            STATE = END
        # else:
        #     print("No Collision")
 
        
    def checkCollision(self):
        for i in range(len(obstacles)):
            o = obstacles[i]
            if o != None:
                if self.x + self.width / GRID > o.x and self.x < o.x + o.width / GRID:
                    if self.y + self.height / GRID > o.y and self.y < o.y + o.height / GRID:
                        return True
        return False


    def keyDown(self, key):
        pass
        # if key == K_LEFT:
        #     self.x -= 1 * GRID
        # elif key == K_RIGHT:
        #     self.x += 1 * GRID



class Obstacle(object):
    def __init__(self, image, scale, lane):
        global obstacles
        self.image = imageScale(image, GRID * scale)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        x = [102, 291, 502, 691][lane] + 4
        self.x = x / GRID - self.width / GRID / 2

        # self.x = 0
        self.y = -20 - self.height / GRID
        # self.y = 1

        

    def draw(self):
        WIN.blit(self.image, (self.x * GRID, self.y * GRID))

    def update(self, i):
        global score
        self.y += 1 * GRID

        if self.y > HEIGHT:
            score += 1
            obstacles.pop(i)
            return True
        
        return False
        



class Cone1(Obstacle):
    def __init__(self, lane):
        img = pygame.image.load('obstacles/cone1.png')
        super().__init__(img, 3, lane)
        
class Cone2(Obstacle):
    def __init__(self, lane):
        img = pygame.image.load('obstacles/cone2.png')
        super().__init__(img, 3, lane)
        
class Block(Obstacle):
    def __init__(self, lane):
        img = pygame.image.load('obstacles/block.png')
        super().__init__(img, 1.8, lane)


availableObsicles.append(Cone1)      
availableObsicles.append(Cone2)
availableObsicles.append(Block)

def keyDown(key):
    global RUN, STATE

    if key == pygame.K_ESCAPE:
        RUN = False

    if key == pygame.K_SPACE and STATE == PREGAME:
        STATE = GAME

    if key == pygame.K_SPACE and STATE == END:
        STATE = RESET

def drawBackground(bg):
    WIN.blit(bg, (0, 0))
    px1 = WIDTH * GRID / 102
    px2 = px1 + 1

    def pxCalc(n):
        e = px1 * n - px1 + 1
        e = math.floor(e)
        return e

    pygame.draw.rect(WIN, WHITE, (pxCalc(14) , 1, px2, 1))
    pygame.draw.rect(WIN, WHITE, (pxCalc(38) , 1, px2, 1))
    pygame.draw.rect(WIN, WHITE, (pxCalc(65) , 1, px2, 1))
    pygame.draw.rect(WIN, WHITE, (pxCalc(89) , 1, px2, 1))


def main():
    global RUN, STATE

    clock = pygame.time.Clock()

    cars = []
    cars.append(pygame.image.load('cars/red.png'))
    cars.append(pygame.image.load('cars/blue.png'))
    cars.append(pygame.image.load('cars/pink.png'))
    cars.append(pygame.image.load('cars/green.png'))

    road = pygame.image.load('road.png')
    road = pygame.transform.scale(road, (WIDTH * GRID, HEIGHT * GRID))

    yourCar = YourCar(cars[random.randint(0, len(cars)-1)])

    # obstacles.append(Cone1(0))
    # obstacles.append(Cone2(1))
    # obstacles.append(Block(2))

    while RUN:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

            if event.type == pygame.KEYDOWN:
                keyDown(event.key)
                if STATE == GAME:
                    yourCar.keyDown(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

            
    
        if STATE == PREGAME:
            WIN.fill(BLACK)

            
            text1 = font1.render("RACING SIM 9000", 1, WHITE)
            text2 = font2.render("Use wsad or arrow keys to play", 1, WHITE)
            text3 = font2.render("Press space to start", 1, WHITE)
            WIN.blit(text1, (WIDTH * GRID / 2 - text1.get_width() / 2, (HEIGHT * GRID / 2 - text1.get_height() / 2) - font1Size - GRID))
            WIN.blit(text2, (WIDTH * GRID / 2 - text2.get_width() / 2, (HEIGHT * GRID / 2 - text2.get_height() / 2)))
            WIN.blit(text3, (WIDTH * GRID / 2 - text3.get_width() / 2, (HEIGHT * GRID / 2 - text3.get_height() / 2) + font2Size + GRID))

        elif STATE == GAME:
            WIN.fill(BLACK)

            drawBackground(road)
            
            if random.randint(0, 100) < 1:
                newObsictal = availableObsicles[random.randint(0, len(availableObsicles) - 1)]
                obstacles.append(newObsictal(random.randint(0, 3)))

        
            def doObstacles():
                for i in range(len(obstacles)):
                    i = len(obstacles) - 1 - i
                    if not obstacles[i].update(i):
                        obstacles[i].draw()
                    else:
                        # print("rerun")
                        doObstacles()
                        break

            doObstacles()

            yourCar.updete()
            yourCar.draw()

        elif STATE == END:

            text1 = font1.render("Game Over", 1, WHITE)
            text2 = font2.render(F"You died with a score of {score}", 1, WHITE)
            text3 = font2.render("Press space to restart", 1, WHITE)
            WIN.blit(text1, (WIDTH * GRID / 2 - text1.get_width() / 2, (HEIGHT * GRID / 2 - text1.get_height() / 2) - font1Size - GRID))
            WIN.blit(text2, (WIDTH * GRID / 2 - text2.get_width() / 2, (HEIGHT * GRID / 2 - text2.get_height() / 2)))
            WIN.blit(text3, (WIDTH * GRID / 2 - text3.get_width() / 2, (HEIGHT * GRID / 2 - text3.get_height() / 2) + font2Size + GRID))

        elif STATE == RESET:
            obstacles = []
            score = 0
            yourCar = YourCar(cars[random.randint(0, len(cars)-1)])
            STATE = PREGAME

        pygame.display.update()
    pygame.quit()
if __name__ == '__main__':
    main()
