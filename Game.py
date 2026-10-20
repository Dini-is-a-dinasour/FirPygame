
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Be Ire Simulator")

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 60, 60)

# Player
player1 = pygame.Rect(275, 340, 50, 40)
player1_speed = 15
# Player 2
player2 = pygame.Rect(400, 340, 50, 40)
player2_speed = 15

# Falling block
blocks = []

for i in range(5):
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


# Game loop setup
clock = pygame.time.Clock()
running = True

game_over1 = False
game_over2 = False

# Game mode selection
game_mode = 0

while running and game_mode == 0:
    screen.fill(BLACK)

    title = pygame.font.Font(None, 60).render(
        "DODGE EM", True, WHITE
    )
    option1 = font.render("Press 1 - Single Player", True, BLUE)
    option2 = font.render("Press 2 - Two Players", True, (0, 255, 0))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))
    screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, 200))
    screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_mode = 1
            elif event.key == pygame.K_2:
                game_mode = 2

    pygame.display.flip()
    clock.tick(60)

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
                player1.x, player1.y = 275, 340
                player2.x, player2.y = 400, 340


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
        if game_mode == 2:
          # Green player - arrow keys
          if keys[pygame.K_LEFT] and player2.left > 0:
            player2.x -= player2_speed
          if player2.colliderect(player1):
            player2.x += player2_speed

          if keys[pygame.K_RIGHT] and player2.right < WIDTH:
           player2.x += player2_speed
          if player2.colliderect(player1):
            player2.x -= player2_speed

          if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= player2_speed
          if player2.colliderect(player1):
            player2.y += player2_speed

          if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
           player2.y += player2_speed
          if player2.colliderect(player1):
            player2.y -= player2_speed

        # Move all four falling blocks
        for block in blocks:
            block.y += block_speed

            # Block reaches the bottom
            if block.top > HEIGHT:
                block.x = random.randint(0, WIDTH - block.width)
                block.y = random.randint(-150, -30)
                score += 1
                block_speed += 0.5

            # Blue collision - both modes
            if player1.colliderect(block):
             game_over1 = True

            # Green collision - two-player mode only
            if game_mode == 2 and player2.colliderect(block):
             game_over2 = True

    # Draw everything
    screen.fill(BLACK)

    pygame.draw.rect(screen, RED, player1)
    if game_mode == 2:
     pygame.draw.rect(screen, (0, 255, 0), player2)
    for block in blocks:
     pygame.draw.rect(screen, BLUE, block)

     score_text = font.render(f"Score: {score}", True, WHITE)
     screen.blit(score_text, (10, 10))

    if game_over1:
         message = font.render("Game Over! BLUE LOST", True, RED)
         screen.blit(message, (180, 160))


    elif game_over2 and game_mode == 2:
       message = font.render("Game Over! GREEN LOST", True, (0, 255, 0))
       screen.blit(message, (180, 160))

    if game_over1 or game_over2:
       restart_text = font.render("Press R to Restart", True, WHITE)
       screen.blit(restart_text, (210, 200))

    pygame.display.flip()

pygame.quit()
