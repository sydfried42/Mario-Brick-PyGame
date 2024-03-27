import random
import pygame
from pygame.locals import *
from pygame import mixer

mixer.init()
pygame.init()

screen_width = 1400
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

#define font
font = pygame.font.SysFont('Constantia', 30)

# bg_img = pygame.image.load("./images/davies-designs-studio-f5_lfi2S-d4-unsplash.jpg")
# screen.blit(bg_img, (0, 0))
# brick_img = pygame.image.load("/Users/mattclancy/Desktop/images/—Pngtree—red brick wall_5410880.png")

# replace ball with image
# x = 1
# y = 1
# scale = 1
ball_img = pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/mario_mushroom.png")

# replace paddle with image
paddle_img = pygame.image.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/mario_greentube.png")
# Scale the image to a larger size
new_paddle_width = 1200  # Adjust width as needed
new_paddle_height = 240  # Adjust height as needed
scale = 10
paddle_img = pygame.transform.scale(paddle_img, (new_paddle_width * scale, new_paddle_height * scale))


# rect = ball_img.get_rect()
# rect.center = (x, y)

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

#load music and sounds
pygame.mixer.music.load("/Users/mattclancy/development/code/se-prep/phase-3-project/assets/Super Mario Bros. Theme Song.mp3")
pygame.mixer.music.play(-1, 0.0)

#define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#brick wall class
class wall():
	def __init__(self):
		self.width = screen_width // cols
		self.height = 50
		self.brick_imgs = [
            pygame.image.load('/Users/mattclancy/development/code/se-prep/phase-3-project/assets/brick_1.png'),
            pygame.image.load('/Users/mattclancy/development/code/se-prep/phase-3-project/assets/brick_2.png'),
            pygame.image.load('/Users/mattclancy/development/code/se-prep/phase-3-project/assets/brick_3.png')
        ]

		# Scale the images smaller by 500%
		self.brick_imgs = [pygame.transform.scale(img, (int(self.width * 0.9), int(self.height * 0.9))) for img in self.brick_imgs]

	def create_wall(self):
		self.blocks = []
		#define an empty list for an individual block
		block_individual = []
		for row in range(rows):
			#reset the block row list
			block_row = []
			#iterate through each column in that row
			for col in range(cols):
				#generate x and y positions for each block and create a rectangle from that
				block_x = (col * self.width) 
				block_y = (row * self.height)
				rect = pygame.Rect(block_x, block_y, self.width, self.height)
				#assign block strength based on row
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1
				#create a list at this point to store the rect and colour data
				block_individual = [rect, strength]
				#append that individual block to the block row
				block_row.append(block_individual)
			#append the row to the full list of blocks
			self.blocks.append(block_row)

	def create_chaos(self):
		self.blocks = []
		block_individual = []
		for row in range(rows):
			block_row = []
			for col in range(cols):
				block_x = random.randint(0,col * self.width) 
				block_y = random.randint(0, row * self.height)
				rect = pygame.Rect(block_x, block_y, self.width, self.height)
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1
				block_individual = [rect, strength]
				block_row.append(block_individual)
			self.blocks.append(block_row)
			
            
	# def draw_wall(self):
		# for row in self.blocks:
			# for block in row:
				#assign a colour based on block strength
				# if block[1] == 3:
					# block_col = block_blue
				# elif block[1] == 2:
					# block_col = block_green
				# elif block[1] == 1:
					# block_col = block_red
				# pygame.draw.rect(screen, block_col, block[0])
				# pygame.draw.rect(screen, bg, (block[0]), 2)
	def draw_wall(self):
		for row in range(rows):
			for col in range(cols):
				brick_rect = pygame.Rect(col * self.width, row * self.height, self.width, self.height)
				brick_strength = wall.blocks[row][col][1]
				if self.blocks[row][col][1] > 0:
					brick_img = self.brick_imgs[brick_strength - 1]  # Adjust index to match strength
					screen.blit(brick_img, brick_rect)
					# Draw brick if it's not destroyed
					pygame.draw.rect(screen, block_col, self.blocks[row][col][0])


#paddle class
class paddle():
	def __init__(self):
		self.reset()


	def move(self):
		#reset movement direction
		self.direction = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = -1
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += self.speed
			self.direction = 1

	#def draw(self):
		# pygame.draw.rect(screen, paddle_col, self.rect)
		# pygame.draw.rect(screen, paddle_outline, self.rect, 3)


	def reset(self):
		#define paddle variables
		self.height = 20
		self.width = int(screen_width / cols)
		self.x = int((screen_width / 2) - (self.width / 2))
		self.y = screen_height - (self.height * 2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0


#ball class
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        # Collision detection with bricks
        for row in range(rows):
            for col in range(cols):
                if wall.blocks[row][col][1] > 0:
                    if self.rect.colliderect(wall.blocks[row][col][0]):
                        # Update brick strength
                        wall.blocks[row][col][1] -= 1
                        if wall.blocks[row][col][1] == 0:
                            wall.blocks[row][col] = (pygame.Rect(0, 0, 0, 0), 0)  # Mark brick as destroyed

        # Collision detection with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1

        # Collision detection with paddle
        if self.rect.colliderect(player_paddle.rect):
            self.speed_y *= -1

            # Adjust ball's horizontal speed based on paddle movement
            paddle_center = player_paddle.rect.x + player_paddle.width / 2
            distance_from_center = self.rect.centerx - paddle_center
            self.speed_x = distance_from_center / (player_paddle.width / 2) * self.max_speed

        # Update ball's position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check for game-over conditions
        if self.rect.bottom > screen_height:
            return True  # Game over: Ball went beyond the bottom of the screen
        return False  # Game continues

    def reset(self, x, y):
        self.rect = pygame.Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.max_speed = 5

        # Other reset logic...



run = True
while run:
    
	clock.tick(fps)

	screen.fill(bg)
	
	# screen.blit(bg_img, (0,0))
	# Load ball img
	ball_img = pygame.transform.scale(ball_img, (ball.ball_rad * 5, ball.ball_rad * 5))

# Load paddle img
paddle_img = pygame.transform.scale(paddle_img, (player_paddle.width, player_paddle.height))

# Create a wall
wall = wall()
wall.create_wall()

# Create paddle
player_paddle = paddle()

# Create ball
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

	#draw all objects
wall.draw_wall()
	# player_paddle.draw()
	# ball.draw()
if live_ball:
		#draw paddle
		screen.blit(paddle_img, (player_paddle.rect.x, player_paddle.rect.y))  # Blit paddle image onto screen
		player_paddle.move()
		#draw ball
		game_over = ball.move()
		if game_over != 0:
			live_ball = False
		screen.blit(ball_img, (ball.rect.x, ball.rect.y))  # Blit ball image onto screen


	#print player instructions
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