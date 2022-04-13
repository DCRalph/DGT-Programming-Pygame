#!python3.9
"""
RACINGCAR GAME
by: William Giles

This is a simple racing game made in Python with Pygame.
The game is a single player game where the player must
avoid the obstacles and reach the finish line.
Version X.0
"""
import sys
if sys.platform != 'darwin':
    print('ewww...')
import random
import pygame
from pygame.locals import *
import math




GRID = 2
WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH * GRID, HEIGHT * GRID))

pygame.font.init()
font1Size = math.floor(25 * GRID)
font2Size = math.floor(20 * GRID)
font1 = pygame.font.SysFont("comicsans", font1Size)
font2 = pygame.font.SysFont("comicsans", font2Size)

CAPTION = "Racingcar SIM 9000"
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

obstacles = pygame.sprite.Group()
availableObstacles = []

highScore = 0
score = 0
scoreTick = 0

speed = 2
carSpeed = 2

try:
    f = open("hs", "r")
    highScore = int(f.read())
    f.close()
except:
    f = open("hs", "w")
    f.write(str(highScore))
    f.close()


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
            self.x -= carSpeed * GRID
        if keys[K_RIGHT] or keys[K_d]:
            self.x += carSpeed * GRID

        if keys[K_UP] or keys[K_w]:
            self.y -= carSpeed * GRID
        if keys[K_DOWN] or keys[K_s]:
            self.y += carSpeed * GRID

        offset = 10

        if self.x < offset:
            self.x = offset
        elif self.x > WIDTH - self.width / GRID - offset:
            self.x = WIDTH - self.width / GRID - offset

        if self.y < offset:
            self.y = offset
        elif self.y > HEIGHT - self.height / GRID - offset:
            self.y = HEIGHT - self.height / GRID - offset
            

        if self.checkCollision():
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
        self.image = imageScale(image, GRID * scale)
        self.mask  = pygame.mask.from_surface(self.image)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        x = [102, 291, 502, 691][lane] + 4
        self.x = x / GRID - self.width / GRID / 2
        self.y = -20 - self.height / GRID

        self.rect = self.image.get_rect(topleft=(self.x * GRID, self.y * GRID))

    def check(self):
        global obstacles
        if pygame.sprite.spritecollideany(self, obstacles):
            obstacles.remove(self)
            return True
        return False

    def update(self):
        global score, scoreTick, speed
        self.y += speed

        self.rect.topleft = (self.x * GRID, self.y * GRID)

        if self.y > HEIGHT:
            score += 1
            scoreTick += 1

            if scoreTick >= 10:
                scoreTick = 0
                speed += 1

            obstacles.remove(self)


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

class Hmm(Obstacle):
    def __init__(self, lane):
        img = pygame.image.load('obstacles/hmm.png')
        super().__init__(img, 1, lane)

class Baby(Obstacle):
    def __init__(self, lane):
        img = pygame.image.load('obstacles/baby.png')
        super().__init__(img, 2, lane)


availableObstacles.append(Cone1)      
availableObstacles.append(Cone2)
availableObstacles.append(Block)
availableObstacles.append(Hmm)
availableObstacles.append(Baby)


class Road(object):
    def __init__(self, image):
        self.image1 = pygame.transform.scale(image, (WIDTH * GRID, HEIGHT * GRID))
        self.image2 = pygame.transform.scale(image, (WIDTH * GRID, HEIGHT * GRID))

        self.x1 = 0
        self.y1 = 0

        self.x2 = 0
        self.y2 = -HEIGHT

    def update(self):
        spd = speed
        self.y1 += spd
        self.y2 += spd

        if self.y1 >= HEIGHT:
            self.y1 = self.y2 - HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = self.y1 - HEIGHT

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

def drawBackgroundMarkings():
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

    pygame.draw.rect(WIN, WHITE, (pxCalc(14) + px1 / 2 , 1, 2, HEIGHT * GRID))
    pygame.draw.rect(WIN, WHITE, (pxCalc(38) + px1 / 2 , 1, 2, HEIGHT * GRID))
    pygame.draw.rect(WIN, WHITE, (pxCalc(65) + px1 / 2 , 1, 2, HEIGHT * GRID))
    pygame.draw.rect(WIN, WHITE, (pxCalc(89) + px1 / 2 , 1, 2, HEIGHT * GRID))

