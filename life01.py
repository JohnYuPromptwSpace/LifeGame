"""
v0.0.01
Life Game main screen
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
ORANGE = (233, 200, 68)
DARKORANGE = (36, 47, 55)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Text setup using Pygame's built-in functionality
pygame.font.init()
# Search for a 'monospace' font which often looks more pixelated
fontP = pygame.font.SysFont('monospace', 18, bold=True)
fontH1 = pygame.font.SysFont('monospace', 36, bold=True)

def update_grid(grid):
    new_grid = grid.copy()
    for i in range(GRID_SIZE_Y):
        for j in range(GRID_SIZE_X):
            num_neighbors = np.sum(grid[max(i - 1, 0):min(i + 2, GRID_SIZE_Y), max(j - 1, 0):min(j + 2, GRID_SIZE_X)]) - grid[i, j]
            if grid[i, j] == 1 and (num_neighbors < 2 or num_neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and num_neighbors == 3:
                new_grid[i, j] = 1
    return new_grid

def draw_loading_screen(progress):
    screen.fill(COBALT)
    title = fontP.render("Follow the Life", True, ORANGE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 7*3))

    # Draw title
    screen.blit(title, title_rect)

    # Draw progress bar
    progress_bar_length = 500
    progress_bar_height = 5
    progress_rect = pygame.Rect(WIDTH // 2 - progress_bar_length // 2, HEIGHT // 2, progress_bar_length * progress, progress_bar_height)
    pygame.draw.rect(screen, ORANGE, progress_rect)

    pygame.display.update()

def main_game():
    grid = np.random.randint(2, size=(GRID_SIZE_Y, GRID_SIZE_X))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COBALT)

        for row in range(GRID_SIZE_Y):
            for col in range(GRID_SIZE_X):
                if grid[row][col] == 1:
                    pygame.draw.rect(screen, DARKORANGE, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])

        grid = update_grid(grid)

        title = fontH1.render("Follow the Life", True, ORANGE)
        prompt = fontP.render("> Press Space to Follow <", True, ORANGE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6*2.5))
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.5))

        screen.blit(title, title_rect)
        screen.blit(prompt, prompt_rect)

        pygame.display.update()
        time.sleep(0.01)

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
    time.sleep(2)

# load_screen()
main_game()
pygame.quit()