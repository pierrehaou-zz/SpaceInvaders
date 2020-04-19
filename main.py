import pygame

#Initialized pygame library
pygame.init()

#created game window
screen = pygame.display.set_mode((800,600))

#Setting Title
pygame.display.set_caption("Pierre's Space Invaders")

#Setting icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#Creating Player
playerImg = pygame.image.load('aircraft.png')
player_x = 370 #sets the x coordinate of the player image
player_y = 480 #sets the y coordinate of the player image

def player():
    screen.blit(playerImg, (player_x, player_y)) #This renders player image onto screen


# Game Loop
running = True
while running:

    # This sets the background, takes RGB as input
    screen.fill((51, 102, 153))

    for event in pygame.event.get(): #This loop cycles through all game events
        if event.type == pygame.QUIT: #If "red x" is pressed in gui the game loop stops
            running = False


    player() #This must be after the color fill!

    pygame.display.update()



