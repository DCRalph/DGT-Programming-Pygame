#!python3.9
"""
RACINGCAR GAME
by: William Giles

This is a simple racing game made in Python with Pygame.
The game is a single player game where the player must
avoid the obstacles and reach the finish line.
Version 1.0
"""

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

        keys = pygame.key.get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            self.x -= 1 * GRID
        elif keys[K_RIGHT] or keys[K_d]:
            self.x += 1 * GRID


        # constrain the car to the screen
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.width / GRID:
            self.x = WIDTH - self.width / GRID

        

    def keyDown(self, key):
        pass
        # if key == K_LEFT:
        #     self.x -= 1 * GRID
        # elif key == K_RIGHT:
        #     self.x += 1 * GRID



class Obstacle(object):
    def __init__(self, image, * ,scale = 1):
        self.image = imageScale(image, GRID * scale)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.x = WIDTH / 2 - self.width / GRID / 2
        self.y = HEIGHT / 2  - self.height / GRID / 2

    def draw(self):
        WIN.blit(self.image, (self.x * GRID, self.y * GRID))

    def update(self):
        self.y += 1 * GRID



def keyDown(key):
    global RUN, STATE

    if key == pygame.K_ESCAPE:
        RUN = False

    if key == pygame.K_SPACE and STATE == PREGAME:
        STATE = GAME

    if key == pygame.K_SPACE and STATE == END:
        STATE = RESET



def main():
    global RUN, STATE

    clock = pygame.time.Clock()

    redcar = pygame.image.load('cars/red.png')
    bluecar = pygame.image.load('cars/blue.png')
    pinkcar = pygame.image.load('cars/pink.png')

    block = pygame.image.load('obstacles/block.png')
    cone1 = pygame.image.load('obstacles/cone1.png')
    cone2 = pygame.image.load('obstacles/cone2.png')


    yourCar = YourCar(redcar)


    obstacles = []
    
    obstacles.append(Obstacle(block, scale=1))
    # obstacles.append(Obstacle(cone1 , scale=3))
    # obstacles.append(Obstacle(cone2, scale=3))

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
                pass

            
        

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

            for i in obstacles:
                i.draw()


            yourCar.updete()
            yourCar.draw()

        elif STATE == END:
            pass

        elif STATE == RESET:
            STATE = PREGAME

        pygame.display.update()
    pygame.quit()
if __name__ == '__main__':
    main()
