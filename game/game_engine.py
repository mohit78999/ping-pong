import os
import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5   # default best-of target
        self.game_over = False
        self.winner = None
        self.font = pygame.font.SysFont("Arial", 30)

        try:
            base_path = os.path.dirname(os.path.dirname(__file__))  # go up from 'game/' to 'ping-pong/'
            self.snd_paddle = pygame.mixer.Sound(os.path.join(base_path, "paddle.wav"))
            self.snd_wall = pygame.mixer.Sound(os.path.join(base_path, "wall.wav"))
            self.snd_score = pygame.mixer.Sound(os.path.join(base_path, "score.wav"))

        except Exception as e:
            print("Sound loading error:", e)
            self.snd_paddle = self.snd_wall = self.snd_score = None


    def handle_input(self):
        # in GameEngine.handle_input()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.height)


    def update(self):
        if self.game_over:
            return

    # pass paddles so ball can detect collisions predictively
        hit = self.ball.move(self.player, self.ai)
        if hit == 'player' or hit == 'ai':
            if self.snd_paddle:
                self.snd_paddle.play()
        elif hit == 'wall':
            if self.snd_wall:
                self.snd_wall.play()


    # scoring: check rect edges rather than raw x
           # --- Check scoring ---
        if self.ball.rect().right < 0:  # AI scores
            self.ai_score += 1
            if self.snd_score:          # <-- Play score sound here
                self.snd_score.play()
            if self.ai_score >= self.winning_score:
                self.game_over = True
                self.winner = "AI"
            self.ball.reset()
        
        elif self.ball.rect().left > self.width:  # Player scores
            self.player_score += 1
            if self.snd_score:                    # <-- Play score sound here
                self.snd_score.play()
            if self.player_score >= self.winning_score:
                self.game_over = True
                self.winner = "Player"
            self.ball.reset()

    # give AI control the ball to follow
        self.ai.auto_track(self.ball, self.height)


    def render(self, screen):
    # Clear the screen (optional if handled elsewhere)
        screen.fill(BLACK)

    # --- Draw paddles and ball ---
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

    # --- Draw scores ---
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    # --- Game Over Overlay ---
        if self.game_over:
        # Winner message
            large = pygame.font.SysFont("Arial", 60)
            msg = f"{self.winner} Wins!"
            surf = large.render(msg, True, WHITE)
            rect = surf.get_rect(center=(self.width // 2, self.height // 2 - 30))
            screen.blit(surf, rect)

        # Replay / Quit instructions
            small = pygame.font.SysFont("Arial", 24)
            option = "Press 3/5/7 to Replay (best of), or ESC to Quit"
            surf2 = small.render(option, True, WHITE)
            rect2 = surf2.get_rect(center=(self.width // 2, self.height // 2 + 20))
            screen.blit(surf2, rect2)

    # --- Update the display ---
        pygame.display.flip()


    def restart(self, best_of=5):
        self.winning_score = best_of
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()

