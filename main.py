import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init()   # Initialize sound mixer


# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if game is over, allow restart options
            if event.type == pygame.KEYDOWN and engine.game_over:
                if event.key == pygame.K_3:
                    engine.restart(best_of=3)
                elif event.key == pygame.K_5:
                    engine.restart(best_of=5)
                elif event.key == pygame.K_7:
                    engine.restart(best_of=7)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # only handle normal input when not game_over
        if not engine.game_over:
            engine.handle_input()
            engine.update()

        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
