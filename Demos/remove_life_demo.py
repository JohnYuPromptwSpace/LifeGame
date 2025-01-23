import pygame

# Constants
SCREEN_SIZE = 800
GRID_SIZE = 100
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
FPS = 10

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Conway's Game of Life")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT_GREEN = (0, 255, 0, 128)  # Semi-transparent green
TRANSPARENT_RED = (255, 0, 0, 128)  # Semi-transparent red

# Initialize grid as a 1D list
grid = [0] * (GRID_SIZE * GRID_SIZE)

# Toad pattern with relative positions
toad_pattern = [[2, 0], [0, 1], [0, 2], [3, 1], [3, 2], [1, 3]]

# Function to convert 2D index to 1D index
def index(x, y):
    return y * GRID_SIZE + x

# Function to draw the grid
def draw_grid(screen, grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE if grid[index(x, y)] == 1 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to update the grid
def update_grid(grid):
    new_grid = grid.copy()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            # Count alive neighbors
            alive_neighbors = 0
            for ny in range(max(0, y - 1), min(y + 2, GRID_SIZE)):
                for nx in range(max(0, x - 1), min(x + 2, GRID_SIZE)):
                    if (nx != x or ny != y) and grid[index(nx, ny)] == 1:
                        alive_neighbors += 1
            # Apply Conway's rules
            if grid[index(x, y)] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                new_grid[index(x, y)] = 0
            elif grid[index(x, y)] == 0 and alive_neighbors == 3:
                new_grid[index(x, y)] = 1
    return new_grid

# Function to place a pattern on the grid
def place_pattern(grid, pattern, center_x, center_y):
    for rel_x, rel_y in pattern:
        abs_x = center_x + rel_x
        abs_y = center_y + rel_y
        if 0 <= abs_x < GRID_SIZE and 0 <= abs_y < GRID_SIZE:
            grid[index(abs_x, abs_y)] = 1

# Function to remove cells within a rectangle
def remove_cells(grid, start_x, start_y, end_x, end_y):
    for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                grid[index(x, y)] = 0

# Function to draw the pattern overlay
def draw_pattern_overlay(screen, pattern, center_x, center_y, color):
    overlay_surf = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), pygame.SRCALPHA)
    for rel_x, rel_y in pattern:
        abs_x = center_x + rel_x
        abs_y = center_y + rel_y
        if 0 <= abs_x < GRID_SIZE and 0 <= abs_y < GRID_SIZE:
            pygame.draw.rect(overlay_surf, color, (abs_x * CELL_SIZE, abs_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    screen.blit(overlay_surf, (0, 0))

# Function to draw the transparent rectangle
def draw_transparent_rect(screen, start_x, start_y, end_x, end_y, color):
    rect_surf = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
    rect_x = min(start_x, end_x) * CELL_SIZE
    rect_y = min(start_y, end_y) * CELL_SIZE
    rect_w = (abs(start_x - end_x) + 1) * CELL_SIZE
    rect_h = (abs(start_y - end_y) + 1) * CELL_SIZE
    pygame.draw.rect(rect_surf, color, (rect_x, rect_y, rect_w, rect_h))
    screen.blit(rect_surf, (0, 0))

# Main loop
running = True
clock = pygame.time.Clock()
mouse_x, mouse_y = 0, 0
drawing_rect = False
rect_start_x, rect_start_y = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            if event.button == 1:  # Left mouse button
                place_pattern(grid, toad_pattern, grid_x, grid_y)
            elif event.button == 3:  # Right mouse button
                drawing_rect = True
                rect_start_x, rect_start_y = grid_x, grid_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                drawing_rect = False
                rect_end_x = mouse_x // CELL_SIZE
                rect_end_y = mouse_y // CELL_SIZE
                remove_cells(grid, rect_start_x, rect_start_y, rect_end_x, rect_end_y)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
    
    screen.fill(BLACK)
    draw_grid(screen, grid)
    
    # Draw the pattern overlay at the current mouse position
    overlay_x = mouse_x // CELL_SIZE
    overlay_y = mouse_y // CELL_SIZE
    draw_pattern_overlay(screen, toad_pattern, overlay_x, overlay_y, TRANSPARENT_GREEN)
    
    # Draw the transparent rectangle if drawing
    if drawing_rect:
        rect_end_x = mouse_x // CELL_SIZE
        rect_end_y = mouse_y // CELL_SIZE
        draw_transparent_rect(screen, rect_start_x, rect_start_y, rect_end_x, rect_end_y, TRANSPARENT_RED)

    pygame.display.flip()
    
    grid = update_grid(grid)
    clock.tick(FPS)

pygame.quit()
