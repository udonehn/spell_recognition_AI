import tkinter as tk
import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other):
        damage = random.randint(1, self.attack_power)
        other.health -= damage
        return damage

    def is_alive(self):
        return self.health > 0

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("モンスター戦闘ゲーム")

        self.start_screen()

    def start_screen(self):
        # スタート画面
        self.clear_screen()

        start_label = tk.Label(self.root, text="モンスター戦闘ゲーム", font=("Helvetica", 24))
        start_label.pack(pady=20)

        start_button = tk.Button(self.root, text="スタート", command=self.battle_screen)
        start_button.pack(pady=20)

    def battle_screen(self):
        # 戦闘画面
        self.clear_screen()

        self.player = Character("Hero", 20, 5)
        self.monster = Character("Goblin", 15, 3)

        self.battle_label = tk.Label(self.root, text=f"あなたのHP: {self.player.health}\nモンスターのHP: {self.monster.health}", font=("Helvetica", 16))
        self.battle_label.pack(pady=20)

        attack_button = tk.Button(self.root, text="攻撃", command=self.attack)
        attack_button.pack(pady=10)

        run_button = tk.Button(self.root, text="逃げる", command=self.start_screen)
        run_button.pack(pady=10)

    def attack(self):
        damage_to_monster = self.player.attack(self.monster)
        self.battle_label.config(text=f"あなたのHP: {self.player.health}\nモンスターのHP: {self.monster.health}\nあなたはモンスターに{damage_to_monster}のダメージを与えた！")

        if not self.monster.is_alive():
            self.battle_label.config(text="モンスターを倒した！")
            return
        
        damage_to_player = self.monster.attack(self.player)
        self.battle_label.config(text=f"あなたのHP: {self.player.health}\nモンスターのHP: {self.monster.health}\nモンスターはあなたに{damage_to_player}のダメージを与えた！")

        if not self.player.is_alive():
            self.battle_label.config(text="あなたは倒れてしまった...")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
