import random
import pygame
from pygame.locals import *

pygame.init()

screen_width = 1400
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

#define font
font = pygame.font.SysFont('Constantia', 30)

# Load the background image
bg_img = pygame.image.load("/Users/kevincardenas/Development/code/phase-3/phase-3-project/assets/background (3).png").convert()

# Load other images
ball_img = pygame.image.load("/Users/kevincardenas/Development/code/phase-3/phase-3-project/assets/mario_mushroom.png")
paddle_img = pygame.image.load("/Users/kevincardenas/Development/code/phase-3/phase-3-project/assets/mario_greentube.png")
# Scale the paddle image to fit the screen width
new_paddle_width = 1200  # Adjust width as needed
scale = 10
paddle_img = pygame.transform.scale(paddle_img, (new_paddle_width * scale, 240 * scale))

#define colours
bg = (234, 218, 184)
#block colours
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
#paddle colours
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
#text colour
text_col = (78, 81, 139)

# Load music and sounds
pygame.mixer.music.load("/Users/kevincardenas/Development/code/phase-3/phase-3-project/assets/Super Mario Bros. Theme Song.mp3")
pygame.mixer.music.play(-1, 0.0)

# Define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Initialize background x-coordinates
bg_x1 = 0
bg_x2 = bg_img.get_width()
bg_x3 = bg_img.get_width() * 2

# Define scrolling speed
scroll_speed = 0.5  # Adjust as needed for slower scrolling

# Main game loop
run = True
while run:
    screen.fill(bg)

    # Draw three copies of the background image side by side for infinite scrolling
    screen.blit(bg_img, (bg_x1, 0))
    screen.blit(bg_img, (bg_x2, 0))
    screen.blit(bg_img, (bg_x3, 0))

    # Update background x-coordinates for horizontal scrolling
    bg_x1 -= scroll_speed
    bg_x2 -= scroll_speed
    bg_x3 -= scroll_speed

    # If the first background image goes off the screen, reset its position
    if bg_x1 <= -bg_img.get_width():
        bg_x1 = bg_img.get_width() * 2

    # If the second background image goes off the screen, reset its position
    if bg_x2 <= -bg_img.get_width():
        bg_x2 = bg_img.get_width() * 2

    # If the third background image goes off the screen, reset its position
    if bg_x3 <= -bg_img.get_width():
        bg_x3 = bg_img.get_width() * 2

    # Print player instructions
    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_col, 500, screen_height // 2 + 100)
            draw_text('Press C to create chaos!!!', font, text_col, 500, screen_height // 2 + 50)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_col, 500, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 500, screen_height // 2 + 100)
            draw_text('Press C to create chaos!!!', font, text_col, 500, screen_height // 2 + 50)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_col, 500, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 500, screen_height // 2 + 100)
            draw_text('Press C to create chaos!!!', font, text_col, 500, screen_height // 2 + 50)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
        if event.type == pygame.KEYDOWN and live_ball == False:
            if event.key == K_c:
                live_ball = True
                ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
                player_paddle.reset()
                wall.create_chaos()

    pygame.display.update()

pygame.quit()