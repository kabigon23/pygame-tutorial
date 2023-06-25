import pygame, sys
from pygame.locals import *

pygame.init() # pygame 모듈 초기화

FPS = 60 # 초당 프레임 수

# 디스플레이 크기
WIDTH = 400
HEIGHT = 300

# 기타 게임에 필요한 값
BLACK = (0, 0, 0)
SPEED = [2, 2]

ball = pygame.image.load("soccer_ball.png")
ball_rect = ball.get_rect()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    ball_rect.move_ip(SPEED)
    if ball_rect.left < 0 or ball_rect.right > WIDTH:
        SPEED[0] = -SPEED[0]
    if ball_rect.top < 0 or ball_rect.bottom > HEIGHT:
        SPEED[1] = -SPEED[1]

    screen.fill(BLACK)
    screen.blit(ball, ball_rect)

    pygame.display.update()
    clock.tick(FPS)