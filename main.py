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
DARK_GREEN = (0, 200, 0)
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
WINNING_SCORE = 30  # Apples needed to win

# --- Fonts ---
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 50)

# --- Sound Setup ---
game_over_sound = None
victory_sound = None

try:
    game_over_sound = pygame.mixer.Sound("gameover.wav")
    # If you have a win sound, name it 'win.wav'
    victory_sound = pygame.mixer.Sound("win.wav")
except:
    pass


def your_score(score):
    # Show score / Target
    score_text = f"Score: {score} / {WINNING_SCORE}"
    value = score_font.render(score_text, True, YELLOW)
    dis.blit(value, [BORDER_WIDTH + 5, BORDER_WIDTH])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])


def message_centered(msg, color, y_offset=0, font=font_style):
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH / 2, DIS_HEIGHT / 2 + y_offset))
    dis.blit(mesg, text_rect)


def game_intro():
    intro = True
    while intro:
        dis.fill(BLACK)
        pygame.draw.rect(dis, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], BORDER_WIDTH)

        message_centered("SNAKE GAME", GREEN, -100, menu_font)
        message_centered("Reach Score 30 to Win!", WHITE, -20)
        message_centered("1. Easy", BLUE, 20)
        message_centered("2. Medium", YELLOW, 50)
        message_centered("3. Hard", RED, 80)
        message_centered("Press Q to Quit", BORDER_COLOR, 140)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return None
                if event.key == pygame.K_1:
                    return 10
                if event.key == pygame.K_2:
                    return 15
                if event.key == pygame.K_3:
                    return 25


def gameLoop(speed):
    game_over = False
    game_close = False
    game_won = False  # NEW: Track if player won

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(BORDER_WIDTH, DIS_WIDTH - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(BORDER_WIDTH, DIS_HEIGHT - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        # --- LOSS SCREEN or WIN SCREEN ---
        while game_close == True:
            # Check if it was a Win or a Loss
            if game_won:
                dis.fill(BLACK)  # Or a celebratory color
                title_text = "YOU WON!"
                title_color = GREEN
            else:
                dis.fill(BLACK)
                title_text = "GAME OVER"
                title_color = RED

            pygame.draw.rect(dis, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], BORDER_WIDTH)

            message_centered(title_text, title_color, -50, menu_font)
            message_centered(f"Final Score: {Length_of_snake - 1}", YELLOW, 10)
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
                        gameLoop(speed)
                    if event.key == pygame.K_m:
                        new_speed = game_intro()
                        if new_speed:
                            gameLoop(new_speed)
                        else:
                            game_over = True
                            game_close = False

        # --- GAMEPLAY ---
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

        # Boundary Check
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

        # --- EATING FOOD ---
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(BORDER_WIDTH, DIS_WIDTH - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(BORDER_WIDTH, DIS_HEIGHT - BORDER_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

            # --- NEW: Check for Win ---
            if (Length_of_snake - 1) == WINNING_SCORE:
                if victory_sound: pygame.mixer.Sound.play(victory_sound)
                game_won = True
                game_close = True

        clock.tick(speed)

    pygame.quit()
    quit()


# --- Main Execution ---
chosen_speed = game_intro()
if chosen_speed:
    gameLoop(chosen_speed)