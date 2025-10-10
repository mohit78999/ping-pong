import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.max_speed = 12
        # optional: last_hit used by engine to play sounds
        self.last_hit = None

    def move(self, player=None, ai=None):
        """Move using predictive checks to avoid tunneling.
           Returns a string indicating what was hit: 'player', 'ai', 'wall', or None.
        """
        hit = None

        # --- Horizontal move with predictive rect ---
        next_x = self.x + self.velocity_x
        future_rect = pygame.Rect(int(next_x), int(self.y), self.width, self.height)

        # left paddle collision (player)
        if player and self.velocity_x < 0 and future_rect.colliderect(player.rect()):
            # place ball just right of player paddle
            self.x = player.x + player.width
            self.velocity_x = -self.velocity_x * 1.05  # reverse + slight speed up
            # tweak vertical velocity based on where the ball hit the paddle
            offset = (self.y + self.height/2) - (player.y + player.height/2)
            self.velocity_y += offset * 0.03
            hit = 'player'
        # right paddle collision (ai)
        elif ai and self.velocity_x > 0 and future_rect.colliderect(ai.rect()):
            # place ball just left of ai paddle
            self.x = ai.x - self.width
            self.velocity_x = -self.velocity_x * 1.05
            offset = (self.y + self.height/2) - (ai.y + ai.height/2)
            self.velocity_y += offset * 0.03
            hit = 'ai'
        else:
            self.x = next_x

        # --- Vertical move and wall bounce ---
        next_y = self.y + self.velocity_y
        if next_y <= 0:
            self.y = 0
            self.velocity_y *= -1
            hit = 'wall'
        elif next_y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            hit = 'wall'
        else:
            self.y = next_y

        # clamp speeds to reasonable range
        if abs(self.velocity_x) > self.max_speed:
            self.velocity_x = self.max_speed * (1 if self.velocity_x > 0 else -1)
        if abs(self.velocity_y) > self.max_speed:
            self.velocity_y = self.max_speed * (1 if self.velocity_y > 0 else -1)

        self.last_hit = hit
        return hit

    def reset(self, direction=None):
        self.x = float(self.original_x)
        self.y = float(self.original_y)
        # randomize direction on reset, or keep given direction
        self.velocity_x = random.choice([-5, 5]) if direction is None else (abs(self.velocity_x) if direction == "right" else -abs(self.velocity_x))
        self.velocity_y = random.choice([-3, 3])
        self.last_hit = None

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
