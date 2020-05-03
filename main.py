import pygame
from random import randint

# Initialized pygame library
pygame.init()

# created game window
screen = pygame.display.set_mode((800, 600))

# Setting Title
pygame.display.set_caption("Pierre's Space Invaders")

# Setting icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Creating Player
playerImg = pygame.image.load('aircraft.png')
player_x = 370  # sets the x coordinate of the player image
player_y = 480  # sets the y coordinate of the player image
player_x_change = 0

# Creating enemy
enemyImg = pygame.image.load('enemy.png')
enemy_x = randint(0, 800)  # sets the x coordinate of the enemy image
enemy_y = randint(50, 150 )  # sets the y coordinate of the enemy image
enemy_x_change = 0.3
enemy_y_change = 30


def player(x, y):
    screen.blit(playerImg, (x, y))  # This renders player image onto screen


def enemy(x, y):
    screen.blit(enemyImg, (x, y))  # This renders enemy image onto screen


# Game Loop
running = True
while running:

    # This sets the background, takes RGB as input
    screen.fill((51, 102, 153))

    for event in pygame.event.get():  # This loop cycles through all game events

        # If "red x" is pressed in gui the game loop stops
        if event.type == pygame.QUIT:
            running = False

        # Checks if there is a key stroke and if it is left or right
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            elif event.key == pygame.K_RIGHT:
                player_x_change = 0.3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player_x_change = 0  # This ensures the ship stops when you lift up the key

    player_x += player_x_change  # updates position of player based on keys pressed

    # sets boundaries for the player
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    enemy_x += enemy_x_change

    # setting movement for enemy
    if enemy_x <= 0:
        enemy_x_change = 0.3
        enemy_y += enemy_y_change
    elif enemy_x >= 736:
        enemy_x_change = -0.3
        enemy_y += enemy_y_change

    player(player_x, player_y)  # This must be after the color fill!
    enemy(enemy_x, enemy_y)
    pygame.display.update()
