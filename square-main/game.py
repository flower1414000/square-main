import pygame # pyright: ignore[reportMissingImports]
import random
import sys

from config import *
import messages


class Game:
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption(messages.WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.player = pygame.Rect(
            (WIN_W - PLAYER_SIZE) // 2,
            (WIN_H - PLAYER_SIZE) // 2,
            PLAYER_SIZE,
            PLAYER_SIZE
        )

        self.red_rects = []
        self.score = 0
        self.time_since_spawn = 0.0

        self.spawn_red()  # первое яблоко

    # ---------- Спавн красного квадрата ----------
    def spawn_red(self):
        margin = 10
        tries = 0

        while tries < 200:
            x = random.randint(margin, WIN_W - RED_SIZE - margin)
            y = random.randint(margin, WIN_H - RED_SIZE - margin)
            rect = pygame.Rect(x, y, RED_SIZE, RED_SIZE)

            if not rect.colliderect(self.player.inflate(10, 10)):
                # не на игроке и не слишком близко к другим
                if all(not rect.colliderect(r.inflate(8, 8)) for r in self.red_rects):
                    self.red_rects.append(rect)
                    return

            tries += 1

        # резервный спавн
        x = random.randint(0, WIN_W - RED_SIZE)
        y = random.randint(0, WIN_H - RED_SIZE)
        self.red_rects.append(pygame.Rect(x, y, RED_SIZE, RED_SIZE))

    # ---------- Обработка ввода ----------
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        # нормализация диагонали
        if dx and dy:
            inv = (2 ** 0.5) / 2
            dx *= inv
            dy *= inv

        self.player.x += int(dx * PLAYER_SPEED * dt)
        self.player.y += int(dy * PLAYER_SPEED * dt)

        # границы окна
        self.player.clamp_ip(pygame.Rect(0, 0, WIN_W, WIN_H))

    # ---------- Проверка коллизий ----------
    def check_collisions(self):
        collected = [r for r in self.red_rects if self.player.colliderect(r)]
        for r in collected:
            self.red_rects.remove(r)
            self.score += 1

    # ---------- Рендер ----------
    def draw(self):
        self.screen.fill(BG_COLOR)

        # красные квадраты
        for r in self.red_rects:
            pygame.draw.rect(self.screen, RED_COLOR, r)

        # игрок
        pygame.draw.rect(self.screen, PLAYER_COLOR, self.player)

        # HUD
        score_text = self.font.render(messages.HUD_SCORE.format(self.score), True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

        info_text = self.font.render(messages.HUD_INFO, True, INFO_COLOR)
        self.screen.blit(info_text, (10, WIN_H - FONT_SIZE - 10))

        pygame.display.flip()

    # ---------- Основной цикл ----------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.time_since_spawn += dt

            # события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # ввод
            self.handle_input(dt)

            # спавн красных
            if self.time_since_spawn >= SPAWN_INTERVAL and len(self.red_rects) < MAX_REDS:
                self.time_since_spawn = 0.0
                self.spawn_red()

            # коллизии
            self.check_collisions()

            # рендер
            self.draw()

        pygame.quit()
        sys.exit()