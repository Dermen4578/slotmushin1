import pygame
import random
import sys
import time


pygame.init()
pygame.mixer.init()
# --------------------
# Налаштування
# --------------------
WIDTH = 900
HEIGHT = 600


wall = pygame.image.load("image/phone.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

clock = pygame.time.Clock()
pygame.mixer.music.load("saunds/backmusic.mp3")
pygame.mixer.music.play()

dep = pygame.mixer.Sound("saunds/prokrutka.mp3")
# --------------------
# Кольори
# --------------------
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 180, 0)
RED = (220, 50, 50)
GOLD = (255, 215, 0)
BLUE = (50, 120, 255)
GRAY = (80, 80, 80)

# --------------------
# Шрифти
# --------------------
title_font = pygame.font.SysFont("arial", 60, bold=True)
font = pygame.font.SysFont("arial", 36)

# --------------------
# Символи
# --------------------
symbols = ["A", "B", "C", "7", "$"]

slots = ["A", "A", "A"]

balance = 1000
bet = 100

game_state = "menu"

# --------------------
# Кнопка
# --------------------
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)

        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)

        screen.blit(text, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# --------------------
# Кнопки
# --------------------
play_button = Button(330, 250, 240, 70, "PLAY", GREEN)
exit_button = Button(330, 350, 240, 70, "EXIT", RED)

spin_button = Button(330, 500, 240, 70, "SPIN", BLUE)
menu_button = Button(20, 20, 180, 60, "MENU", GRAY)

# --------------------
# Меню
# --------------------
def draw_menu():
    screen.fill(BLACK)

    title = title_font.render("SLOT MACHINE", True, GOLD)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

    play_button.draw()
    exit_button.draw()

# --------------------
# Гра
# --------------------
def draw_game():
    screen.blit(wall, (-20,-10))


    # Баланс
    balance_text = font.render(f"Balance: ${balance}", True, WHITE)
    screen.blit(balance_text, (40, 100))

    # Ставка
    bet_text = font.render(f"Bet: ${bet}", True, WHITE)
    screen.blit(bet_text, (40, 150))

    # Слоти
    slot_w = 180
    slot_h = 180
    gap = 25

    start_x = WIDTH//2 - (slot_w * 3 + gap * 2)//2

    for i in range(3):

        rect = pygame.Rect(
            start_x + i * (slot_w + gap),
            200,
            slot_w,
            slot_h
        )

        pygame.draw.rect(screen, WHITE, rect, border_radius=15)
        pygame.draw.rect(screen, GOLD, rect, 5, border_radius=15)

        symbol = title_font.render(slots[i], True, BLACK)

        symbol_rect = symbol.get_rect(center=rect.center)

        screen.blit(symbol, symbol_rect)

    spin_button.draw()
    menu_button.draw()

# --------------------
# Прокрутка
# --------------------
def spin():
    global balance
    global slots

    if balance < bet:
        return
    dep.play()
    balance -= bet

    slots = [
        random.choice(symbols),
        random.choice(symbols),
        random.choice(symbols)
    ]

    # Виграш
    if slots[0] == slots[1] == slots[2]:
        balance += bet * 5


    elif slots[0] == slots[1] or slots[1] == slots[2]:
        balance += bet * 2

  #  else:
  #      lose.play()

# --------------------
# Головний цикл
# --------------------
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        # Вихід
        if event.type == pygame.QUIT:
            running = False

        # Мишка
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # Меню
            if game_state == "menu":

                if play_button.clicked(mouse_pos):
                    game_state = "game"

                if exit_button.clicked(mouse_pos):
                    running = False

            # Гра
            elif game_state == "game":

                if spin_button.clicked(mouse_pos):
                    spin()

                if menu_button.clicked(mouse_pos):
                    game_state = "menu"

        # Клавіатура
        if event.type == pygame.KEYDOWN:

            if game_state == "game":

                if event.key == pygame.K_SPACE:
                    spin()

                if event.key == pygame.K_UP:
                    bet += 50

                if event.key == pygame.K_DOWN:
                    bet -= 50

                    if bet < 50:
                        bet = 50

    # Малювання
    if game_state == "menu":
        draw_menu()

    if game_state == "game":
        draw_game()

    pygame.display.update()

pygame.quit()
sys.exit()