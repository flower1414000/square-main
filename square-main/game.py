import pygame
import random
import sys

from config import *
import messages


class SnakeGame:
    def _init_(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption(messages.WINDOW_TITLE)
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 48)
        
        # Начальные значения
        self.reset_game()
    
    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        # Начальная позиция головы змейки (в центре экрана)
        head_x = WIN_W // 2
        head_y = WIN_H // 2
        
        # Создаем змейку как список прямоугольников
        # Змейка растёт вверх от головы
        self.snake = []
        for i in range(INITIAL_LENGTH):
            segment = pygame.Rect(
                head_x,
                head_y + i * SNAKE_SIZE,  # Каждый следующий сегмент ниже
                SNAKE_SIZE,
                SNAKE_SIZE
            )
            self.snake.append(segment)
        
        # Направление движения (изначально вверх)
        self.direction = DIR_UP
        self.next_direction = DIR_UP  # Следующее направление (для плавной смены)
        
        # Счёт и флаг игры
        self.score = 0
        self.game_over = False
        
        # Таймер движения (двигаем змейку с интервалом)
        self.move_timer = 0
        self.move_delay = 1.0 / (SNAKE_SPEED / SNAKE_SIZE)  # Время между шагами
        
        # Создаем первое яблоко
        self.spawn_apple()
    
    def spawn_apple(self):
        """Создание яблока в случайном месте, не на змейке"""
        margin = 10
        tries = 0
        
        while tries < 200:
            # Генерируем случайные координаты
            x = random.randint(margin, WIN_W - APPLE_SIZE - margin)
            y = random.randint(margin, WIN_H - APPLE_SIZE - margin)
            
            apple_rect = pygame.Rect(x, y, APPLE_SIZE, APPLE_SIZE)
            
            # Проверяем, что яблоко не на змейке
            if not any(apple_rect.colliderect(segment) for segment in self.snake):
                self.apple = apple_rect
                return
            
            tries += 1
        
        # Резервный спавн
        x = random.randint(0, WIN_W - APPLE_SIZE)
        y = random.randint(0, WIN_H - APPLE_SIZE)
        self.apple = pygame.Rect(x, y, APPLE_SIZE, APPLE_SIZE)
    
    def handle_input(self):
        """Обработка ввода для изменения направления"""
        keys = pygame.key.get_pressed()
        
        # Сохраняем текущее направление как следующее для проверки
        new_direction = self.direction
        
        # Меняем направление, но не на противоположное
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.direction != DIR_DOWN:  # Нельзя развернуться на 180°
                new_direction = DIR_UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.direction != DIR_UP:
                new_direction = DIR_DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.direction != DIR_RIGHT:
                new_direction = DIR_LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.direction != DIR_LEFT:
                new_direction = DIR_RIGHT
        
        # Обновляем направление
        self.next_direction = new_direction
    
    def move_snake(self):
        """Движение змейки"""
        # Получаем голову змейки
        head = self.snake[0].copy()
        
        # Обновляем текущее направление
        self.direction = self.next_direction
        
        # Двигаем голову в текущем направлении
        head.x += self.direction[0] * SNAKE_SIZE
        head.y += self.direction[1] * SNAKE_SIZE
        
        # Проверяем столкновение со стенами
        if (head.x < 0 or head.x >= WIN_W or 
            head.y < 0 or head.y >= WIN_H):
            self.game_over = True
            return
        
        # Проверяем столкновение с собой
        for segment in self.snake[:-1]:  # Проверяем все сегменты кроме хвоста
            if head.colliderect(segment):
                self.game_over = True
                return
        
        # Добавляем новую голову в начало списка
        self.snake.insert(0, head)
        
        # Проверяем, съела ли змейка яблоко
        if head.colliderect(self.apple):
            # Увеличиваем счёт
            self.score += 10
            
            # Спавним новое яблоко
            self.spawn_apple()
            
            # Не удаляем хвост (змея растёт)
        else:
            # Удаляем хвост (змея не выросла)
            self.snake.pop()
    
    def check_collisions(self):
        """Проверка всех столкновений (упрощённая версия)"""
        # Проверяем столкновение головы с яблоком
        head = self.snake[0]
        if head.colliderect(self.apple):
            self.score += 10
            self.spawn_apple()
            
            # Добавляем новый сегмент в конец
            last_segment = self.snake[-1]
            new_segment = last_segment.copy()
            self.snake.append(new_segment)
    
    def update(self, dt):
        """Обновление состояния игры"""
        if self.game_over:
            return
        
        # Обновляем таймер движения
        self.move_timer += dt
        
        # Если пришло время двигаться
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.move_snake()
    
    def draw(self):
        """Отрисовка игры"""
        # Фон
        self.screen.fill(BG_COLOR)
        
        # Рисуем сетку (опционально, для удобства)
        self.draw_grid()
        
        # Рисуем яблоко
        pygame.draw.rect(self.screen, APPLE_COLOR, self.apple)
        # Делаем яблоко круглым
        pygame.draw.circle(
            self.screen, 
            APPLE_COLOR, 
            self.apple.center, 
            APPLE_SIZE // 2
        )
        
        # Рисуем змейку
        for i, segment in enumerate(self.snake):
            # Голова другим цветом
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            pygame.draw.rect(self.screen, color, segment)
            
            # Скруглённые углы для лучшего вида
            pygame.draw.rect(self.screen, color, segment, border_radius=4)
        
        # Рисуем HUD (интерфейс)
        self.draw_hud()
        
        # Если игра окончена, показываем сообщение
        if self.game_over:
            self.draw_game_over()
        
        # Обновляем экран
        pygame.display.flip()
    
    def draw_grid(self):
        """Отрисовка сетки (для удобства)"""
        grid_color = (50, 50, 50)
        
        # Вертикальные линии
        for x in range(0, WIN_W, SNAKE_SIZE):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, WIN_H), 1)
        
        # Горизонтальные линии
        for y in range(0, WIN_H, SNAKE_SIZE):
            pygame.draw.line(self.screen, grid_color, (0, y), (WIN_W, y), 1)
    
    def draw_hud(self):
        """Отрисовка интерфейса"""
        # Счёт
        score_text = self.font.render(
            messages.HUD_SCORE.format(self.score), 
            True, 
            TEXT_COLOR
        )
        self.screen.blit(score_text, (10, 10))
        
        # Длина змейки
        length_text = self.font.render(
            messages.HUD_LENGTH.format(len(self.snake)), 
            True, 
            TEXT_COLOR
        )
        self.screen.blit(length_text, (10, 40))
        
        # Инструкция
        info_text = self.font.render(messages.HUD_INFO, True, TEXT_COLOR)
        self.screen.blit(info_text, (10, WIN_H - 30))
    
    def draw_game_over(self):
        """Отрисовка экрана завершения игры"""
        # Полупрозрачное затемнение
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Чёрный с прозрачностью
        self.screen.blit(overlay, (0, 0))
        
        # Текст "Игра окончена"
        game_over_text = self.big_font.render(
            messages.GAME_OVER_TEXT.format(self.score), 
            True, 
            GAME_OVER_COLOR
        )
        text_rect = game_over_text.get_rect(center=(WIN_W//2, WIN_H//2 - 30))
        self.screen.blit(game_over_text, text_rect)
        
        # Текст "Рестарт"
        restart_text = self.font.render(messages.RESTART_TEXT, True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(WIN_W//2, WIN_H//2 + 30))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            # Время с прошлого кадра
            dt = self.clock.tick(FPS) / 1000.0
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Рестарт при нажатии R
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
            
            # Обработка ввода (только если игра не окончена)
            if not self.game_over:
                self.handle_input()
            
            # Обновление игры
            self.update(dt)
            
            # Отрисовка
            self.draw()
        
        # Завершение
        pygame.quit()
        sys.exit()


# Запуск игры
if __name__ == "_main_":
    game = SnakeGame()
    game.run()