"""
v0.0.05
Finished Lab
"""

import pygame
import numpy as np
import time
import sys

pygame.init()

pygame.display.set_caption("Follw the Life")
FPS = 60
FPS_clock = pygame.time.Clock()

# def background life const
CELL_SIZE = 5
GRID_SIZE_X = 150
GRID_SIZE_Y = 100
WIDTH = GRID_SIZE_X * CELL_SIZE
HEIGHT = GRID_SIZE_Y * CELL_SIZE

# def screen. based on background life grid
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# def colors
BRIGHTERCOBALT = (25, 41, 59)
BRIGHTCOBALT = (32, 52, 71)
BITBRIGHTCOBALT = (30, 48, 67)
COBALT = (23, 38, 55)

BRIGHTORANGE = (233, 200, 68)
BITBRIGHTORANGE = (192, 153, 69)
ORANGE = (117, 109, 79)
BITDARKORANGE = (86, 76, 55)
DARKORANGE = (73, 68, 55)
DARKERORANGE = (36, 47, 55)

# def fonts
pygame.font.init()

fontS1 = pygame.font.SysFont('monospace', 14, bold=True)
fontS2 = pygame.font.SysFont('monospace', 11, bold=True)
fontP = pygame.font.SysFont('monospace', 18, bold=True)
fontH2 = pygame.font.SysFont('monospace', 28, bold=True)
fontH1 = pygame.font.SysFont('monospace', 36, bold=True)

selected_lab = 1  # Tracks the selected lab(puzzle)
current_screen = 'main_title'  # Manage screen state

# def background life grid
grid = np.random.randint(2, size=(GRID_SIZE_Y, GRID_SIZE_X))

# def lab const
LAB_NAME = ["Toad", "Beacon", "Glider", "Pulsar", "48P22.1", "Achim's p11", "Flicker", "Gosper Glider Gun"]
LAB_FONTS = [0,0,0,0,1,1,1,1]
LAB_DELAY = [5,5,5,3,1,1,1,1]

LAB_SIZE = [3,3,3,6,6,8,10,7]
LAB_ADJ = [5/9,5/9,5/9,9/11,6/7,6/7,6/7,6/7]

# load puzzle answer
def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        row = [int(char) for char in line.strip()]
        result.append(row)

    return result

PUZZLE = []

for PUZZLE_MAP in LAB_NAME:
    PUZZLE.append(load_data(f"data/puzzles/{PUZZLE_MAP}.txt"))

player_solution = []

for PUZZLE_MAP in LAB_NAME:
    player_solution.append(load_data(f"data/player_data/{PUZZLE_MAP}.txt"))

player_state = load_data("data/player_data/player_state.txt")
# 0 : lab clear state
# 1 : lab unlock state

# quit game
def quit_game():
    # save player state
    with open("data/player_data/player_state.txt", 'w') as file:
        for data in player_state:
            file.write("".join(map(str,data)) + "\n")
    
    for i, PUZZLE_MAP in enumerate(LAB_NAME):
        with open(f"data/player_data/{PUZZLE_MAP}.txt", 'w') as file:
            for data in player_solution[i]:
                file.write("".join(map(str,data)) + "\n")

    pygame.quit()
    sys.exit()

# render loading screen
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

# animate loading screen
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

# update background life grid
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

# render background life
def draw_life():
    global grid
    for row in range(GRID_SIZE_Y):
        for col in range(GRID_SIZE_X):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, DARKERORANGE, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])
    update_grid()

# reset background life grid
def reset_life():
    global grid
    grid = np.random.randint(2, size=(GRID_SIZE_Y, GRID_SIZE_X))

