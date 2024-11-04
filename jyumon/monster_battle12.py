import pygame
import sys
import random  # randomモジュールをインポート
from voice_recognition import onsei

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

imgBtlBG = pygame.image.load("btlbg.png")
imgEnemy = pygame.image.load("knight.png")
imgEffect = pygame.image.load("effect_b.png")  # エフェクト画像

emy_x = 440 - imgEnemy.get_width() / 2
emy_y = 560 - imgEnemy.get_height()

# ボタンの設定
cast_button_rect = None
attack_button_rect = None
title_button_rect = None  # タイトルボタンの矩形
ranking_button_rect = None  # ランキングボタンの矩形
spell_value = 0
casted = False
damage_displayed = False  # ダメージ表示フラグ
effect_displayed = False  # エフェクト表示フラグ
effect_start_time = 0  # エフェクト表示開始時刻
result_displayed = False  # 結果表示フラグ
ranking_list = []  # ランキングリスト

def draw_battle(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])

    if effect_displayed:
        bg.blit(imgEffect, (emy_x - 100, emy_y))  # エフェクトを表示
    elif result_displayed:
        # 結果画面を描画
        result_text = fnt.render("Congratulations!", True, WHITE)
        result_rect = result_text.get_rect(center=(440, 360))  # 中央に配置
        bg.blit(result_text, result_rect)

        # 攻撃力を表示
        damage_text = f"Damage: {spell_value}"
        damage_surface = fnt.render(damage_text, True, WHITE)
        damage_rect = damage_surface.get_rect(center=(440, 420))  # 中央に配置
        bg.blit(damage_surface, damage_rect)

        # タイトルボタンを描画
        pygame.draw.rect(bg, BLACK, title_button_rect)
        title_label = fnt.render("title", True, (255, 255, 255))
        title_label_rect = title_label.get_rect(center=title_button_rect.center)
        bg.blit(title_label, title_label_rect)

    else:
        bg.blit(imgEnemy, (emy_x, emy_y))  # モンスターを表示
        enemy_text = fnt.render("Knight", True, WHITE)
        bg.blit(enemy_text, [370, 95])

        if not casted:  # 詠唱ボタンが押されていない場合
            pygame.draw.rect(bg, BLACK, cast_button_rect)
            cast_label = fnt.render("spell", True, (255, 255, 255))
            cast_label_rect = cast_label.get_rect(center=cast_button_rect.center)
            bg.blit(cast_label, cast_label_rect)
        else:  # 詠唱ボタンが押された後、攻撃ボタンを表示
            if not damage_displayed:  # ダメージが表示されていない場合
                pygame.draw.rect(bg, BLACK, attack_button_rect)
                attack_label = fnt.render("attack", True, (255, 255, 255))
                attack_label_rect = attack_label.get_rect(center=attack_button_rect.center)
                bg.blit(attack_label, attack_label_rect)
            else:  # ダメージを表示
                damage_text = f"{spell_value}"
                damage_surface = fnt.render(damage_text, True, WHITE)
                bg.blit(damage_surface, [360, 650])  # ダメージ表示位置

def draw_start_screen(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])  # 戦闘画面の背景を使用
    # タイトルを大きくしてホラーっぽくカラフルに
    title_font = pygame.font.Font(None, 80)  # フォントサイズを80に変更
    title_color = (random.randint(128, 255), random.randint(0, 128), random.randint(0, 128))  # ホラーっぽい色
    title_text = title_font.render("Monster Battle", True, title_color)
    title_text_rect = title_text.get_rect(center=(440, 300))  # 中央に配置
    bg.blit(title_text, title_text_rect)  # スタートテキストを描画

    global attack_button_rect, ranking_button_rect
    pygame.draw.rect(bg, BLACK, attack_button_rect)  # ボタンを描画
    button_label = fnt.render("start", True, (255, 255, 255))
    button_label_rect = button_label.get_rect(center=attack_button_rect.center)
    bg.blit(button_label, button_label_rect)  # ボタンのラベルを描画

    # ランキングボタンを描画
    ranking_button_rect = pygame.Rect(340, 500, 200, 50)  # ランキングボタンの位置とサイズ
    pygame.draw.rect(bg, BLACK, ranking_button_rect)
    ranking_label = fnt.render("ranking", True, (255, 255, 255))
    ranking_label_rect = ranking_label.get_rect(center=ranking_button_rect.center)
    bg.blit(ranking_label, ranking_label_rect)  # ランキングボタンのラベルを描画

