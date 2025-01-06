import pygame
import random
import math
import time
from pygame.locals import *
from pygame import mixer

# intialize the pygame
pygame.init()

# Background image
background = pygame.image.load("background.jpg")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Game over
game_over = False

# create the screen for the game
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('shootingship.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(30, 750))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet coordinates

# ready - it means you cant see bullet but its ready to fire
# Fire -  The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# score

score_value = 0
topScore = 0
scoreAdded = False
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text

over_font = pygame.font.Font('freesansbold.ttf', 64)

# Play Again

play_font = pygame.font.Font('freesansbold.ttf', 48)


def showscore(x, y,val):
    score = font.render("Score: " + str(val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def showTopScore(x, y,val):
    score = font.render("Top Score: " + str(val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



def play_again_text():
    play_text = play_font.render("Press any key to play again ", True, (255, 255, 255))
    screen.blit(play_text, (100, 320))



def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    if distance < 27:
        return True
    else:
        return False


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Game Loop
running = True
while running:
    # RGB - Red Green Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and bullet_state == "ready":  # In order to avoid changing location everytime
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                fire_bullet(playerX, bulletY)  # Space bar is pressed
                bulletX = playerX
            if game_over:
                if event.type == pygame.KEYDOWN:
                    score_value = 0
                    scoreAdded = False
                    for i in range(num_of_enemies):
                        enemyX[i] = random.randint(20, 730)
                        enemyY[i] = random.randint(50, 150)
                        game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # Setting the boundary
    if int(playerX) < 10:
        playerX = 10
    elif int(playerX) > 740:
        playerX = 740

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            play_again_text()
            if score_value >  topScore:
                topScore = score_value
            game_over = True

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 10:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 740:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound("explosion.wav")
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(20, 730)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    yCo = 10

    player(playerX, playerY)
    showscore(textX, textY,score_value)
    showTopScore(550,10,topScore)
    pygame.display.update()
