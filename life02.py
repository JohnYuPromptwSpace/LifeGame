"""
v0.0.02
Add loading screen & lab select buttons + interactions
"""

import pygame
import numpy as np
import time

pygame.init()

# Screen dimensions and colors
CELL_SIZE = 5
GRID_SIZE_X = 150
GRID_SIZE_Y = 100
WIDTH = GRID_SIZE_X * CELL_SIZE
HEIGHT = GRID_SIZE_Y * CELL_SIZE

COBALT = (23, 38, 55)
BRIGHTERCOBALT = (25, 41, 59)
BRIGHTCOBALT = (32, 52, 71)

BRIGHTORANGE = (233, 200, 68)
BITBRIGHTORANGE = (192, 153, 69)
ORANGE = (103, 96, 69)
DARKERORANGE = (36, 47, 55)
DARKORANGE = (73, 68, 55)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Text setup using Pygame's built-in functionality
pygame.font.init()
fontP = pygame.font.SysFont('monospace', 18, bold=True)
fontH2 = pygame.font.SysFont('monospace', 28, bold=True)
fontH1 = pygame.font.SysFont('monospace', 36, bold=True)

current_screen = 'main_game'  # Manage screen state

def update_grid():
    global grid
    new_grid = grid.copy()
    for i in range(GRID_SIZE_Y):
        for j in range(GRID_SIZE_X):
            num_neighbors = np.sum(grid[max(i - 1, 0):min(i + 2, GRID_SIZE_Y), max(j - 1, 0):min(j + 2, GRID_SIZE_X)]) - grid[i, j]
            if grid[i, j] == 1 and (num_neighbors < 2 or num_neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and num_neighbors == 3:
                new_grid[i, j] = 1
    grid = new_grid

def draw_life():
    global grid
    for row in range(GRID_SIZE_Y):
        for col in range(GRID_SIZE_X):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, DARKERORANGE, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])
    update_grid()

def reset_life():
    global grid
    grid = np.random.randint(2, size=(GRID_SIZE_Y, GRID_SIZE_X))

def draw_loading_screen(progress):
    screen.fill(COBALT)
    title = fontP.render("Loading...", True, BRIGHTORANGE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 7*3))

    # Draw title
    screen.blit(title, title_rect)

    # Draw progress bar
    progress_bar_length = 500
    progress_bar_height = 5
    progress_rect = pygame.Rect(WIDTH // 2 - progress_bar_length // 2, HEIGHT // 2, progress_bar_length * progress, progress_bar_height)
    pygame.draw.rect(screen, BRIGHTORANGE, progress_rect)

    pygame.display.update()

def load_screen():
    for i in range(30):
        draw_loading_screen(i / 100)
        time.sleep(0.04)

    time.sleep(1)

    for i in range(30, 85, 3):
        draw_loading_screen(i / 100)
        time.sleep(0.04)

    time.sleep(1)

    draw_loading_screen(0.9)
    time.sleep(1)

    draw_loading_screen(1)
    time.sleep(1)

def level_select():
    global current_screen
    running = True
    button_width = WIDTH // 8
    button_height = WIDTH // 8
    margin = 20
    border_radius = 15  # Radius of the rounded corners
    border_size = 4  # Size of the button border

    # Colors
    edge_normal_color = DARKORANGE
    button_normal_color = COBALT
    text_normal_color = DARKORANGE
    
    edge_hover_color = ORANGE
    button_hover_color = BRIGHTCOBALT
    text_hover_color = ORANGE
    
    edge_click_color = BITBRIGHTORANGE
    button_click_color = BRIGHTERCOBALT    
    text_click_color = BITBRIGHTORANGE    

    # Define level buttons (positions)
    buttons = []
    for j in range(2):  # 2 rows
        for i in range(4):  # 4 buttons per row
            x = margin * (i + 1) + button_width * i + (WIDTH - (margin * 5 + button_width * 4)) // 2
            y = HEIGHT // 2 + margin * j + button_height * j - (HEIGHT - (margin * 5 + button_height * 4)) * 2
            buttons.append(pygame.Rect(x, y, button_width, button_height))

    # Track the clicked state
    clicked = [False] * len(buttons)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(COBALT)
        
        draw_life()
        
        level_title = fontH2.render("Select Life", True, BRIGHTORANGE)
        level_rect = level_title.get_rect(center=(WIDTH // 2, HEIGHT // 13*3))
        screen.blit(level_title, level_rect)

        # Draw buttons with rounded corners and borders
        for index, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                if clicked[index]:
                    color = button_click_color
                    text_color = text_click_color
                    edge_color = edge_click_color
                else:
                    color = button_hover_color
                    text_color = text_hover_color
                    edge_color = edge_hover_color
            else:
                color = button_normal_color
                text_color = text_normal_color
                edge_color = edge_normal_color
            
            outer_rect = pygame.Rect(button.x - border_size, button.y - border_size, button.width + 2 * border_size, button.height + 2 * border_size)
            pygame.draw.rect(screen, edge_color, outer_rect, border_radius=border_radius)  # Draw the outer rectangle for the border

            pygame.draw.rect(screen, color, button, border_radius=border_radius)  # Draw the inner rectangle

            # Render level number in the center of each button
            level_number_text = fontH2.render(str(index + 1), True, text_color)
            text_rect = level_number_text.get_rect(center=(button.centerx, button.centery))
            screen.blit(level_number_text, text_rect)

        # Handling events in the level select screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for index, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        clicked[index] = True  # Mark the button as clicked
                        print(f"Level {index + 1} selected")  # Debug: Replace with actual level loading
            elif event.type == pygame.MOUSEBUTTONUP:
                for index in range(len(clicked)):
                    clicked[index] = False  # Reset click state when mouse button is released
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to go back
                    current_screen = 'main_game'
                    running = False
                if event.key == pygame.K_r:
                    reset_life()

        pygame.display.update()
        time.sleep(0.01)

def game_loop():
    global current_screen
    while True:
        if current_screen == 'main_game':
            main_game()
        elif current_screen == 'level_select':
            level_select()

def main_game():
    global current_screen
    load_screen()
    reset_life()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_screen = 'level_select'
                    running = False
                if event.key == pygame.K_r:
                    reset_life()

        screen.fill(COBALT)
        
        draw_life()

        title = fontH1.render("Follow the Life", True, BRIGHTORANGE)
        prompt = fontP.render("> Press Space to Follow <", True, BRIGHTORANGE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6*2.5))
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.5))

        screen.blit(title, title_rect)
        screen.blit(prompt, prompt_rect)

        pygame.display.update()
        time.sleep(0.01)

game_loop()