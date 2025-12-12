import pygame
import time
import random

# --- Initialization ---
pygame.init()

# Colors (R, G, B)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
# --- NEW: Border Color ---
BORDER_COLOR = (169, 169, 169)  # Dark Gray

# Display settings
DIS_WIDTH = 600
DIS_HEIGHT = 400

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Python Snake Game')

clock = pygame.time.Clock()

# Snake settings
SNAKE_BLOCK = 10
SNAKE_SPEED = 15
# --- NEW: Border Thickness ---
BORDER_WIDTH = 20

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    dis.blit(value, [BORDER_WIDTH, BORDER_WIDTH])  # Moved score slightly inside


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    # Center the message
    text_rect = mesg.get_rect(center=(DIS_WIDTH / 2, DIS_HEIGHT / 2))
    dis.blit(mesg, text_rect)


def gameLoop():
    game_over = False
    game_close = False

    # Starting position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Ensure food spawns INSIDE the borders (between BORDER_WIDTH and WIDTH - BORDER_WIDTH)
    foodx = round(random.randrange(BORDER_WIDTH, DIS_WIDTH - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(BORDER_WIDTH, DIS_HEIGHT - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(BLUE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # --- CHANGED: Boundary Check ---
        # Now checks against BORDER_WIDTH instead of 0
        if x1 >= DIS_WIDTH - BORDER_WIDTH or x1 < BORDER_WIDTH or y1 >= DIS_HEIGHT - BORDER_WIDTH or y1 < BORDER_WIDTH:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(BLACK)

        # --- NEW: Draw the Border ---
        # Arguments: Surface, Color, [x, y, w, h], thickness
        pygame.draw.rect(dis, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], BORDER_WIDTH)

        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # Snake Movement Logic
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self-collision Check
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Eating Food Logic
        if x1 == foodx and y1 == foody:
            # --- CHANGED: Food Respawn Logic ---
            foodx = round(random.randrange(BORDER_WIDTH, DIS_WIDTH - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(BORDER_WIDTH, DIS_HEIGHT - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


# Start the game
gameLoop()