def draw_ranking_screen(bg, fnt):
    bg.blit(imgBtlBG, [0, 0])  # 戦闘画面の背景を使用
    title_font = pygame.font.Font(None, 80)  # フォントサイズを80に変更
    title_color = (random.randint(128, 255), random.randint(0, 128), random.randint(0, 128))  # ホラーっぽい色
    title_text = title_font.render("Ranking", True, title_color)
    title_text_rect = title_text.get_rect(center=(440, 100))  # 中央に配置
    bg.blit(title_text, title_text_rect)  # ランキングタイトルを描画

    # ランキングリストを描画
    for i, damage in enumerate(sorted(ranking_list, reverse=True)[:10]):
        ranking_text = f"{i + 1}: Damage {damage}"
        ranking_surface = fnt.render(ranking_text, True, WHITE)
        bg.blit(ranking_surface, (360, 150 + i * 40))  # ランキング表示位置

    # タイトルボタンを描画
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
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 40)
    in_battle = False
    viewing_ranking = False

    cast_button_rect = pygame.Rect(340, 500, 200, 50)  # 詠唱ボタンの位置とサイズ
    attack_button_rect = pygame.Rect(340, 400, 200, 50)  # 攻撃ボタンの位置とサイズ
    title_button_rect = pygame.Rect(20, 650, 100, 50)  # タイトルボタンの位置とサイズ

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if in_battle and event.key == pygame.K_SPACE:
                    in_battle = False  # 戦闘をリセット
                if viewing_ranking and event.key == pygame.K_SPACE:
                    viewing_ranking = False  # ランキング画面をリセット
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if attack_button_rect.collidepoint(event.pos) and casted:
                        # 攻撃ボタンが押された場合
                        spell_value = random.randint(5, 20)  # ランダムな攻撃力を設定


                        spell_value = onsei.onsei()  # 音声認識


                        damage_displayed = True  # ダメージ表示フラグをセット
                        effect_displayed = True  # エフェクト表示フラグをセット
                        effect_start_time = pygame.time.get_ticks()  # エフェクト開始時刻を記録
                    elif cast_button_rect.collidepoint(event.pos) and not casted:
                        # 詠唱ボタンが押された場合
                        spell_value = random.randint(5, 20)  # ランダムな攻撃力を設定
                        casted = True  # 詠唱したことを示す
                    elif result_displayed and title_button_rect.collidepoint(event.pos):
                        # タイトルボタンが押された場合
                        ranking_list.append(spell_value)  # 攻撃力をランキングに追加
                        result_displayed = False  # 結果を非表示にし、スタート画面に戻る
                        casted = False  # 詠唱状態をリセット
                        damage_displayed = False  # ダメージ表示フラグをリセット
                        effect_displayed = False  # エフェクト表示フラグをリセット
                        in_battle = False  # 戦闘状態をリセット
                    elif ranking_button_rect.collidepoint(event.pos) and not in_battle:
                        # ランキングボタンが押された場合
                        viewing_ranking = True  # ランキング画面に移行
                    elif attack_button_rect.collidepoint(event.pos) and not in_battle:
                        # スタートボタンが押された場合
                        in_battle = True  # 戦闘状態に移行
                    elif viewing_ranking and title_button_rect.collidepoint(event.pos):
                        # タイトルボタンが押された場合
                        viewing_ranking = False  # ランキング画面を非表示にし、スタート画面に戻る

        # エフェクトが表示されている場合、1秒後に結果を表示
        if effect_displayed and (pygame.time.get_ticks() - effect_start_time > 1000):
            effect_displayed = False  # エフェクトを消す
            result_displayed = True  # 結果を表示

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
