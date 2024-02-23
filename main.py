import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Say what the width and height of the window should be
WIDTH, HEIGHT = 900, 500
# WIN stands for window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Title of the game
pygame.display.set_caption("First Game")

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Tutorial Game', 'Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Tutorial Game', 'Assets', 'Gun+Silencer.mp3'))

# Font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# FPS
FPS = 60

# Velocity at which the spaceship and bullet travels
VEL = 5
BULLET_VEL = 7

# Max number of bullets
MAX_BULLETS = 3

# Dimiensions of width and height
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# This is howyou create a new event using pygame. Make sure to add a number in sequencialorderso that the events can perform different things
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Characters
# How to load images
# We imported os so that it's easier to find the images on other systems
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Tutorial Game', 'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Tutorial Game', 'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Tutorial Game', 'Assets', 'space.png')), (WIDTH, HEIGHT))


# Functions to draw a window, and averything within the window
# Make sure to fill teh background color before putting the background and characters
# This si so that the color used to fill in the window doesn't cover the background and characters
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # The .blit functions is used to display surfaces, which are characters, platforms, etc.
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(key_pressed, yellow):
        if key_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL
        if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
            yellow.x += VEL
        if key_pressed[pygame.K_w] and yellow.y + VEL > 0: # UP
            yellow.y -= VEL
        if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
            yellow.y += VEL

def red_handle_movement(key_pressed, red):
        if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -= VEL
        if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x += VEL
        if key_pressed[pygame.K_UP] and red.y + VEL > 0: # UP
            red.y -= VEL
        if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
            red.y += VEL

#Function to handle bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# Function to see who won
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2  - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# Main function
def main():
    # Create 2 rectangles that represent the spaceshis so that we can keep track of where they go
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    # Health
    red_health = 10
    yellow_health = 10

    # This helps keep FPS at 60
    clock = pygame.time.Clock()
    run = True
    while run:
        # This makes sure the FPS maxes out at 60, not over
        clock.tick(FPS)
        # This is to check if the user quits the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


# This if statement is saying that if the name of the main file is name main, then this is main file of the game
if __name__ == "__main__":
    main()