import pygame
from pygame.locals import *
from pygame import mixer

mixer.init()
pygame.init()

# Screen dimensions
screen_width = 1400
screen_height = 800

# Initialize screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Font
font = pygame.font.SysFont('Constantia', 30)

# Colours
bg = (234, 218, 184)
text_col = (78, 81, 139)

#load music and sounds
pygame.mixer.music.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/Super Mario Bros. Theme Song.mp3")
pygame.mixer.music.play(-1, 0.0)

# Game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

# Load images
ball_img = pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/mario_mushroom.png").convert_alpha()
ball_img = pygame.transform.scale(ball_img, (30, 30))  # Adjust size as needed
bg_img = pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/background_3.png").convert()
paddle_img = pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/mario_greentube.png").convert_alpha()
paddle_img = pygame.transform.scale(paddle_img, (150, 30))  # Adjust size as needed

brick_images = {
    1: pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/brick_1.png").convert_alpha(),
    2: pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/brick_2.png").convert_alpha(),
    3: pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/brick_3.png").convert_alpha()
}
bg_x1 = 0
bg_x2 = bg_img.get_width()
bg_x3 = bg_img.get_width() * 2
scroll_speed = 0.5


for level, image in brick_images.items():
    brick_images[level] = pygame.transform.scale(image, (screen_width // cols, 50))

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Brick wall class
class Wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                else:
                    strength = 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[1] in brick_images:
                    screen.blit(brick_images[block[1]], block[0])

# Paddle class
class Paddle():
    def __init__(self):
        self.reset()

    def draw(self):
        screen.blit(paddle_img, self.rect)

    def reset(self):
        self.height = 20
        self.width = 150
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += 10
            self.direction = 1

# Ball class
class GameBall():
    def __init__(self, x, y):
        self.reset(x, y)

    def draw(self):
        screen.blit(ball_img, self.rect)

    def reset(self, x, y):
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y 
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed_x = 4
        self.speed_y = -4  # Adjust this value as needed
        self.speed_max = 5
        self.game_over = 0

    def move(self):
        # Ball movement logic
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with walls
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1

        if self.rect.top <= 0:
            self.speed_y *= -1

        # Ball collision with paddle
        if self.rect.colliderect(player_paddle.rect):
            self.speed_y *= -1

            # Adjust ball speed based on paddle movement
            self.speed_x += player_paddle.direction * 2
            if abs(self.speed_x) > self.speed_max:
                self.speed_x = self.speed_max * (self.speed_x / abs(self.speed_x))

        # Ball collision with bottom of the screen
        if self.rect.bottom >= screen_height:
            self.game_over = -1

        # Ball collision with bricks
        for row in wall.blocks:
            for brick in row:
                if self.rect.colliderect(brick[0]):
                    if abs(self.rect.bottom - brick[0].top) < 10 and self.speed_y > 0:
                        self.speed_y *= -1
                    elif abs(self.rect.top - brick[0].bottom) < 10 and self.speed_y < 0:
                        self.speed_y *= -1
                    elif abs(self.rect.right - brick[0].left) < 10 and self.speed_x > 0:
                        self.speed_x *= -1
                    elif abs(self.rect.left - brick[0].right) < 10 and self.speed_x < 0:
                        self.speed_x *= -1
                    if brick[1] > 1:
                        brick[1] -= 1
                    else:
                        brick[1] = 0

        return self.game_over


# Create wall, paddle, and ball instances
wall = Wall()
wall.create_wall()
player_paddle = Paddle()
ball = GameBall(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

# Game loop
run = True
while run:
    clock.tick(fps)
    screen.fill(bg)
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
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
    # Draw wall, paddle, and ball
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    # Move paddle if the game is active
    if live_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

    # Display game over message
    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_col, 500, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)

    pygame.display.update()

pygame.quit()
