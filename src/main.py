import pygame


pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

fpsClock= pygame.time.Clock()

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


live_ball = False
margin= 50
font= pygame.font.SysFont('Arial', 30)
cpu_score= 0
player_score= 0
fps= 60
winner = 0
speed_increase = 0
bg = (50, 25, 50)
white= (255, 255, 255)

def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen, white, (0, margin), (SCREEN_WIDTH, margin))


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

class Paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y, 20, 100))
        self.speed = 5

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip((0, -1 * self.speed))
        if key[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip((0, self.speed))

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

    def ai(self):
        if self.rect.centery < pong.rect.top and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, self.speed)
        if self.rect.centery > pong.rect.top and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)


class Ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        if self.rect.top < margin:
            self.speed_y *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > SCREEN_WIDTH:
            self.winner = -1       
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    
    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.radius= 8
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0


player_paddle = Paddle(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2)
cpu_paddle = Paddle(20, SCREEN_HEIGHT // 2 )


pong = Ball(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)


run = True
while run == True:

    fpsClock.tick(fps)

    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, white, 20, 15)
    draw_text('P1: ' + str(player_score), font, white, SCREEN_WIDTH -100, 15)
    draw_text('Ball Speed: ' + str(abs(pong.speed_x)), font, white, SCREEN_WIDTH // 2 - 100, 15)
    
    player_paddle.draw()
    cpu_paddle.draw()
    if live_ball == True:
        speed_increase += 1
        winner = pong.move()
        if winner == 0: 
            player_paddle.move()
            cpu_paddle.ai()
            pong.draw()
        else: 
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                cpu_score += 1

    if live_ball == False:
        if winner == 0:
            draw_text('CLICK ANYWHER TO START', font, white, 100, SCREEN_HEIGHT // 2 - 100)
        if winner == 1:
            draw_text('You Scored', font, white, 220, SCREEN_HEIGHT // 2 - 100)
            draw_text('CLICK ANYWHERE TO START', font, white, 100, SCREEN_HEIGHT // 2 - 50)
        if winner == -1:
            draw_text('CPU Scored', font, white, 220, SCREEN_HEIGHT // 2 - 100)
            draw_text('CLICK ANYWHERE TO START', font, white, 100, SCREEN_HEIGHT // 2 - 50)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)

    if speed_increase> 500:
        speed_increase= 0 
        if pong.speed_x < 0:
            pong.speed_x -= 1
        if pong.speed_x > 0:
            pong.speed_x += 1
        if pong.speed_y < 0:
            pong.speed_y -=1
        if pong.speed_y > 0:
            pong.speed_y +=1

            
    pygame.display.update()
pygame.quit()