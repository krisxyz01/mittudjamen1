import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game variables
bird_width = 40
bird_height = 30
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_jump = -7
bird_gravity = 1

pipe_width = 50
pipe_gap = 150
pipe_speed = 3
pipes = []

score = 0
font = pygame.font.Font(None, 36)

# Load images
bird_img = pygame.Surface((bird_width, bird_height))
bird_img.fill(RED)
pipe_img = pygame.Surface((pipe_width, SCREEN_HEIGHT))
pipe_img.fill(GREEN)

# Load bird sprite image
bird_sprite = pygame.image.load("bird_sprite.png").convert_alpha()

# Resize bird sprite if needed
bird_sprite = pygame.transform.scale(bird_sprite, (bird_width, bird_height))

def draw_bird(x, y):
    screen.blit(bird_sprite, (x, y))


def draw_pipe(x, y, top=True):
    if top:
        screen.blit(pipe_img, (x, y - SCREEN_HEIGHT))
    else:
        screen.blit(pipe_img, (x, y + pipe_gap))


def collision(pipe):
    if bird_x + bird_width > pipe['x'] and bird_x < pipe['x'] + pipe_width:
        if bird_y < pipe['y'] or bird_y + bird_height > pipe['y'] + pipe_gap:
            return True
    return False


def restart_game():
    global bird_y, bird_gravity, score, pipes
    bird_y = SCREEN_HEIGHT // 2
    bird_gravity = 1
    score = 0
    pipes.clear()


def main():
    global bird_y, bird_gravity, score, pipes

    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        screen.fill(BLUE)

        if not game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_gravity = bird_jump

            # Move bird
            bird_y += bird_gravity
            bird_gravity += 0.5

            # Generate pipes
            if len(pipes) == 0 or pipes[-1]['x'] < SCREEN_WIDTH - 200:
                pipe_x = SCREEN_WIDTH
                pipe_y = random.randint(50, SCREEN_HEIGHT - pipe_gap - 50)
                pipes.append({'x': pipe_x, 'y': pipe_y})

            # Move pipes
            for pipe in pipes:
                pipe['x'] -= pipe_speed
                draw_pipe(pipe['x'], pipe['y'])
                draw_pipe(pipe['x'], pipe['y'], top=False)

                if collision(pipe):
                    game_over = True

                if pipe['x'] + pipe_width < bird_x:
                    score += 1

            # Remove pipes that are off screen
            pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

            # Draw bird
            draw_bird(bird_x, bird_y)

            # Display score
            score_text = font.render("Score: " + str(score), True, BLACK)
            screen.blit(score_text, (10, 10))

        else:
            # Game over screen
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            restart_text = font.render("Press R to restart", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()
                        game_over = False

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
