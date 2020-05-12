import pygame
import math
from random import randint
from pygame import mixer

# Initialized pygame library
pygame.init()

# created game window
screen = pygame.display.set_mode((800, 600))

# setting the background
background = pygame.image.load('background.jpg')

# Setting Title
pygame.display.set_caption("Pierre's Space Invaders")

#Background Music
mixer.music.load("game_music.wav")
mixer.music.play(-1)

# Setting icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render(f"GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def show_score(x,y):
    score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

# Creating Player
playerImg = pygame.image.load('aircraft.png')
player_x = 370  # sets the x coordinate of the player image
player_y = 480  # sets the y coordinate of the player image
player_x_change = 0

# Creating enemies
enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemy_x.append(randint(0, 736))  # sets the x coordinate of the enemy image
    enemy_y.append(randint(50, 150))  # sets the y coordinate of the enemy image
    enemy_x_change.append(1)
    enemy_y_change.append(30)

# Creating bullet
bulletImg = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"  # "ready" - the bullet has not been fired

# #creating explosion
# explosion_img = pygame.image.load('explosion.png')


def player(x, y):
    screen.blit(playerImg, (x, y))  # This renders player image onto screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # This renders enemy image onto screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # setting the coordinates for the bullet when fired


def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    """Determines when there is a collision between bullet and enemy"""
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # This sets the background, takes RGB as input
    screen.fill((0, 0, 0))

    # setting the background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # This loop cycles through all game events

        # If "red x" is pressed in gui the game loop stops
        if event.type == pygame.QUIT:
            running = False

        # Checks if there is a key stroke and if it is left or right
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            elif event.key == pygame.K_RIGHT:
                player_x_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state is 'fire':  # This ensures you can't fire a bullet if bullet state is fire
                    pass
                else:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player_x_change = 0  # This ensures the ship stops when you lift up the key

    player_x += player_x_change  # updates position of player based on keys pressed

    # sets boundaries for the player
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # setting movement for enemy
    for i in range(num_of_enemies):

        #Game over mechanic
        if enemy_y[i] > 200:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 1
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -1
            enemy_y[i] += enemy_y_change[i]

        # collision
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemy_x[i] = randint(0, 736)
            enemy_y[i] = randint(50, 150)  # respawns enemy when there is a collision

        enemy(enemy_x[i], enemy_y[i], i)

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'readu'
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)  # This must be after the color fill!
    show_score(text_x, text_y)
    pygame.display.update()
