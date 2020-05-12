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

#Loading Images
playerImg = pygame.image.load('aircraft.png')
enemyImg = pygame.image.load('enemy.png')


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

# Creating Player class:
class Player:
    def __init__(self, x, y, x_change):
        self.x = x
        self.y = y
        self.x_change = x_change

    def draw(self):
        screen.blit(playerImg, (self.x, self.y))

class Enemy:
    def __init__(self, x, y, y_change):
        self.x = x
        self.y = y
        self.y_change = y_change

    def draw(self):
        screen.blit(enemyImg, (self.x, self.y))


#Creating player
ship = Player(370, 480, 0)

#Creating enemies
num_of_enemies = 6
enemies = [] #creating list to store enemies

for i in range(num_of_enemies): #for loop to create all the enemies
    i = Enemy(randint(0, 736), randint(-200, 100), 0.25) #These integers spawn enemies "above" the window. .25 is a good speed
    enemies.append(i)



# Creating bullet
bulletImg = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"  # "ready" - the bullet has not been fired

# #creating explosion
# explosion_img = pygame.image.load('explosion.png')


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
                ship.x_change = -5
            elif event.key == pygame.K_RIGHT:
                ship.x_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state is 'fire':  # This ensures you can't fire a bullet if bullet state is fire
                    pass
                else:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = ship.x
                    fire_bullet(bullet_x, bullet_y)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                ship.x_change = 0  # This ensures the ship stops when you lift up the key

    ship.x += ship.x_change  # updates position of player based on keys pressed

    # sets boundaries for the player
    if ship.x <= 0:
        ship.x = 0
    elif ship.x >= 736:
        ship.x = 736

    # setting movement for enemy
    for i in enemies:

        # #Game over mechanic
        # if i.y > 200:
        #     for j in range(num_of_enemies):
        #         enemy_y[j] = 2000
        #     game_over_text()
        #     break

        i.y += i.y_change

        # collision
        collision = isCollision(i.x, i.y, bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            i.x = randint(0, 736)
            i.y = randint(-200, 100)  # respawns enemy when there is a collision

        i.draw()

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'readu'
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    ship.draw()
    show_score(text_x, text_y)
    pygame.display.update()
