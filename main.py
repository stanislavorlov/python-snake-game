import pygame
import time
import random
import os

pygame.init()
pygame.mixer.init()

# --- Colors ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
BORDER_COLOR = (169, 169, 169)

# --- Display ---
DIS_WIDTH = 600
DIS_HEIGHT = 400
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Python Snake Game')

clock = pygame.time.Clock()

# --- Settings ---
SNAKE_BLOCK = 10
BORDER_WIDTH = 20

# --- Fonts ---
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 50)  # Bigger font for title

# --- Sound Setup ---
game_over_sound = None
try:
    game_over_sound = pygame.mixer.Sound("gameover.wav")
except:
    pass  # Sound file missing, silent mode


def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    dis.blit(value, [BORDER_WIDTH + 5, BORDER_WIDTH])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])


# Helper to center text at specific Y-coordinate
def message_centered(msg, color, y_offset=0, font=font_style):
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH / 2, DIS_HEIGHT / 2 + y_offset))
    dis.blit(mesg, text_rect)


def game_intro():
    intro = True
    selected_speed = 15  # Default

    while intro:
        dis.fill(BLACK)
        # Draw Border for style
        pygame.draw.rect(dis, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], BORDER_WIDTH)

        # Menu Text
        message_centered("SNAKE GAME", GREEN, -100, menu_font)
        message_centered("Select Difficulty:", WHITE, -20)
        message_centered("1. Easy", BLUE, 20)
        message_centered("2. Medium", YELLOW, 50)
        message_centered("3. Hard", RED, 80)
        message_centered("Press Q to Quit", BORDER_COLOR, 140)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                return None  # Signal to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    intro = False
                    return None
                if event.key == pygame.K_1:
                    return 10  # Slow
                if event.key == pygame.K_2:
                    return 15  # Normal
                if event.key == pygame.K_3:
                    return 25  # Fast


def gameLoop(speed):
    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(BORDER_WIDTH, DIS_WIDTH - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(BORDER_WIDTH, DIS_HEIGHT - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(BLACK)
            pygame.draw.rect(dis, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], BORDER_WIDTH)

            message_centered("YOU LOST!", RED, -50, menu_font)
            message_centered(f"Score: {Length_of_snake - 1}", YELLOW, 10)
            message_centered("Press C to Play Again", WHITE, 60)
            message_centered("Press M for Menu", BLUE, 90)
            message_centered("Press Q to Quit", BORDER_COLOR, 120)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        # Restart with SAME speed
                        gameLoop(speed)
                    if event.key == pygame.K_m:
                        # Return to Menu
                        new_speed = game_intro()
                        if new_speed:
                            gameLoop(new_speed)
                        else:
                            game_over = True
                            game_close = False

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

        # Border Collision Check
        if x1 >= DIS_WIDTH - BORDER_WIDTH or x1 < BORDER_WIDTH or y1 >= DIS_HEIGHT - BORDER_WIDTH or y1 < BORDER_WIDTH:
            if game_over_sound: pygame.mixer.Sound.play(game_over_sound)
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(BLACK)
        pygame.draw.rect(dis, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], BORDER_WIDTH)
        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                if game_over_sound: pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        our_snake(SNAKE_BLOCK, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(BORDER_WIDTH, DIS_WIDTH - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(BORDER_WIDTH, DIS_HEIGHT - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(speed)

    pygame.quit()
    quit()


# --- Main Execution ---
chosen_speed = game_intro()
if chosen_speed:
    gameLoop(chosen_speed)