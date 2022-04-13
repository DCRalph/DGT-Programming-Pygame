#!python3.9
"""
RACINGCAR GAME
by: William Giles

This is a simple racing game made in Python with Pygame.
The game is a single player game where the player must
avoid the obstacles and reach the finish line.
Version 5.0
"""

import random
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

rawObstacles = []
obstacles = pygame.sprite.Group()
availableObsicles = []
score = 0

def imageScale(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))


class Car(pygame.sprite.Sprite):
    def __init__(self, image, scale):
        super().__init__()
        self.image = imageScale(image, GRID * scale)
        self.mask  = pygame.mask.from_surface(self.image)
        

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.x = WIDTH / 2 - self.width / GRID / 2
        self.y = HEIGHT - 10 - self.height / GRID

        self.rect = self.image.get_rect(topleft=(self.x * GRID, self.y * GRID))


class YourCar(Car):
    def __init__(self, image, *, scale=1):
        super().__init__(image, scale)

    def update(self):
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
        else:
            self.rect.topleft = (self.x * GRID, self.y * GRID)
 
        
    def checkCollision(self):
        collisions = pygame.sprite.spritecollide(self, obstacles, False)
        collidable = pygame.sprite.collide_mask
        if pygame.sprite.spritecollideany(self, collisions, collidable):
            return True
        return False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, scale, lane):
        super().__init__()
        global obstacles
        self.image = imageScale(image, GRID * scale)
        self.mask  = pygame.mask.from_surface(self.image)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        x = [102, 291, 502, 691][lane] + 4
        self.x = x / GRID - self.width / GRID / 2
        self.y = -20 - self.height / GRID

        self.rect = self.image.get_rect(topleft=(self.x * GRID, self.y * GRID))

    def update(self):
        global score
        self.y += 1

        self.rect.topleft = (self.x * GRID, self.y * GRID)

        if self.y > HEIGHT:
            score += 1
            obstacles.remove(self)
            print('pop')


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


class Road(object):
    def __init__(self, image):
        self.image1 = pygame.transform.scale(image, (WIDTH * GRID, HEIGHT * GRID))
        self.image2 = pygame.transform.scale(image, (WIDTH * GRID, HEIGHT * GRID))

        self.x1 = 0
        self.y1 = 0

        self.x2 = 0
        self.y2 = -HEIGHT

    def update(self):
        self.y1 += 1
        self.y2 += 1

        if self.y1 >= HEIGHT:
            self.y1 = -HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = -HEIGHT

    def draw(self):
        WIN.blit(self.image1, (self.x1 * GRID, self.y1 * GRID))
        WIN.blit(self.image2, (self.x2 * GRID, self.y2 * GRID))

def keyDown(key):
    global RUN, STATE

    if key == pygame.K_ESCAPE:
        RUN = False

    if key == pygame.K_SPACE and STATE == PREGAME:
        STATE = GAME

    if key == pygame.K_SPACE and STATE == END:
        STATE = RESET

def drawBackground(road):
    pass
    
    # px1 = WIDTH * GRID / 102
    # px2 = px1 + 1

    # def pxCalc(n):
    #     e = px1 * n - px1 + 1
    #     e = math.floor(e)
    #     return e

    # pygame.draw.rect(WIN, WHITE, (pxCalc(14) , 1, px2, 1))
    # pygame.draw.rect(WIN, WHITE, (pxCalc(38) , 1, px2, 1))
    # pygame.draw.rect(WIN, WHITE, (pxCalc(65) , 1, px2, 1))
    # pygame.draw.rect(WIN, WHITE, (pxCalc(89) , 1, px2, 1))


def main():
    global RUN, STATE, obstacles, rawObstacles

    clock = pygame.time.Clock()

    cars = []
    cars.append(pygame.image.load('cars/red.png'))
    cars.append(pygame.image.load('cars/blue.png'))
    cars.append(pygame.image.load('cars/pink.png'))
    cars.append(pygame.image.load('cars/green.png'))

    road = Road(pygame.image.load('road.png'))
    

    yourCar = pygame.sprite.GroupSingle(YourCar(cars[random.randint(0, len(cars)-1)]))

    while RUN:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

            if event.type == pygame.KEYDOWN:
                keyDown(event.key)

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     print(event.pos)
                
    
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
            road.update()
            road.draw()
            
            if random.randint(0, 150) < 1:
                newObsictal = availableObsicles[random.randint(0, len(availableObsicles) - 1)]
                new = newObsictal(random.randint(0, 3))

                obstacles.add(new)
                rawObstacles.append(new)
        
            obstacles.update()
            obstacles.draw(WIN)


            yourCar.update()
            yourCar.draw(WIN)

        elif STATE == END:
            WIN.fill(BLACK)
            drawBackground(road)

            obstacles.draw(WIN)

            yourCar.draw(WIN)

            s = pygame.Surface((WIDTH*GRID, HEIGHT*GRID))
            s.set_alpha(128)
            s.fill((0,0,0))
            WIN.blit(s, (0,0))

            text1 = font1.render("Game Over", 1, WHITE)
            text2 = font2.render(F"You died with a score of {score}", 1, WHITE)
            text3 = font2.render("Press space to restart", 1, WHITE)
            WIN.blit(text1, (WIDTH * GRID / 2 - text1.get_width() / 2, (HEIGHT * GRID / 2 - text1.get_height() / 2) - font1Size - GRID))
            WIN.blit(text2, (WIDTH * GRID / 2 - text2.get_width() / 2, (HEIGHT * GRID / 2 - text2.get_height() / 2)))
            WIN.blit(text3, (WIDTH * GRID / 2 - text3.get_width() / 2, (HEIGHT * GRID / 2 - text3.get_height() / 2) + font2Size + GRID))


        elif STATE == RESET:
            yourCar = pygame.sprite.GroupSingle(YourCar(cars[random.randint(0, len(cars)-1)]))
            obstacles = pygame.sprite.Group()
            score = 0
            STATE = PREGAME

        pygame.display.update()
    pygame.quit()
if __name__ == '__main__':
    main()