import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
GRID_SIZE = 7
CELL_SIZE = 40
GRID_ORIGIN = (100, 60)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Nonogram')

puzzle = [
    [1, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 1, 0, 0, 1, 1, 0],
    [1, 0, 1, 1, 0, 1, 0],
]

player_solution = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(GRID_ORIGIN[0] + x * CELL_SIZE, GRID_ORIGIN[1] + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if player_solution[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif player_solution[y][x] == -1:
                pygame.draw.line(screen, BLUE, (rect.left, rect.top), (rect.right, rect.bottom), 3)
                pygame.draw.line(screen, BLUE, (rect.right, rect.top), (rect.left, rect.bottom), 3)

def toggle_cell(pos):
    x, y = pos
    x = (x - GRID_ORIGIN[0]) // CELL_SIZE
    y = (y - GRID_ORIGIN[1]) // CELL_SIZE
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        player_solution[y][x] = (player_solution[y][x] + 2) % 3 - 1

def check_solution():
    return all(player_solution[y][x] == puzzle[y][x] for y in range(GRID_SIZE) for x in range(GRID_SIZE))

def generate_clues():
    row_clues = []
    col_clues = [[] for _ in range(GRID_SIZE)]

    for y in range(GRID_SIZE):
        current_count = 0
        row_clue = []
        for x in range(GRID_SIZE):
            print(x,y)
            if puzzle[y][x] == 1:
                current_count += 1
            elif current_count > 0:
                row_clue.append(current_count)
                current_count = 0
            col_clues[x].append(puzzle[y][x])

        if current_count > 0:
            row_clue.append(current_count)
        row_clues.append(row_clue)

    for x, col in enumerate(col_clues):
        count = 0
        final_clue = []
        for val in col:
            if val == 1:
                count += 1
            elif count > 0:
                final_clue.append(count)
                count = 0
        if count > 0:
            final_clue.append(count)
        col_clues[x] = final_clue

    return row_clues, col_clues

row_clues, col_clues = generate_clues()

def draw_clues():
    clue_font = pygame.font.SysFont(None, 24)
    for i, rc in enumerate(row_clues):
        text = ' '.join(map(str, rc))
        text_render = clue_font.render(text, True, BLACK)
        screen.blit(text_render, (5, GRID_ORIGIN[1] + i * CELL_SIZE + 5))

    for i, cc in enumerate(col_clues):
        for j, number in enumerate(cc):
            text_render = clue_font.render(str(number), True, BLACK)
            screen.blit(text_render, (GRID_ORIGIN[0] + i * CELL_SIZE + 5, 5 + j * 20))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                toggle_cell(event.pos)
                if check_solution():
                    print("Puzzle Solved!")

    screen.fill(WHITE)
    draw_grid()
    draw_clues()
    pygame.display.flip()

pygame.quit()
sys.exit()