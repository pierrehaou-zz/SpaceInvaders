import pygame
import math
from random import randint
from pygame import mixer

# Initialized pygame library
pygame.init()

# created game window
screen = pygame.display.set_mode((772, 600))

# setting the background
background = pygame.image.load('m_background.jpg')
background_y = 0
background_y2 = background.get_height()

# Setting Title
pygame.display.set_caption("Pierre's Space Invaders")

# Background Music
mixer.music.load("game_music.wav")
mixer.music.play(-1)

# Loading Images
playerImg = pygame.image.load('aircraft.png')
enemyImg = pygame.image.load('enemy.png')
advanced_enemyImg = pygame.image.load('advanced_enemy.png')

# Setting icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Score
score_value = None
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

#Level Up Sound
level_sound = mixer.Sound("level_up.wav")
sound = False #sets the sound state so next level does not repeat


# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 32)

# Start game text
start_font = pygame.font.Font('freesansbold.ttf', 32)

#Enemy wave font
wave_font = pygame.font.Font('freesansbold.ttf', 32)

def redraw_background():  # This function redraws the window to make it look like its moving
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y2))

def wave_text(current_wave):
    text = font.render(f"{current_wave}", True, (255, 0, 0))
    screen.blit(text, (10, 50))

# game over text function
def game_over():
    over_text = over_font.render(f"GAME OVER", True, (255, 0, 0))
    restart_text = restart_font.render(f"Press 'Shift' to play again", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    screen.blit(restart_text, (200, 500))

#start game text
def start_game():
    start_text = start_font.render(f"Press 'Shift' to play", True, (255, 0, 0))
    screen.blit(start_text, (200, 250))


# resets variables to restart game
def init():
    global score_value
    score_value = 0
    ship.life = 5
    ship.y = 480
    for enemy in enemies:
        enemy.x = randint(0, 708)
        enemy.y = randint(-200, 0)
    for enemy in advanced_enemies:
        enemy.x = randint(0, 708)
        enemy.y = randint(-200, 0)
    bullet.bullet_state = "ready"


def show_score(x, y):
    score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_life(x, y, life):
    score = font.render(f"Life : {life}", True, (255, 255, 255))
    screen.blit(score, (x, y))


# creating collide functions

def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    # If they collide it will return (x,y) where thats the point of collision
    # if there is no overlap between to images it will return None
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))


def enemy_death(obj):  # when an enemy is killed
    explosion_sound = mixer.Sound("better_explosion.wav")
    explosion_sound.play()
    bullet.y = 480
    bullet.x = 1000
    bullet.bullet_state = 'ready'
    obj.x = randint(0, 708)
    obj.y = randint(-200, 0)  # respawns enemy when there is a collision


def enemy_attack(obj):  # when the enemy lands an attack on player
    explosion_sound = mixer.Sound("player_damage2.wav")
    explosion_sound.play()
    obj.x = randint(0, 708)
    obj.y = randint(-200, 0)  # respawns enemy when there is a collision


# function to add the number of enemies
def more_enemies(num):
    enemies = []  # creating list to store enemies

    for i in range(num):  # for loop to create all the enemies
        i = Enemy(randint(0, 720), randint(-200, 0),
                  0.5)  # These integers spawn enemies "above" the window. .25 is a good speed
        enemies.append(i)
    return enemies


# function to add the number of advanced enemies
def more_advanced_enemies(num):
    enemies = []  # creating list to store enemies

    for i in range(num):  # for loop to create all the enemies
        i = Advanced_Enemy(randint(0, 720), randint(-200, 0),
                           1)  # These integers spawn enemies "above" the window. .25 is a good speed
        enemies.append(i)
    return enemies


# Creating Player class:
class Player:
    def __init__(self, x, y, x_change):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.playerImg = playerImg
        self.mask = pygame.mask.from_surface(self.playerImg)
        self.life = 5

    def draw(self):
        screen.blit(playerImg, (self.x, self.y))


# Creating Enemy Class
class Enemy:
    def __init__(self, x, y, y_change):
        self.x = x
        self.y = y
        self.y_change = y_change
        self.enemyImg = enemyImg
        self.mask = pygame.mask.from_surface(self.enemyImg)

    def collision(self, obj):
        return collide(self, obj)

    def draw(self):
        screen.blit(self.enemyImg, (self.x, self.y))


class Advanced_Enemy:
    def __init__(self, x, y, y_change):
        self.x = x
        self.y = y
        self.y_change = y_change
        self.x_change = 0
        self.advanced_enemyImg = advanced_enemyImg
        self.mask = pygame.mask.from_surface(self.advanced_enemyImg)

    def collision(self, obj):
        return collide(self, obj)

    def draw(self):
        screen.blit(self.advanced_enemyImg, (self.x, self.y))


# Creating bullet class
class Bullet:

    def __init__(self, x, y, x_change, y_change, bullet_state):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.bullet_state = bullet_state
        self.bulletImg = pygame.image.load('bullet.png')
        self.mask = pygame.mask.from_surface(self.bulletImg)

    def fire_bullet(self):
        global bullet_state
        self.bullet_state = "fire"
        screen.blit(self.bulletImg, (self.x + 16, self.y + 10))  # setting the coordinates for the bullet when fired

    def collision(self, obj):
        return collide(self, obj)


# Creating player
ship = Player(370, 480, 0)

# Creating bullet
bullet = Bullet(1000, 1000, 0, 10, "ready")

# Creating enemies
num_of_enemies = 5
enemies = []  # creating list to store enemies

for i in range(num_of_enemies):  # for loop to create all the enemies
    i = Enemy(randint(0, 720), randint(-200, 0),
              0.5)  # These integers spawn enemies "above" the window. .25 is a good speed
    enemies.append(i)

