import asyncio
import pygame, sys
from pygame.locals import *
import random, time

# 초기화
pygame.init()

async def main():

    # FPS 설정
    FPS_SEC = 60
    FPS = pygame.time.Clock()

    # 색깔
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (245, 245, 66)

    # 게임 변수
    WIDTH = 400
    HEIGHT = 600
    SPEED = 1
    MONEY = 10000
    LEVEL = 2000
    rates = 0
    PM = BLACK
    PLUS = ""
    waiting = True
    size_list = ["short", "medium", "long", "llong"]

    # 폰트 설정
    font = pygame.font.SysFont("Verdana", 60)
    font_small = pygame.font.SysFont("Verdana", 20)

    start_text = font_small.render("Press Enter to Start", True, WHITE)
    game_success = font.render("You are rich!", True, YELLOW)
    game_over_text = font.render("Game Over", True, BLACK)
    effect_text_p5 = font_small.render("+5%", True, RED)
    effect_text_p10 = font_small.render("+10%", True, RED)
    effect_text_p25 = font_small.render("+25%", True, RED)
    effect_text_p50 = font_small.render("+50%", True, RED)
    effect_text_m5 = font_small.render("-5%", True, BLUE)
    effect_text_m10 = font_small.render("-10%", True, BLUE)
    effect_text_m25 = font_small.render("-25%", True, BLUE)
    effect_text_m50 = font_small.render("-50%", True, BLUE)


    # 픽셀아트 만들기
    red_stick = pygame.Surface((12,32))
    red_stick.fill(RED)
    red_stick_short = pygame.Surface((12,10))
    red_stick_short.fill(RED)
    red_stick_medium = pygame.Surface((12,32))
    red_stick_medium.fill(RED)
    red_stick_long = pygame.Surface((12,60))
    red_stick_long.fill(RED)
    red_stick_llong = pygame.Surface((12,90))
    red_stick_llong.fill(RED)
    pygame.image.save(red_stick,"red_stick.png")
    pygame.image.save(red_stick_short,"red_stick_short.png")
    pygame.image.save(red_stick_medium,"red_stick_medium.png")
    pygame.image.save(red_stick_long,"red_stick_long.png")
    pygame.image.save(red_stick_llong,"red_stick_llong.png")

    blue_stick = pygame.Surface((12,32))
    blue_stick.fill(BLUE)
    blue_stick_short = pygame.Surface((12,10))
    blue_stick_short.fill(BLUE)
    blue_stick_medium = pygame.Surface((12,32))
    blue_stick_medium.fill(BLUE)
    blue_stick_long = pygame.Surface((12,60))
    blue_stick_long.fill(BLUE)
    blue_stick_llong = pygame.Surface((12,90))
    blue_stick_llong.fill(BLUE)
    pygame.image.save(blue_stick,"blue_stick.png")
    pygame.image.save(blue_stick_short,"blue_stick_short.png")
    pygame.image.save(blue_stick_medium,"blue_stick_medium.png")
    pygame.image.save(blue_stick_long,"blue_stick_long.png")
    pygame.image.save(blue_stick_llong,"blue_stick_llong.png")

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT)) # 디스플레이 좌측상단 꼭지점이 (0,0) 우측하단 꼭지점이 (최대, 최대)

    pygame.display.set_caption("Game")

    class effect(pygame.sprite.Sprite):
        def __init__(self, effect, pos_x, pos_y):
            super().__init__()
            if effect == "p5":
                self.image = effect_text_p5
            elif effect == "p10":
                self.image = effect_text_p10
            elif effect == "p25":
                self.image = effect_text_p25
            elif effect == "p50":
                self.image = effect_text_p50
            elif effect == "m5":
                self.image = effect_text_m5
            elif effect == "m10":
                self.image = effect_text_m10
            elif effect == "m25":
                self.image = effect_text_m25
            else:
                self.image = effect_text_m50
                    
            self.rect = self.image.get_rect()
            self.rect.center = (pos_x+30, pos_y+30)
        
        def move(self):
            self.rect.move_ip(0, -3)
            if self.rect.bottom < 450:
                self.kill()
        
        def draw(self, surface):
            surface.blit(self.image, self.rect)


            

    class Yangbong(pygame.sprite.Sprite):
        def __init__(self, size):
            super().__init__()
            self.size = size
            self.image = pygame.image.load(f"red_stick_{size}.png")
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, WIDTH-40), 0)

        def move(self):
            self.rect.move_ip(0, SPEED)
            if self.rect.bottom > 600:
                rand_size = size_list[random.randint(0,3)]
                self.size = rand_size
                self.image = pygame.image.load(f"red_stick_{rand_size}.png")
                self.rect.top = 0
                self.rect.center = (random.randint(10, 390), 0)

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    class Embong(pygame.sprite.Sprite):
        def __init__(self, size):
            super().__init__()
            self.size = size
            self.image = pygame.image.load(f"blue_stick_{size}.png")
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, WIDTH-40), 0)

        def move(self):
            self.rect.move_ip(0, SPEED)
            if self.rect.bottom > 600:
                rand_size = size_list[random.randint(0,3)]
                self.size = rand_size
                self.image = pygame.image.load(f"blue_stick_{rand_size}.png")
                self.rect.top = 0
                self.rect.center = (random.randint(10, 390), 0)

        def draw(self, surface):
            surface.blit(self.image, self.rect)


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("player1.png")
            self.rect = self.image.get_rect()
            self.rect.center = (160,520)

        def move(self):
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
    Y1 = Yangbong(size_list[random.randint(0,3)])
    E1 = Embong(size_list[random.randint(0,3)])

    # 스프라이트 그룹핑
    yangbongs = pygame.sprite.Group()
    embongs = pygame.sprite.Group()
    yangbongs.add(Y1)
    embongs.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(Y1)
    all_sprites.add(E1)

    # 새로운 유저이벤트 생성
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, LEVEL)

    # 시작화면 생성
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(start_text, (100, 300))

    # 게임 루프 시작
    while True:
        pygame.display.update()
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        waiting = False

        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 1
            if event.type == pygame.QUIT: # 종료 조건
                pygame.quit()
                sys.exit()
        if rates > 0:
            PM = RED
            PLUS = "+"
        elif rates == 0:
            PM = BLACK
            PLUS = ""
        else:
            PM = BLUE
            PLUS = ""

        DISPLAYSURF.fill(WHITE)
        current_money = font_small.render(f"ACCOUNT: ${str(round(MONEY, 2))}", True, BLACK)
        current_rates = font_small.render(f"{PLUS}{round(rates, 2)}%", True, PM)
        DISPLAYSURF.blit(current_money, (10,10))
        DISPLAYSURF.blit(current_rates, (10,30))

        # 모든 객체 그려주기
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        
        # 충돌 상황 설정
        collided_yangbong = pygame.sprite.spritecollideany(P1, yangbongs)
        if collided_yangbong:
            if collided_yangbong.size == "short":
                MONEY *= 1.05
                P_EFFECT = effect("p5", collided_yangbong.rect.x, collided_yangbong.rect.y)
                all_sprites.add(P_EFFECT)
            elif collided_yangbong.size == "medium":
                MONEY *= 1.1
                P_EFFECT = effect("p10", collided_yangbong.rect.x, collided_yangbong.rect.y)
                all_sprites.add(P_EFFECT)
            elif collided_yangbong.size == "long":
                MONEY *= 1.25
                P_EFFECT = effect("p25", collided_yangbong.rect.x, collided_yangbong.rect.y)
                all_sprites.add(P_EFFECT)
            else:
                MONEY *= 1.5
                P_EFFECT = effect("p50", collided_yangbong.rect.x, collided_yangbong.rect.y)
                all_sprites.add(P_EFFECT)

            rates = MONEY / 100 - 100
            collided_yangbong.kill()
            if rates >= 1000:
                        
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_success, (15,250))
                
                pygame.display.update()
                for entity in all_sprites:
                        entity.kill() 
                time.sleep(2)
                pygame.quit()
                sys.exit()             
            Y1 = Yangbong(size_list[random.randint(0,3)])
            all_sprites.add(Y1)
            yangbongs.add(Y1)

        collided_embong = pygame.sprite.spritecollideany(P1, embongs)
        if collided_embong:
            if E1.size == "short":
                MONEY *= 0.95
                M_EFFECT = effect("m5", collided_embong.rect.x, collided_embong.rect.y)
                all_sprites.add(M_EFFECT)
            elif E1.size == "medium":
                MONEY *= 0.9
                M_EFFECT = effect("m10", collided_embong.rect.x, collided_embong.rect.y)
                all_sprites.add(M_EFFECT)
            elif E1.size == "long":
                MONEY *= 0.75
                M_EFFECT = effect("m25", collided_embong.rect.x, collided_embong.rect.y)
                all_sprites.add(M_EFFECT)
            else:
                MONEY *= 0.5
                M_EFFECT = effect("m50", collided_embong.rect.x, collided_embong.rect.y)
                all_sprites.add(M_EFFECT)

            rates = MONEY / 100 - 100
            
            collided_embong.kill()
            if rates <= -95:                     
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_over_text, (30,250))
                
                pygame.display.update()
                for entity in all_sprites:
                        entity.kill() 
                time.sleep(2)
                pygame.quit()
                sys.exit()             
            E1 = Embong(size_list[random.randint(0,3)])
            all_sprites.add(E1)
            embongs.add(E1)


        pygame.display.update() # 이 함수가 호출되기 전까진 화면 변화가 일어나지 않는다.
        FPS.tick(FPS_SEC)
        await asyncio.sleep(0)

asyncio.run(main())
