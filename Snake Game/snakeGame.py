import random
import pygame
import time

#AUTHOR: SANDESH BANSODE

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
background_color = (150, 150, 150)  # Light gray background

# Game window dimensions
display_width = 800
display_height = 600

# Snake block size
block_size = 10

# Frame rate
clock = pygame.time.Clock()

# Game over flag
game_over = False

# Snake initial position and direction
snake_length = 3
snake_list = []
snake_head = [display_width / 2, display_height / 2]
direction = "right"

# Apple position
apple_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
apple_y = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0

# Score
score = 0

# Diff levels
difficulty_levels = {
    1: 5,  # Easy
    2: 15,  # Medium
    3: 10  # Hard
}

# Func to draw the snake, apple, and score
def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(game_display, green, [x, y, block_size, block_size])

def draw_apple(apple_x, apple_y):
    pygame.draw.circle(game_display, red, (apple_x + block_size // 2, apple_y + block_size // 2), block_size // 2)

def draw_score(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, white)
    game_display.blit(text, [10, 10])

def game_over_screen(score):
    font_style = pygame.font.SysFont(None, 50)
    game_over_msg = font_style.render("GAME OVER    ", True, red)
    score_msg = font_style.render("your Score: " + str(score), True, white)
    restart_msg = font_style.render("press R to Restart", True, white)
    quit_msg = font_style.render("press Q to Quit", True, white)

    # Draw a rectangle around the game over screen with a slightly larger size and rounded corners
    pygame.draw.rect(game_display, white, [display_width // 4 - 75, display_height // 4 - 75, display_width // 2 + 150, display_height // 2 + 150], 2, border_radius=10)

    game_display.blit(game_over_msg, [display_width // 2 - 100, display_height // 2 - 125])
    game_display.blit(score_msg, [display_width // 2 - 100, display_height // 2 - 75])
    game_display.blit(restart_msg, [display_width // 2 - 100, display_height // 2])
    game_display.blit(quit_msg, [display_width // 2 - 100, display_height // 2 + 50])

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Initialize pygame
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Difficulty selection screen
def difficulty_selection_screen():
    font = pygame.font.SysFont(None, 30)
    title_text = font.render("Choose Difficulty", True, white)
    easy_text = font.render("1. Easy", True, white)
    medium_text = font.render("2. Medium", True, white)
    hard_text = font.render("3. Hard", True, white)

    game_display.fill(background_color)
    game_display.blit(title_text, (display_width // 2 - 100, display_height // 4))
    game_display.blit(easy_text, (display_width // 2 - 50, display_height // 4 + 50))
    game_display.blit(medium_text, (display_width // 2 - 50, display_height // 4 + 100))
    game_display.blit(hard_text, (display_width // 2 - 50, display_height // 4 + 150))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3

# Game loop
while True:
    # Difficulty selection
    difficulty_choice = difficulty_selection_screen()

    # Set frame rate based on difficulty
    if difficulty_choice in difficulty_levels:
        fps = difficulty_levels[difficulty_choice]
    else:
        print("Invalid difficulty choice. Defaulting to Easy.")
        fps = difficulty_levels[1]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                elif event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"

        # Update snake position
        if direction == "right":
            snake_head[0] += block_size
        elif direction == "left":
            snake_head[0] -= block_size
        elif direction == "up":
            snake_head[1] -= block_size
        elif direction == "down":
            snake_head[1] += block_size

        snake_list.append(list(snake_head))

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake has hit itself or the edges
        if snake_head in snake_list[:-1] or snake_head[0] >= display_width or snake_head[0] < 0 or snake_head[1] >= display_height or snake_head[1] < 0:
            game_over = True

        # Check if snake has eaten an apple
        if snake_head == [apple_x, apple_y]:
            snake_length += 1
            apple_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
            apple_y = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0
            score += 1

        # Draw the game objects
        game_display.fill(background_color)
        draw_snake(snake_list)
        draw_apple(apple_x, apple_y)
        draw_score(score)

        pygame.display.update()
        clock.tick(fps)  
        # Use the chosen frame rate

    # Game over screen
    if not game_over_screen(score):
        pygame.quit()