def generateObstacle():
    newObstacle = availableObstacles[random.randint(0, len(availableObstacles) - 1)]
    new = newObstacle(random.randint(0, 3))
    if not new.check():
        obstacles.add(new)
    else:
        generateObstacle() 


def main():
    global RUN, STATE, obstacles, score, speed, scoreTick, highScore

    clock = pygame.time.Clock()

    road = Road(pygame.image.load('road.png'))

    cars = []
    cars.append((pygame.image.load('cars/red.png'), 1))
    cars.append((pygame.image.load('cars/blue.png'), 1))
    cars.append((pygame.image.load('cars/pink.png'), 1))
    cars.append((pygame.image.load('cars/green.png'), 1))
    cars.append((pygame.image.load('cars/falcon heavy.png'), .2))
    cars.append((pygame.image.load('cars/tank.png'), .4))
    cars.append((pygame.image.load('cars/tank2.png'), .4))
    cars.append((pygame.image.load('cars/dragon.png'), 1.5))

    # cars.append((pygame.image.load('cars/dragon.png'), .5))



    n = random.randint(0, len(cars)-1)
    yourCar = YourCar(cars[n][0], scale=cars[n][1])
    yourCar = pygame.sprite.GroupSingle(yourCar)

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

            # drawBackgroundMarkings()
            
            if random.randint(0,80) < 1:
                generateObstacle()
                
        
            obstacles.update()
            obstacles.draw(WIN)

            text1 = font1.render(F"{score}", 1, RED)
            WIN.blit(text1, (WIDTH * GRID / 2 - text1.get_width() / 2, -1*GRID))

            yourCar.update()
            yourCar.draw(WIN)

        elif STATE == END:
            WIN.fill(BLACK)
            road.draw()

            obstacles.draw(WIN)
            yourCar.draw(WIN)

            s = pygame.Surface((WIDTH*GRID, HEIGHT*GRID))
            s.set_alpha(128)
            s.fill((0,0,0))
            WIN.blit(s, (0,0))

            text1 = font1.render("Game Over", 1, WHITE)

            if score > highScore:
                textHS = font1.render("New High Score!", 1, WHITE)
                WIN.blit(textHS, (WIDTH * GRID / 2 - textHS.get_width() / 2, (HEIGHT * GRID / 2 - textHS.get_height() / 2) - (font1Size * 3) - GRID))
                text3 = font2.render(F"Highscore: {score}", 1, WHITE)
            else:
                text3 = font2.render(F"Highscore: {highScore}", 1, WHITE)

            text2 = font2.render(F"You died with a score of {score}", 1, WHITE)
            text4 = font2.render("Press space to restart", 1, WHITE)
            WIN.blit(text1, (WIDTH * GRID / 2 - text1.get_width() / 2, (HEIGHT * GRID / 2 - text1.get_height() / 2) - (font1Size * 1) - GRID))
            WIN.blit(text2, (WIDTH * GRID / 2 - text2.get_width() / 2, (HEIGHT * GRID / 2 - text2.get_height() / 2)))
            WIN.blit(text3, (WIDTH * GRID / 2 - text3.get_width() / 2, (HEIGHT * GRID / 2 - text3.get_height() / 2) + (font2Size * 1) + GRID))
            WIN.blit(text4, (WIDTH * GRID / 2 - text4.get_width() / 2, (HEIGHT * GRID / 2 - text4.get_height() / 2) + (font2Size * 2) + GRID))



        elif STATE == RESET:
            n = random.randint(0, len(cars)-1)
            yourCar = YourCar(cars[n][0], scale=cars[n][1])
            yourCar = pygame.sprite.GroupSingle(yourCar)

            obstacles = pygame.sprite.Group()

            if score > highScore:
                highScore = score

            score = 0
            scoreTick = 0
            speed = 2
            
            STATE = PREGAME

        pygame.display.update()
        pygame.display.set_caption(F"{CAPTION} - FPS: {clock.get_fps():.2f}")

    f = open("hs", "w")
    f.write(str(highScore))
    f.close()
    pygame.quit()

if __name__ == '__main__':
    main()