# laboratory main code
def main_lab():
    global grid, current_screen
    
    # def lab const
    GRID_SIZE = len(PUZZLE[selected_lab-1])
    NO_CELL_SIZE = HEIGHT // (GRID_SIZE+LAB_SIZE[selected_lab-1])
    GRID_ORIGIN = [(WIDTH - NO_CELL_SIZE * GRID_SIZE)/2, (HEIGHT - NO_CELL_SIZE * GRID_SIZE) * LAB_ADJ[selected_lab-1]]
    
    # cal X and black to 0, colored to 1(puzzle grid)
    def cal(a):
        if a == 2 or a == 0:
            return 0
        return 1
    
    # check if user's answer is correct
    def check_solution():
        return all(cal(player_solution[selected_lab-1][y][x]) == PUZZLE[selected_lab-1][y][x] for y in range(GRID_SIZE) for x in range(GRID_SIZE))
    
    # render lab puzzle grid
    def draw_grid():
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(GRID_ORIGIN[0] + x * NO_CELL_SIZE, GRID_ORIGIN[1] + y * NO_CELL_SIZE, NO_CELL_SIZE, NO_CELL_SIZE)
                pygame.draw.rect(screen, BRIGHTORANGE, rect, 1)
                if player_solution[selected_lab-1][y][x] == 1:
                    pygame.draw.rect(screen, BRIGHTORANGE, rect)
                elif player_solution[selected_lab-1][y][x] == 2:
                    pygame.draw.line(screen, BRIGHTORANGE, (rect.left, rect.top), (rect.right, rect.bottom), 3)
                    pygame.draw.line(screen, BRIGHTORANGE, (rect.right, rect.top), (rect.left, rect.bottom), 3)
    
    # toggle cell when clicked. based on mouse pos
    def toggle_cell(pos, mouse_state):
        x, y = pos
        x = int((x - GRID_ORIGIN[0]) // NO_CELL_SIZE)
        y = int((y - GRID_ORIGIN[1]) // NO_CELL_SIZE)
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            if mouse_state == 1:
                if player_solution[selected_lab-1][y][x] == 1:
                    player_solution[selected_lab-1][y][x] = 0
                else:
                    player_solution[selected_lab-1][y][x] = 1
            elif mouse_state == 3:
                if player_solution[selected_lab-1][y][x] == 2:
                    player_solution[selected_lab-1][y][x] = 0
                else:
                    player_solution[selected_lab-1][y][x] = 2
    
    # gen clues for given puzzle
    def generate_clues():
        row_clues = []
        col_clues = [[] for _ in range(GRID_SIZE)]

        for y in range(GRID_SIZE):
            current_count = 0
            row_clue = []
            for x in range(GRID_SIZE):
                if PUZZLE[selected_lab-1][y][x] == 1:
                    current_count += 1
                elif current_count > 0:
                    row_clue.append(current_count)
                    current_count = 0
                col_clues[x].append(PUZZLE[selected_lab-1][y][x])

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

    # def cluesfor row, column
    row_clues, col_clues = generate_clues()

    # render clues. based on puzzle puzzle cell size(NO_CELL_SIZE), fons size(LAB_FONTS). adjustment based on GRID_ORIGIN
    def draw_clues():
        if LAB_FONTS[selected_lab-1] == 0:
            clue_font = fontS1
        else:
            clue_font = fontS2
        for i, rc in enumerate(row_clues):
            text = ' '.join(map(str, rc))
            W,_ = clue_font.size(text)
            text_render = clue_font.render(text, True, BRIGHTORANGE)
            screen.blit(text_render, (GRID_ORIGIN[0] - W - 5, GRID_ORIGIN[1] + i * NO_CELL_SIZE + NO_CELL_SIZE / 2 - _/2))

        _, H = clue_font.size(str(1))
        
        for i, cc in enumerate(col_clues):
            for j, number in enumerate(cc):
                text_render = clue_font.render(str(number), True, BRIGHTORANGE)
                screen.blit(text_render, (GRID_ORIGIN[0] + i * NO_CELL_SIZE + NO_CELL_SIZE / 2 - _/2, GRID_ORIGIN[1] - H * len(cc) - 5 + j * H))
    
    # def update puzzle grid. based on conway. only activated when puzzle is cleared
    def update_nono(solution):
        new_grid = solution.copy()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                nono_neighbors = np.sum(solution[max(i - 1, 0):min(i + 2, GRID_SIZE), max(j - 1, 0):min(j + 2, GRID_SIZE)]) - solution[i, j]
                if solution[i, j] == 1 and (nono_neighbors < 2 or nono_neighbors > 3):
                    new_grid[i, j] = 0
                elif solution[i, j] == 0 and nono_neighbors == 3:
                    new_grid[i, j] = 1
        return new_grid
    
    # main loop states
    running = True
    cnt = 0
    
    # user answer
    # solution = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    # solution = PUZZLE[selected_lab-1].copy()
    
    # main loop
    i = 0
    while running:
        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = 'lab_select'
                    running = False
                if event.key == pygame.K_r:
                    reset_life()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not player_state[0][selected_lab-1]:
                    if event.button == 1:
                        toggle_cell(event.pos, 1)
                        if check_solution():
                            player_state[0][selected_lab-1] = True
                    elif event.button == 3:
                        toggle_cell(event.pos, 3)
                        if check_solution():
                            player_state[0][selected_lab-1] = True

        screen.fill(COBALT)
        
        draw_life()
        
        title = fontH1.render(f"{LAB_NAME[selected_lab-1]}", True, BRIGHTORANGE)
        screen.blit(title, (20,10))

        draw_grid()
        draw_clues()
        
        # only activate when cleared
        if player_state[0][selected_lab-1]:
            if cnt == 0:
                player_state[0][selected_lab-1] = 1
                try:
                    player_state[1][selected_lab] = 1
                except:
                    pass
                player_solution[selected_lab-1] = np.array(PUZZLE[selected_lab-1])
                cnt = 1
            
            W,H = fontH2.size("Clear")
            title = fontH2.render("Clear", True, BRIGHTORANGE)
            screen.blit(title, (WIDTH - W - 10, HEIGHT - H - 10))
            
            i += 1
            if i == LAB_DELAY[selected_lab-1]:
                player_solution[selected_lab-1] = update_nono(player_solution[selected_lab-1])
                i = 0
            
        pygame.display.update()
        FPS_clock.tick(FPS)

# lab select page main code
def lab_select():
    global current_screen, selected_lab
    running = True
    button_width = WIDTH // 8
    button_height = WIDTH // 8
    margin = 20
    border_radius = 15
    border_size = 4

    edge_normal_color = DARKORANGE
    button_normal_color = COBALT
    text_normal_color = DARKORANGE
    
    edge_clear_color = BITDARKORANGE
    button_clear_color = BITBRIGHTCOBALT
    text_clear_color = BITDARKORANGE
    
    edge_hover_color = ORANGE
    button_hover_color = BRIGHTCOBALT
    text_hover_color = ORANGE
    
    edge_click_color = BITBRIGHTORANGE
    button_click_color = BRIGHTERCOBALT    
    text_click_color = BITBRIGHTORANGE
    
    # def lab buttons(positions)
    buttons = []
    for j in range(2):  # 2 rows
        for i in range(4):  # 4 buttons per row
            x = margin * (i + 1) + button_width * i + (WIDTH - (margin * 5 + button_width * 4)) // 2
            y = HEIGHT // 2 + margin * j + button_height * j - (HEIGHT - (margin * 5 + button_height * 4)) * 2
            buttons.append(pygame.Rect(x, y, button_width, button_height))

    clicked = [False] * len(buttons)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(COBALT)
        
        draw_life()
        
        lab_title = fontH2.render("Laboratory", True, BRIGHTORANGE)
        lab_rect = lab_title.get_rect(center=(WIDTH // 2, HEIGHT // 13*3))
        screen.blit(lab_title, lab_rect)

        # draw buttons with rounded corners and borders
        for index, button in enumerate(buttons):
            outer_rect = pygame.Rect(button.x - border_size, button.y - border_size, button.width + 2 * border_size, button.height + 2 * border_size)
            
            color = button_normal_color
            text_color = text_normal_color
            edge_color = edge_normal_color
            
            # change color when cleared
            if player_state[0][index] == 1:
                color = button_clear_color
                text_color = text_clear_color
                edge_color = edge_clear_color
            
            # only activate if lab unlocked
            if player_state[1][index] == 1:
                # check button is clicked
                if outer_rect.collidepoint(mouse_pos):
                    if clicked[index]:
                        color = button_click_color
                        text_color = text_click_color
                        edge_color = edge_click_color
                    else:
                        color = button_hover_color
                        text_color = text_hover_color
                        edge_color = edge_hover_color
            
            pygame.draw.rect(screen, edge_color, outer_rect, border_radius=border_radius)

            pygame.draw.rect(screen, color, button, border_radius=border_radius)
            
            if player_state[1][index] == 1:
                for i in range(len(LAB_NAME[index].split())):
                    level_number_text = fontP.render(LAB_NAME[index].split()[i], True, text_color)
                    text_rect = level_number_text.get_rect(center=(button.centerx, button.centery + (i - (len(LAB_NAME[index].split()) - 1) / 2) * 18))
                    screen.blit(level_number_text, text_rect)

        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for index, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        if player_state[1][index] == 1:
                            clicked[index] = True
                            selected_lab = index + 1
                            current_screen = 'solve_puzzle'
                            running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for index in range(len(clicked)):
                    clicked[index] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = 'main_title'
                    running = False
                if event.key == pygame.K_r:
                    reset_life()

        pygame.display.update()
        FPS_clock.tick(FPS)

# game title page main code
def main_title():
    global current_screen
    running = True
    while running:
        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    current_screen = 'lab_select'
                    running = False
                elif event.key == pygame.K_r:
                    reset_life()

        screen.fill(COBALT)
        
        draw_life()

        title = fontH1.render("Follow the Life", True, BRIGHTORANGE)
        game = fontP.render(">  Press Space to Start  <", True, BRIGHTORANGE)
        lab_title = fontP.render("> Press L for Laboratory <", True, BRIGHTORANGE)
        
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6*2.5))
        game_rect = game.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.45))
        lab_title_rect = lab_title.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.7))

        screen.blit(title, title_rect)
        screen.blit(game, game_rect)
        screen.blit(lab_title, lab_title_rect)

        pygame.display.update()
        FPS_clock.tick(FPS)

# game loop, spine
def game_loop():
    global current_screen
    # load_screen()
    while True:
        if current_screen == 'main_title':
            main_title()
        elif current_screen == 'lab_select':
            lab_select()
        elif current_screen == 'solve_puzzle':
            main_lab()

game_loop()