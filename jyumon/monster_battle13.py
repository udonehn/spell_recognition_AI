import pygame
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

imgBtlBG = pygame.image.load("dark-dungeon2.jpg")
imgEnemy = pygame.image.load("knight.png")
imgEffect = pygame.image.load("effect_b.png")  # エフェクト画像

emy_x = 800 - imgEnemy.get_width() / 2  # 中央に配置
emy_y = 600 - imgEnemy.get_height()

# ボタンの設定
cast_button_rect = None
attack_button_rect = None
title_button_rect = None
ranking_button_rect = None
spell_value = 0
casted = False
damage_displayed = False
effect_displayed = False
effect_start_time = 0
result_displayed = False
ranking_list = []

def draw_battle(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])

    if effect_displayed:
        bg.blit(imgEffect, (emy_x - 100, emy_y))
    elif result_displayed:
        result_text = fnt.render("Congratulations!", True, WHITE)
        result_rect = result_text.get_rect(center=(800, 450))  # 中央に配置
        bg.blit(result_text, result_rect)

        damage_text = f"Damage: {spell_value}"
        damage_surface = fnt.render(damage_text, True, WHITE)
        damage_rect = damage_surface.get_rect(center=(800, 520))  # 中央に配置
        bg.blit(damage_surface, damage_rect)

        pygame.draw.rect(bg, BLACK, title_button_rect)
        title_label = fnt.render("title", True, (255, 255, 255))
        title_label_rect = title_label.get_rect(center=title_button_rect.center)
        bg.blit(title_label, title_label_rect)

    else:
        bg.blit(imgEnemy, (emy_x, emy_y))
        enemy_text = fnt.render("Knight", True, WHITE)
        bg.blit(enemy_text, [640, 190])  # 中央に配置

        if not casted:
            pygame.draw.rect(bg, BLACK, cast_button_rect)
            cast_label = fnt.render("spell", True, (255, 255, 255))
            cast_label_rect = cast_label.get_rect(center=cast_button_rect.center)
            bg.blit(cast_label, cast_label_rect)
        else:
            if not damage_displayed:
                pygame.draw.rect(bg, BLACK, attack_button_rect)
                attack_label = fnt.render("attack", True, (255, 255, 255))
                attack_label_rect = attack_label.get_rect(center=attack_button_rect.center)
                bg.blit(attack_label, attack_label_rect)
            else:
                damage_text = f"{spell_value}"
                damage_surface = fnt.render(damage_text, True, WHITE)
                bg.blit(damage_surface, [640, 800])  # ダメージ表示位置

def draw_start_screen(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])
    title_font = pygame.font.Font(None, 80)
    title_color = (random.randint(128, 255), random.randint(0, 128), random.randint(0, 128))
    title_text = title_font.render("Monster Battle", True, title_color)
    title_text_rect = title_text.get_rect(center=(800, 300))
    bg.blit(title_text, title_text_rect)

    global attack_button_rect, ranking_button_rect
    pygame.draw.rect(bg, BLACK, attack_button_rect)
    button_label = fnt.render("start", True, (255, 255, 255))
    button_label_rect = button_label.get_rect(center=attack_button_rect.center)
    bg.blit(button_label, button_label_rect)

    ranking_button_rect = pygame.Rect(600, 600, 400, 50)  # ランキングボタンの位置とサイズ
    pygame.draw.rect(bg, BLACK, ranking_button_rect)
    ranking_label = fnt.render("ranking", True, (255, 255, 255))
    ranking_label_rect = ranking_label.get_rect(center=ranking_button_rect.center)
    bg.blit(ranking_label, ranking_label_rect)

def draw_ranking_screen(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])
    title_font = pygame.font.Font(None, 80)
    title_color = (random.randint(128, 255), random.randint(0, 128), random.randint(0, 128))
    title_text = title_font.render("Ranking", True, title_color)
    title_text_rect = title_text.get_rect(center=(800, 100))
    bg.blit(title_text, title_text_rect)

    for i, damage in enumerate(sorted(ranking_list, reverse=True)[:10]):
        ranking_text = f"{i + 1}: Damage {damage}"
        ranking_surface = fnt.render(ranking_text, True, WHITE)
        bg.blit(ranking_surface, (640, 150 + i * 40))

    pygame.draw.rect(bg, BLACK, title_button_rect)
    title_label = fnt.render("title", True, (255, 255, 255))
    title_label_rect = title_label.get_rect(center=title_button_rect.center)
    bg.blit(title_label, title_label_rect)

def main():
    global attack_button_rect, cast_button_rect, title_button_rect, ranking_button_rect
    global spell_value, casted, damage_displayed
    global effect_displayed, effect_start_time, result_displayed, ranking_list

    pygame.init()
    pygame.display.set_caption("Monster Battle")
    screen = pygame.display.set_mode((1600, 900))  # ウィンドウサイズを1600x900に設定
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 40)
    in_battle = False
    viewing_ranking = False

    cast_button_rect = pygame.Rect(600, 600, 400, 50)  # 詠唱ボタンの位置とサイズ
    attack_button_rect = pygame.Rect(600, 500, 400, 50)  # 攻撃ボタンの位置とサイズ
    title_button_rect = pygame.Rect(20, 800, 100, 50)  # タイトルボタンの位置とサイズ

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if in_battle and event.key == pygame.K_SPACE:
                    in_battle = False
                if viewing_ranking and event.key == pygame.K_SPACE:
                    viewing_ranking = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if attack_button_rect.collidepoint(event.pos) and casted:
                        spell_value = random.randint(5, 20)
                        damage_displayed = True
                        effect_displayed = True
                        effect_start_time = pygame.time.get_ticks()
                    elif cast_button_rect.collidepoint(event.pos) and not casted:
                        spell_value = random.randint(5, 20)
                        casted = True
                    elif result_displayed and title_button_rect.collidepoint(event.pos):
                        ranking_list.append(spell_value)
                        result_displayed = False
                        casted = False
                        damage_displayed = False
                        effect_displayed = False
                        in_battle = False
                    elif ranking_button_rect.collidepoint(event.pos) and not in_battle:
                        viewing_ranking = True
                    elif attack_button_rect.collidepoint(event.pos) and not in_battle:
                        in_battle = True
                    elif viewing_ranking and title_button_rect.collidepoint(event.pos):
                        viewing_ranking = False

        if effect_displayed and (pygame.time.get_ticks() - effect_start_time > 1000):
            effect_displayed = False
            result_displayed = True

        if in_battle:
            draw_battle(screen, font)
        elif viewing_ranking:
            draw_ranking_screen(screen, font)
        else:
            draw_start_screen(screen, font)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()

