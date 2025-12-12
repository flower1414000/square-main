import pygame
import sys
import random

# Настройки
W = 600
H = 400
CELL = 20
FPS = 10  # Медленнее для змейки

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Инициализация змейки
snake = [(W//2//CELL, H//2//CELL)]  # Голова в центре
direction = (1, 0)  # Направление вправо
score = 0
game_over = False

# Еда
def new_food():
    while True:
        x = random.randint(0, W//CELL - 1)
        y = random.randint(0, H//CELL - 1)
        if (x, y) not in snake:
            return (x, y)

food = new_food()

# Основной цикл
while True:
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if e.type == pygame.KEYDOWN:
            if game_over:
                if e.key == pygame.K_r:  # Рестарт
                    snake = [(W//2//CELL, H//2//CELL)]
                    direction = (1, 0)
                    score = 0
                    game_over = False
                    food = new_food()
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                # Управление направлением
                if e.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif e.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif e.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif e.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
    
    # Движение змейки (если игра не окончена)
    if not game_over:
        # Новая позиция головы
        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)
        
        # Проверка столкновений
        # Со стенами
        if (head_x < 0 or head_x >= W//CELL or 
            head_y < 0 or head_y >= H//CELL):
            game_over = True
        
        # С собой
        if new_head in snake:
            game_over = True
        
        # Если игра продолжается
        if not game_over:
            # Добавляем новую голову
            snake.insert(0, new_head)
            
            # Проверяем съела ли змейка еду
            if new_head == food:
                score += 1
                food = new_food()
                # Хвост не удаляем (змея растёт)
            else:
                # Удаляем хвост
                snake.pop()
    
    # Отрисовка
    screen.fill(BLACK)
    
    # Рисуем сетку
    for x in range(0, W, CELL):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, H))
    for y in range(0, H, CELL):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (W, y))
    
    # Рисуем еду
    pygame.draw.rect(screen, RED, 
                     (food[0]*CELL, food[1]*CELL, CELL, CELL))
    
    # Рисуем змейку
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN  # Голова ярче
        pygame.draw.rect(screen, color, (x*CELL, y*CELL, CELL, CELL))
        pygame.draw.rect(screen, (0, 150, 0), (x*CELL, y*CELL, CELL, CELL), 1)
    
    # Счёт
    screen.blit(font.render(f"Счёт: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Длина: {len(snake)}", True, WHITE), (W-150, 10))
    
    # Сообщение о конце игры
    if game_over:
        screen.blit(font.render("ИГРА ОКОНЧЕНА", True, RED), 
                   (W//2-100, H//2-50))
        screen.blit(font.render("R - новая игра", True, WHITE), 
                   (W//2-80, H//2))
        screen.blit(font.render("ESC - выход", True, WHITE), 
                   (W//2-60, H//2+40))
    
    pygame.display.flip()
    clock.tick(FPS)
input()