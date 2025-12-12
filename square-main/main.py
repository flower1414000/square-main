import pygame
import sys
import random

# Настройки
W = 800
H = 600
CELL = 30

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Сбор квадратов")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Игрок
px = W // 2 // CELL
py = H // 2 // CELL
score = 0
best = 0
speed = 10
game_over = False

# Красный квадрат
def new_red():
    while True:
        rx = random.randint(0, W // CELL - 1)
        ry = random.randint(0, H // CELL - 1)
        if not (rx == px and ry == py):
            return rx, ry

rx, ry = new_red()

# Игровой цикл
while True:
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if e.type == pygame.KEYDOWN:
            if game_over:
                if e.key == pygame.K_SPACE:
                    px = W // 2 // CELL
                    py = H // 2 // CELL
                    score = 0
                    speed = 10
                    game_over = False
                    rx, ry = new_red()
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                if e.key == pygame.K_ESCAPE:
                    game_over = True
    
    # Движение
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if px > 0:
                px -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if px < W // CELL - 1:
                px += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if py > 0:
                py -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if py < H // CELL - 1:
                py += 1
    
    # Проверка столкновения
    if not game_over and px == rx and py == ry:
        score += 1
        best = max(best, score)
        speed = min(30, speed + 1)
        rx, ry = new_red()
    
    # Отрисовка
    screen.fill(BLACK)  # Черный фон
    
    # Красный квадрат
    pygame.draw.rect(screen, RED, (rx * CELL, ry * CELL, CELL, CELL))
    
    # Зеленый кубик
    pygame.draw.rect(screen, GREEN, (px * CELL, py * CELL, CELL, CELL))
    pygame.draw.rect(screen, (0, 200, 0), (px * CELL, py * CELL, CELL, CELL), 3)
    
    # Счет
    screen.blit(font.render(f"Счет: {score}", True, GOLD), (10, 10))
    screen.blit(font.render(f"Рекорд: {best}", True, GOLD), (W - 150, 10))
    
    # Сообщение
    if game_over:
        screen.blit(font.render("ИГРА ОКОНЧЕНА", True, RED), (W//2-100, H//2-50))
        screen.blit(font.render("ПРОБЕЛ - новая игра", True, WHITE), (W//2-120, H//2))
        screen.blit(font.render("ESC - выход", True, WHITE), (W//2-80, H//2+40))
    
    pygame.display.flip()
    clock.tick(speed)
input()