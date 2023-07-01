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
    WIDTH = 360
    HEIGHT = 800
    SPEED = 1
    MONEY = 10000
    LEVEL = 2000
    rates = 0
    PM = BLACK
    PLUS = ""
    waiting = True
    mouse_pressed_left = False
    mouse_pressed_right = False
    size_list = ["short", "medium", "long", "llong"]

    # L과 R의 가로 크기와 구분선의 두께 정의
    l_width = 180
    divider_thickness = 2

    # 구분선의 좌표와 크기 계산
    divider_y = 600
    divider_height = HEIGHT - divider_y

    # 폰트 설정
    font = pygame.font.SysFont("Verdana", 40)
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
    l_text = font.render("L", True, YELLOW)
    r_text = font.render("R", True, YELLOW)



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
                self.rect.center = (random.randint(40, WIDTH-40), 0)

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
                self.rect.center = (random.randint(40, WIDTH-40), 0)

        def draw(self, surface):
            surface.blit(self.image, self.rect)


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("normal.png")
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH / 2,550)

        def move(self):
            if rates < -50:
                self.image = pygame.image.load("sad_face.png")
            elif rates > 200:
                self.image = pygame.image.load("smile_face.png")
            else:
                self.image = pygame.image.load("normal_face.png")    
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
    DISPLAYSURF.blit(start_text, ((WIDTH - start_text.get_width()) // 2 , (HEIGHT - start_text.get_height()) // 2))

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
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        waiting = False



        for event in pygame.event.get():
            if event.type == INC_SPEED:
                if SPEED < 40:
                    SPEED += 1.5
            if event.type == pygame.QUIT: # 종료 조건
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos:
                        x,y = event.pos
                        if x <= WIDTH / 2 and y > 600:
                            mouse_pressed_left = True
                        elif x > WIDTH / 2 and y > 600:
                            mouse_pressed_right = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed_left = False
                    mouse_pressed_right = False

        if P1.rect.left > 0 and mouse_pressed_left:
            P1.rect.move_ip(-5,0)
        if P1.rect.right < WIDTH and mouse_pressed_right:
            P1.rect.move_ip(5,0)            

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
            Y1 = Yangbong(size_list[random.randint(0,3)])
            all_sprites.add(Y1)
            yangbongs.add(Y1)
            if rates >= 1000:
                        
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_success, ((WIDTH - game_over_text.get_width()) // 2 , (HEIGHT - game_over_text.get_height()) // 2))
                
                pygame.display.update()
                for entity in all_sprites:
                        entity.kill() 
                time.sleep(2)
                waiting = True
                # pygame.quit()
                # sys.exit()
                while waiting:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == MOUSEBUTTONDOWN:
                            if event.button == 1:
                                waiting = False
                                SPEED = 1
                                MONEY = 10000
                                rates = 0             
                                all_sprites.add(P1)
                                all_sprites.add(Y1)
                                all_sprites.add(E1)
                                yangbongs.add(Y1)
                                embongs.add(E1)
                        elif event.type == KEYDOWN:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                                waiting = False
                                SPEED = 1
                                MONEY = 10000
                                rates = 0             
                                all_sprites.add(P1)
                                all_sprites.add(Y1)
                                all_sprites.add(E1)
                                yangbongs.add(Y1)
                                embongs.add(E1)           


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
            E1 = Embong(size_list[random.randint(0,3)])
            all_sprites.add(E1)
            embongs.add(E1)
            if rates <= -95:                     
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2 , (HEIGHT - game_over_text.get_height()) // 2))
                
                pygame.display.update()
                for entity in all_sprites:
                        entity.kill() 
                time.sleep(2)
                waiting = True
                # pygame.quit()
                # sys.exit()
                while waiting:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == MOUSEBUTTONDOWN:
                            if event.button == 1:
                                waiting = False
                                SPEED = 1
                                MONEY = 10000
                                rates = 0             
                                all_sprites.add(P1)
                                all_sprites.add(Y1)
                                all_sprites.add(E1)
                                yangbongs.add(Y1)
                                embongs.add(E1)

                        elif event.type == KEYDOWN:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                                waiting = False
                                SPEED = 1
                                MONEY = 10000
                                rates = 0             
                                all_sprites.add(P1)
                                all_sprites.add(Y1)
                                all_sprites.add(E1)
                                yangbongs.add(Y1)
                                embongs.add(E1)
        # 왼쪽 구역 그리기 (검은색 배경에 흰색 L)
        pygame.draw.rect(DISPLAYSURF, BLACK, (0, divider_y, l_width, divider_height))
        pygame.draw.rect(DISPLAYSURF, WHITE, (0, divider_y, l_width, divider_thickness))
        l_text_rect = l_text.get_rect(center=(l_width // 2, divider_y + divider_height // 2))
        DISPLAYSURF.blit(l_text, l_text_rect)

        # 오른쪽 구역 그리기 (검은색 배경에 흰색 R)
        r_x = l_width + divider_thickness
        r_width = WIDTH - r_x
        pygame.draw.rect(DISPLAYSURF, BLACK, (r_x, divider_y, r_width, divider_height))
        pygame.draw.rect(DISPLAYSURF, WHITE, (r_x, divider_y, r_width, divider_thickness))
        r_text_rect = r_text.get_rect(center=(r_x + r_width // 2, divider_y + divider_height // 2))
        DISPLAYSURF.blit(r_text, r_text_rect)        

        pygame.display.update() # 이 함수가 호출되기 전까진 화면 변화가 일어나지 않는다.
        FPS.tick(FPS_SEC)
        await asyncio.sleep(0)

asyncio.run(main())
