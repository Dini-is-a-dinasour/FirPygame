
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dodge em water")

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 60, 60)

# Player
player1 = pygame.Rect(140, 340, 50, 200)
player1_speed = 13
# Player 2
player2 = pygame.Rect(700, 340, 50, 40)
player2_speed = 16

# Falling block
blocks = []

for i in range(4):
    block = pygame.Rect(
        random.randint(0, WIDTH - 30),
        -i * 100,
        30,
        30
    )
    blocks.append(block)

block_speed = 4
# Score
score = 0
font = pygame.font.Font(None, 30)

# Game loop
clock = pygame.time.Clock()
running = True
game_over1 = False
game_over2 = False


while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Restart when R is pressed after either player loses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over1 or game_over2):
                # Reset player positions
                player1.x, player1.y = 175, 340
                player2.x, player2.y = 700, 340


                # Reset all four blocks
                for i, block in enumerate(blocks):
                 block.x = random.randint(0, WIDTH - block.width)
                 block.y = -i * 100

                 block_speed = 4

                # Reset score and game-over states
                score = 0
                game_over1 = False
                game_over2 = False

    # Game logic only runs while both players are alive
    if not game_over1 and not game_over2:
        keys = pygame.key.get_pressed()


        # RED player - WASD
        if keys[pygame.K_a] and player1.left > 0:
            player1.x -= player1_speed
            if player1.colliderect(player2):
                player1.x += player1_speed

        if keys[pygame.K_d] and player1.right < WIDTH:
            player1.x += player1_speed
            if player1.colliderect(player2):
                player1.x -= player1_speed

        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= player1_speed
            if player1.colliderect(player2):
                player1.y += player1_speed

        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += player1_speed
            if player1.colliderect(player2):
                player1.y -= player1_speed

        # Green player - arrow keys

        if keys[pygame.K_LEFT] and player2.left > 0:
            player2.x -= player2_speed
            if player2.colliderect(player1) and player2.right < WIDTH:
                player2.x += player2_speed
                if  player2.right < WIDTH:
                 player2.x += player2_speed
                if  player2.right < WIDTH:
                 player2.x += player2_speed

        if keys[pygame.K_RIGHT] and player2.right < WIDTH:
            player2.x += player2_speed
            if player2.colliderect(player1) and player2.left > 0:
                player2.x -= player2_speed
                if player2.left > 0:
                 player2.x -= player2_speed
                if player2.left > 0:
                 player2.x -= player2_speed

        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= player2_speed
            if player2.colliderect(player1) and player2.bottom < HEIGHT:
                player2.y += player2_speed
                if player2.bottom < HEIGHT:
                 player2.y += player2_speed
                if player2.bottom < HEIGHT:
                 player2.y += player2_speed

        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += player2_speed
            if player2.colliderect(player1) and player2.top > 0:
                player2.y -= player2_speed
                if player2.top > 0:
                 player2.y -= player2_speed
                if player2.top > 0:
                 player2.y -= player2_speed


        # Move all four falling blocks
        for block in blocks:
            block.y += block_speed

            # Block reaches the bottom
            if block.top > HEIGHT:
                block.x = random.randint(0, WIDTH - block.width)
                block.y = random.randint(-150, -30)
                score += 1
                block_speed += 0.2

            # Check collision with Blue

            # Check collision with Green
            if player2.colliderect(block):
                game_over2 = True

    # Draw everything
    screen.fill(BLACK)

    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, (0, 255, 0), player2)
    for block in blocks:
     pygame.draw.rect(screen, BLUE, block)

     score_text = font.render(f"Score: {score}", True, WHITE)
     screen.blit(score_text, (10, 10))

    if game_over1:
        message = font.render("Game Over! RED LOST", True, RED)
        screen.blit(message, (490, 300))

    elif game_over2:
        message = font.render("Game Over! GREEN LOST", True, (0, 255, 0))
        screen.blit(message, (490, 300))

    if game_over1 or game_over2:
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (490, 330))

    pygame.display.flip()

pygame.quit()
