import pygame
import sys

WHITE = (255, 255, 255)

imgBtlBG = pygame.image.load("btlbg.png")
imgEnemy = None

emy_num = 0
emy_x = 0
emy_y = 0

# スタート画面のボタンの設定
button_rect = None

def init_battle():
    global imgEnemy, emy_num, emy_x, emy_y
    emy_num = emy_num + 1
    if emy_num == 5:
        emy_num = 1
    imgEnemy = pygame.image.load("knight.png")
    emy_x = 440 - imgEnemy.get_width() / 2
    emy_y = 560 - imgEnemy.get_height()

def draw_battle(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])
    bg.blit(imgEnemy, [emy_x, emy_y])
    sur = fnt.render("knight", True, WHITE)
    bg.blit(sur, [360, 580])

def draw_start_screen(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])  # 戦闘画面の背景を使用
    start_text = fnt.render("", True, WHITE)
    start_text_rect = start_text.get_rect(center=(440, 300))  # 中央に配置
    bg.blit(start_text, start_text_rect)  # スタートテキストを描画
    title_text = fnt.render("Monster Battle", True, WHITE)
    title_text_rect = title_text.get_rect(center=(440, 300))  # 中央に配置
    bg.blit(title_text, title_text_rect)  # タイトルテキストを描画

    global button_rect
    button_rect = pygame.Rect(340, 400, 200, 50)  # ボタンの位置とサイズ
    pygame.draw.rect(bg, WHITE, button_rect)  # ボタンを描画
    button_label = fnt.render("start", True, (0, 0, 0))
    button_label_rect = button_label.get_rect(center=button_rect.center)
    bg.blit(button_label, button_label_rect)  # ボタンのラベルを描画

def main():
    pygame.init()
    pygame.display.set_caption("戦闘開始の処理")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    in_battle = False
    init_battle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if in_battle and event.key == pygame.K_SPACE:
                    init_battle()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    in_battle = True  # 戦闘状態に移行

        if in_battle:
            draw_battle(screen, font)
        else:
            draw_start_screen(screen, font)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
