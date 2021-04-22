import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
back = pygame.image.load('cartoon.jpg')
pygame.display.set_caption("SPACE WAR")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)
# player
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
change = 0
# ghost

ghostimg = []
ghostX = []
ghostY = []
ghostX_change = []
ghostY_change = []
enemies = 5

for i in range(enemies):
    ghostimg.append(pygame.image.load('ghost.png'))
    ghostX.append(random.randint(0, 736))
    ghostY.append(random.randint(50, 100))
    ghostX_change.append(4)
    ghostY_change.append(40)


# bullets
bulletimg = pygame.image.load('bullets.png')
bulletX = 0
bulletY = 480
bulletX_change=0
bulletY_change = 1.5
state = "ready"

score=0
font=pygame.font.Font('googlebold.ttf',32)
textX=10
textY=10

scorefont=pygame.font.Font('googlebold.ttf',64)

def game_over():
    gameovervalue= scorefont.render("GAME OVER", True, (235, 255, 255))
    screen.blit(gameovervalue, (200,250))


def showscore(x,y):
    scorevalue=font.render("Score :" + str(score),True,(235,255,255))
    screen.blit(scorevalue,(x,y))

def player(x, y):
    screen.blit(playerimg, (x, y))


def ghost(x, y, i):
    screen.blit(ghostimg[i], (x, y))


def bulletfire(x, y):
    global state
    state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def collision(ghostX, ghostY, bulletX, bulletY):
    d = math.sqrt(math.pow(ghostX - bulletX, 2) + (math.pow(ghostY - bulletY, 2)))
    if d < 27:
        return True
    else:
        return False

run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(back, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -1
            if event.key == pygame.K_RIGHT:
                change = 1
            if event.key == pygame.K_SPACE:
                if state == "ready":
                    bulletX = playerX
                    bulletfire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0

    playerX += change
    if (playerX <= 0):
        playerX = 0
    elif (playerX >= 736):
        playerX = 736
    for i in range(enemies):

        if ghostY[i]>440:
            for j in range(enemies):
                ghostY[j]=2000
            game_over()
            break

        ghostX[i] += ghostX_change[i]
        if (ghostX[i] <= 0):
            ghostX_change[i] = 0.5
            ghostY[i] += ghostY_change[i]
        elif (ghostX[i] >= 736):
            ghostX_change[i] = -0.5
            ghostY[i] += ghostY_change[i]
        c = collision(ghostX[i], ghostY[i], bulletX, bulletY)
        if (c):
            bulletY = 480
            state = "ready"
            score += 1
            ghostX[i] = random.randint(0, 736)
            ghostY[i] = random.randint(50, 150)
        ghost(ghostX[i], ghostY[i], i)

    if bulletY <= 0:
        bulletY = 480
        state = "ready"
    if state == "fire":
        bulletfire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showscore(textX,textY)
    pygame.display.update()