# Creating advanced enemies
advanced_enemies = []  # creating list to store enemies
num_advanced_enemies = 1
for i in range(num_advanced_enemies):  # for loop to create all the enemies
    i = Advanced_Enemy(randint(0, 720), randint(-200, 0),
                       1)  # These integers spawn enemies "above" the window. .25 is a good speed
    advanced_enemies.append(i)

# Game Loop
running = True
while running:

    # This block renders a moving background
    redraw_background()
    background_y += 1.4
    background_y2 += 1.4
    if background_y > background.get_height():
        background_y = background.get_height() * -1
    if background_y2 > background.get_height():
        background_y2 = background.get_height() * -1

    for event in pygame.event.get():  # This loop cycles through all game events

        # If "red x" is pressed in gui the game loop stops
        if event.type == pygame.QUIT:
            running = False

        # Checks if there is a key stroke and if it is left or right
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.x_change = -3
            elif event.key == pygame.K_RIGHT:
                ship.x_change = 3
            elif event.key == pygame.K_SPACE:
                if bullet.bullet_state is 'fire':  # This ensures you can't fire a bullet if bullet state is fire
                    pass
                else:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet.x = ship.x
                    bullet.fire_bullet()
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # Allows players to restart game
                if ship.life == 0 or score_value == None:
                    init()
                    enemies = more_enemies(5)
                    advanced_enemies = more_advanced_enemies(1)
                else:
                    pass

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                ship.x_change = 0  # This ensures the ship stops when you lift up the key

    ship.x += ship.x_change  # updates position of player based on keys pressed

    # sets boundaries for the player
    if ship.x <= 0:
        ship.x = 0
    elif ship.x >= 708:
        ship.x = 708

    # start game mechanic
    if score_value == None:
        for j in enemies:  # moves enemies off the screen
            j.x = 3000
        for i in advanced_enemies:
            i.x = 5000
        start_game()

    # setting movement for enemy
    for i in enemies:

        # Game over mechanic
        if ship.life == 0:
            for j in enemies:  # moves enemies off the screen
                j.x = 3000
            ship.y = -300  # moves ship off screen

            game_over()

        i.y += i.y_change  # downward enemy movement
        if i.y > 600:
            i.y = randint(-350, 100)  # This respawns enemy if they go below screen

        # player bullet and enemy collision
        if bullet.collision(i) == None:
            pass
        else:
            score_value += 1
            enemy_death(i)

        # enemy and player collision
        if i.collision(ship) == None:
            pass
        else:
            if ship.life == 0:
                pass
            else:
                ship.life -= 1
                enemy_attack(i)

        # Increases difficulty as player score increases
        if score_value == None:
            pass
        elif i.y > 772 or i.y < 772:
            if score_value > 49 and len(enemies) < 6:  # the len piece ensures this if condition is ran only once
                enemies = more_enemies(10)
            elif score_value > 99 and len(enemies) < 15:
                enemies = more_enemies(15)

        i.draw()

    # setting movement for advanced enemy
    for i in advanced_enemies:

        # Game over mechanic
        if ship.life == 0:
            for j in advanced_enemies:  # moves enemies off the screen
                j.x = 3000
            ship.y = -300  # moves ship off screen

            game_over()

        # Advanced Enemy tracking system
        if i.x < ship.x:
            i.x_change = 0.25
        elif i.x > ship.x:
            i.x_change = -0.25

        # downward enemy movement
        i.x += i.x_change
        i.y += i.y_change
        if i.y > 600:
            i.y = randint(-350, 100)  # This respawns enemy if they go below screen

        # player bullet and enemy collision
        if bullet.collision(i) == None:
            pass
        else:
            score_value += 1
            enemy_death(i)

        # enemy and player collision
        if i.collision(ship) == None:
            pass
        else:
            if ship.life == 0:
                pass
            else:
                ship.life -= 1
                enemy_attack(i)

        # Adds advanced enemies as score increases
        if score_value == None:
            pass
        elif i.y > 772 or i.y < 772:
            if score_value > 14 and len(advanced_enemies) < 2:  # the len piece ensures this if condition is ran only once
                advanced_enemies = more_advanced_enemies(2)
            elif score_value > 49 and len(advanced_enemies) < 5:
                advanced_enemies = more_advanced_enemies(5)
            elif score_value > 69 and len(advanced_enemies) < 10:
                advanced_enemies = more_advanced_enemies(10)
            elif score_value > 99 and len(advanced_enemies) < 15:
                advanced_enemies = more_advanced_enemies(15)



        i.draw()

    # bullet movement
    if bullet.y <= 0:
        bullet.y = 480
        bullet.bullet_state = 'readu'
    if bullet.bullet_state is "fire":
        bullet.fire_bullet()
        bullet.y -= bullet.y_change

    # Renders the game level based on the score and plays next level sounds
    if score_value == None:
        pass
    elif score_value > 14 and score_value < 29:
        wave_text("Level 1")
        if sound is True:
            pass
        else:
            level_sound.play()
            sound = True
    elif score_value > 29 and score_value < 49:
        wave_text("Level 2")
        if sound is False:
            pass
        else:
            level_sound.play()
            sound = False
    elif score_value > 49 and score_value < 69:
        wave_text("Level 3")
        if sound is True:
            pass
        else:
            level_sound.play()
            sound = True
    elif score_value > 69 and score_value < 99:
        wave_text("Level 4")
        if sound is False:
            pass
        else:
            level_sound.play()
            sound = False
    elif score_value > 99:
        wave_text("You weren't supposed to get this far...")
        if sound is True:
            pass
        else:
            level_sound.play()
            sound = True

    ship.draw()
    show_life(650, 10, ship.life)
    show_score(text_x, text_y)
    pygame.display.update()
