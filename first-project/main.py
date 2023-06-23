import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
FPS_SEC = 60
FPS = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 400
HEIGHT = 600
SPEED = 5

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT)) # 디스플레이 좌측상단 꼭지점이 (0,0) 우측하단 꼭지점이 (최대, 최대)

pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    def draw(self, surface):
        surface.blit(self.image, self.rect)
# 스프라이트 설정
P1 = Player()
E1 = Enemy()

# 스프라이트 그룹핑
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# 새로운 유저이벤트 생성
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# 게임 루프 시작
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 2
        if event.type == pygame.QUIT: # 종료 조건
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)

    pygame.display.update() # 이 함수가 호출되기 전까진 화면 변화가 일어나지 않는다.
    FPS.tick(FPS_SEC)
