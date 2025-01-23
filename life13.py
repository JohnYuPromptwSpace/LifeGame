"""
v0.1.20
Finished create menu
"""

import pygame
import numpy as np
import time
import sys
from collections import defaultdict
import pyautogui
import lib.lifeextension as lifx
from numba import njit

pygame.init()

pygame.display.set_caption("Follow the Life")
FPS = 60
FPS_clock = pygame.time.Clock()
display_FPS = True

WIDTH,HEIGHT = pyautogui.size()

# def background life const
CELL_SIZE = 7
GRID_SIZE_X = WIDTH //CELL_SIZE
GRID_SIZE_Y = HEIGHT // CELL_SIZE

# WIDTH = GRID_SIZE_X * CELL_SIZE
# HEIGHT = GRID_SIZE_Y * CELL_SIZE

# def screen. based on background life grid
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

# def colors
BRIGHTERCOBALT = (25, 41, 59)
BRIGHTCOBALT = (32, 52, 71)
BITBRIGHTCOBALT = (30, 48, 67)
ABITBRIGHTCOBALT = (29,44,57)
COBALT = (23, 38, 55)
DARKCOBALT = (24,35,44)

BRIGHTORANGE = (233, 200, 68)
BITBRIGHTORANGE = (192, 153, 69)
LITTLEBRIGHTORANGE = (164,145,62)
ORANGE = (117, 109, 79)
BITDARKORANGE = (86, 76, 55)
DARKORANGE = (73, 68, 55)
DARKERORANGE = (36, 47, 55)

# def fonts
pygame.font.init()

fontS1 = pygame.font.SysFont('monospace', int(CELL_SIZE * 4), bold=True)
fontS2 = pygame.font.SysFont('monospace', int(CELL_SIZE * 3.2), bold=True)
fontP = pygame.font.SysFont('monospace', int(CELL_SIZE * 4), bold=True)
fontH2 = pygame.font.SysFont('monospace', int(CELL_SIZE * 8 * (2/3)), bold=True)
fontH1 = pygame.font.SysFont('monospace', int(CELL_SIZE * 8), bold=True)

selected_lab = 1  # Tracks the selected lab(puzzle)
current_screen = 'main_title'  # Manage screen state
current_game_data = 0 # Track game screen

# def background life grid
alive_cells = set()
for i in range(GRID_SIZE_Y):
    for j in range(GRID_SIZE_X):
        if np.random.randint(10) == 0:
            alive_cells.add((i, j))

# def lab const
LAB_NAME = ["Toad", "Beacon", "Glider", "Pulsar", "48P22.1", "Achim's p11", "Flicker", "Gosper Glider Gun"]
LAB_FONTS = [0,0,0,0,1,1,1,1]
LAB_DELAY = [10,10,10,7,3,3,3,3]

LIFE_NAME = ["Block", "Blinker","Glider stopper","Toad", "Beacon", "Glider", "Pulsar", "48P22.1", "Achim's p11", "Flicker", "Gosper Glider Gun"]

LAB_SIZE = [3,3,3,6,6,8,10,7]
LAB_ADJ = [5/9,5/9,5/9,9/11,6/7,6/7,6/7,6/7]

updateGrid_cnt = 0
updateGrid_li = 1

# Dialog manage list
dialogs = []

# load puzzle answer
def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        row = [int(char) for char in line.strip()]
        result.append(row)

    return result


# scores
scores = list(map(lambda x:x[0], load_data("data/map_save_data/score.txt")))

# load settings
# 0: FPS
def load_data_settings(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        row = line.strip()
        result.append(row)

    return result

# init settings
settings_data = load_data_settings("data/player_data/settings.txt")
FPS = int(settings_data[0])
display_FPS = True if settings_data[1] == "Show" else False

# load game map
def load_game_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = set()
    for line in lines:
        row = tuple([int(char) for char in line.strip().split(",")])
        result.add(row)

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

# save player state
def save_player_state():
    with open("data/player_data/player_state.txt", 'w') as file:
        for data in player_state:
            file.write("".join(map(str,data)) + "\n")

# save player state
def save_puzzle_data():
    for i, PUZZLE_MAP in enumerate(LAB_NAME):
        with open(f"data/player_data/{PUZZLE_MAP}.txt", 'w') as file:
            for data in player_solution[i]:
                file.write("".join(map(str,data)) + "\n")
                
# save map data
def save_map_data(currMap, idx,W):
    with open(f"data/map_save_data/save_data{idx}.txt", 'w') as file:
        for pos in currMap.keys():
            file.write(str(pos%W) + ", " + str(pos//W) + "\n")
    
    with open(f"data/map_save_data/score.txt", 'w') as file:
        for score in scores:
            file.write(str(score) + "\n")

# save settings
def save_settings_data(currdata):
    with open(f"data/player_data/settings.txt", 'w') as file:
        for setting in currdata:
            file.write(str(setting) + "\n")

# quit game
def quit_game():
    save_player_state()
    save_puzzle_data()
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
    global alive_cells
    new_alive_cells = set()
    neighbor_counts = defaultdict(int)
    
    for (i, j) in alive_cells:
        for x in range(max(i - 1, 0), min(i + 2, GRID_SIZE_Y)):
            for y in range(max(j - 1, 0), min(j + 2, GRID_SIZE_X)):
                if (x, y) != (i, j):
                    neighbor_counts[(x, y)] += 1

    for (cell, count) in neighbor_counts.items():
        if count == 3 or (count == 2 and cell in alive_cells):
            new_alive_cells.add(cell)

    alive_cells = new_alive_cells

# render background life
def draw_life():
    global alive_cells, updateGrid_li, updateGrid_cnt
    screen.fill(COBALT)
    for (row, col) in alive_cells:
        pygame.draw.rect(screen, DARKERORANGE, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])
    updateGrid_cnt += 1
    if updateGrid_cnt >= updateGrid_li * FPS_clock.get_fps() / FPS:
        update_grid()
        updateGrid_cnt = 0

# reset background life grid
def reset_life():
    global alive_cells
    alive_cells = set()
    for i in range(GRID_SIZE_Y):
        for j in range(GRID_SIZE_X):
            if np.random.randint(10) == 0:
                alive_cells.add((i, j))

# main game screen
def main_game():
    global current_screen, display_FPS

    # Define main game constants
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    WORLD_WIDTH, WORLD_HEIGHT = 8000, 7000
    GAME_CELL_SIZE = 20
    MAP_WIDTH = WORLD_WIDTH // GAME_CELL_SIZE
    MAP_HEIGHT = WORLD_HEIGHT // GAME_CELL_SIZE
    MINIMAP_SIZE = 5
    MINIMAP_WIDTH, MINIMAP_HEIGHT = SCREEN_WIDTH / MINIMAP_SIZE, SCREEN_HEIGHT / MINIMAP_SIZE

    # State definitions
    LIVE = 1

    @njit
    def neighbors(MAP_WIDTH, MAP_HEIGHT, cell):
        neighbor_indices = [cell-1,cell+1,cell-MAP_WIDTH,cell-MAP_WIDTH-1,cell-MAP_WIDTH+1,cell+MAP_WIDTH,cell+MAP_WIDTH-1,cell+MAP_WIDTH+1]
        return [i for i in neighbor_indices if 0 <= i < MAP_WIDTH * MAP_HEIGHT]

    # Load current map (live cell positions)
    current_map = load_game_map(f"data/map_save_data/save_data{current_game_data+1}.txt")
    interesting = {pos[1] * MAP_WIDTH + pos[0]: LIVE for pos in current_map}
    SCREEN_UPDATE_TICK_CNT = 0
    SCREEN_UPDATE_TICK = 1

    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))

    # Camera settings
    camera_x, camera_y = 0, 0
    dragging = False
    drag_start_x, drag_start_y = 0, 0
    camera_start_x, camera_start_y = 0, 0
    minimap_fullscreen = False
    mouse_init = False

    pause = False
    prevpause = pause
    running = True
    
    # 0: spectator
    mode = 0
    
    button_font = pygame.font.Font(None, GAME_CELL_SIZE * 2)

    # Define the buttons
    main_button_rect = pygame.Rect(SCREEN_WIDTH-200, SCREEN_HEIGHT-83, 150, 50)
    main_button_text = button_font.render('Menu', True, BRIGHTORANGE)
    main_button_text_rect = main_button_text.get_rect(center=main_button_rect.center)
    buttons = [
        [main_button_rect, main_button_text, main_button_text_rect, "Menu"]
    ]
    
    button_pause_rect = pygame.Rect(main_button_rect.x - 160, main_button_rect.y, 150, 50)
    button_pause_text = button_font.render('Stop', True, BRIGHTORANGE)
    button_pause_text_rect = button_pause_text.get_rect(center=button_pause_rect.center)
    buttons.append([button_pause_rect, button_pause_text, button_pause_text_rect, "Stop", 160])
    
    button_mode_rect = pygame.Rect(main_button_rect.x - 370, main_button_rect.y, 200, 50)
    button_mode_text = button_font.render('Manage', True, BRIGHTORANGE)
    button_mode_text_rect = button_mode_text.get_rect(center=button_mode_rect.center)
    buttons.append([button_mode_rect, button_mode_text, button_mode_text_rect, "Manage", 370])
    
    main_button_expanded = False
    button_expand_width = 0
    button_expand_height = 0
    max_expand_height = 120
    height_expand_speed = 50
    max_expand_width = (160 + 10) * 2
    expand_speed = 76  # Slower animation speed
    
    pannel_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    pannel_color = (233, 200, 68)
    top_left = (SCREEN_WIDTH - 630, SCREEN_HEIGHT - 120)
    top_right = (SCREEN_WIDTH, SCREEN_HEIGHT - 120)
    bottom_left = (SCREEN_WIDTH - 700, SCREEN_HEIGHT)
    bottom_right = (SCREEN_WIDTH, SCREEN_HEIGHT)
    trapezoid_points = [top_left, top_right, bottom_right, bottom_left]

    # Draw the trapezoid on the transparent surface
    pygame.draw.polygon(pannel_surface, pannel_color, trapezoid_points)
    
    pannel_color = BRIGHTCOBALT
    top_left = (SCREEN_WIDTH - 625, SCREEN_HEIGHT - 110)
    top_right = (SCREEN_WIDTH, SCREEN_HEIGHT - 110)
    bottom_left = (SCREEN_WIDTH - 685, SCREEN_HEIGHT)
    bottom_right = (SCREEN_WIDTH, SCREEN_HEIGHT)
    trapezoid_points = [top_left, top_right, bottom_right, bottom_left]

    # Draw the trapezoid on the transparent surface
    pygame.draw.polygon(pannel_surface, pannel_color, trapezoid_points)
    
    # function buttons
    create_button_rect = pygame.Rect(50, SCREEN_HEIGHT-83, 150, 50)
    create_button_text = button_font.render('Create', True, BRIGHTORANGE)
    create_button_text_rect = create_button_text.get_rect(center=create_button_rect.center)
    manage_buttons = [
        [create_button_rect, create_button_text, create_button_text_rect, "Create",0]
    ]
    
    button_kill_rect = pygame.Rect(create_button_rect.x + 160, create_button_rect.y, 100, 50)
    button_kill_text = button_font.render('Kill', True, BRIGHTORANGE)
    button_kill_text_rect = button_kill_text.get_rect(center=button_kill_rect.center)
    manage_buttons.append([button_kill_rect, button_kill_text, button_kill_text_rect, "Kill", 160])
    
    manage_expand_height = 0
    max_expand_height_manage = 120
    height_expand_speed_manage = 50
    manage_mode = 0
    # 0 : None, 1 : Create, 3 : Kill
    
    manage_pannel_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    pannel_color = (233, 200, 68)
    manage_top_left = (0, SCREEN_HEIGHT-120)
    manage_top_right = (330, SCREEN_HEIGHT-120)
    manage_bottom_left = (0, SCREEN_HEIGHT)
    manage_bottom_right = (400, SCREEN_HEIGHT)
    manage_trapezoid_points = [manage_top_left, manage_top_right, manage_bottom_right, manage_bottom_left]

    # Draw the trapezoid on the transparent surface
    pygame.draw.polygon(manage_pannel_surface, pannel_color, manage_trapezoid_points)
    
    pannel_color = BRIGHTCOBALT
    manage_top_left = (0, SCREEN_HEIGHT - 110)
    manage_top_right = (325, SCREEN_HEIGHT - 110)
    manage_bottom_left = (0, SCREEN_HEIGHT)
    manage_bottom_right = (385, SCREEN_HEIGHT)
    manage_trapezoid_points = [manage_top_left, manage_top_right, manage_bottom_right, manage_bottom_left]

    # Draw the trapezoid on the transparent surface
    pygame.draw.polygon(manage_pannel_surface, pannel_color, manage_trapezoid_points)
    
    # Scroll bar init  
    life_create_buttons = lifx.ScrollableItemList(screen,11,100,150,3,SCREEN_WIDTH,SCREEN_HEIGHT-119,15,fontP,LIFE_NAME)
    
    scroll_bar_show = False
    scroll_bar_toggle = pygame.Rect(0, 200, 120, 50)
    scroll_bar_toggle_text = button_font.render('Lifes', True, BRIGHTORANGE)
    scroll_bar_toggle_text_rect = scroll_bar_toggle_text.get_rect(center=scroll_bar_toggle.center)
    
    life_create_expand_width = 0
    life_create_max_expand_width = 165
    life_create_expand_speed = 76
    
    # scores
    maxlifes = scores[current_game_data]
    log_text_height= fontP.size("A")[1]
    
    selected = None
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if dialogs:
                currDialog = dialogs[0]
                if currDialog.handle_event(event) == True:
                    current_screen = "map_select"
                    save_map_data(interesting, current_game_data+1,MAP_WIDTH)
                    del currDialog
                    scores[current_game_data] = maxlifes
                    running = False
                elif currDialog.handle_event(event) == False:
                    pause = prevpause
                    del currDialog
                    dialogs.clear()
            else:
                if scroll_bar_show:
                    a = life_create_buttons.handle_event(event,selected)
                    if a != 1: selected = a
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # Toggle fullscreen minimap with 'F' key
                        minimap_fullscreen = not minimap_fullscreen
                    elif event.key == pygame.K_ESCAPE:
                        prevpause = pause
                        pause = True
                        quitGameDia = lifx.DialogBox(screen, "Save and Exit Life?", "Press ENTER to Continue\nPress ESCAPE to Discard", width=WIDTH//5, height=HEIGHT//5)
                        dialogs.append(quitGameDia)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0][0].collidepoint(event.pos):
                        main_button_expanded = not main_button_expanded
                    if main_button_expanded:
                        if buttons[2][0].collidepoint(event.pos):
                            if buttons[2][3] == "Spectate":
                                buttons[2][1] = button_font.render('Manage', True, BRIGHTORANGE)
                                buttons[2][3] = "Manage"
                                
                                if prevpause == False:
                                    buttons[1][1] = button_font.render('Stop', True, BRIGHTORANGE)
                                    buttons[1][3] = "Stop"
                                    pause = False
                                else:
                                    buttons[1][1] = button_font.render('Play', True, BRIGHTORANGE)
                                    buttons[1][3] = "Play"
                                    pause = True
                                manage_mode = 0
                                mode = 0
                            else:
                                buttons[2][1] = button_font.render('Spectate', True, BRIGHTORANGE)
                                buttons[2][3] = "Spectate"
                                buttons[1][1] = button_font.render('Play', True, BRIGHTORANGE)
                                buttons[1][3] = "Play"
                                prevpause = pause
                                pause = True
                                mode = 1
                        if mode == 0 and buttons[1][0].collidepoint(event.pos):
                            if buttons[1][3] == "Stop":
                                buttons[1][1] = button_font.render('Play', True, BRIGHTORANGE)
                                buttons[1][3] = "Play"
                                pause = True
                            else:
                                buttons[1][1] = button_font.render('Stop', True, BRIGHTORANGE)
                                buttons[1][3] = "Stop"
                                pause = False
                    if mode == 1:
                        if manage_buttons[0][0].collidepoint(event.pos):
                            if manage_mode == 1:
                                manage_mode = 0
                            else:
                                manage_mode = 1
                                scroll_bar_show = False
                        elif manage_buttons[1][0].collidepoint(event.pos):
                            if manage_mode == 2:
                                manage_mode = 0
                            else:
                                manage_mode = 2
                    if scroll_bar_toggle.collidepoint(event.pos):
                        scroll_bar_show = not scroll_bar_show
                if mode == 0:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            mouse_x, mouse_y = event.pos
                            minimap_rect = pygame.Rect(SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10, MINIMAP_WIDTH, MINIMAP_HEIGHT)
                            if minimap_fullscreen:
                                dragging = True
                                camera_x = int(mouse_x * WORLD_WIDTH / SCREEN_WIDTH - SCREEN_WIDTH / 2)
                                camera_y = int(mouse_y * WORLD_HEIGHT / SCREEN_HEIGHT - SCREEN_HEIGHT / 2)

                                camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
                                camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
                            elif minimap_rect.collidepoint(mouse_x, mouse_y):
                                if not dragging:
                                    mouse_init = True
                                dragging = True
                                relative_mouse_x = mouse_x - (SCREEN_WIDTH - MINIMAP_WIDTH - 10)
                                relative_mouse_y = mouse_y - 10
                                camera_x = int(relative_mouse_x * WORLD_WIDTH / MINIMAP_WIDTH - SCREEN_WIDTH / 2)
                                camera_y = int(relative_mouse_y * WORLD_HEIGHT / MINIMAP_HEIGHT - SCREEN_HEIGHT / 2)

                                camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
                                camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
                            else:
                                if not dragging:
                                    mouse_init = False
                                dragging = True
                                drag_start_x, drag_start_y = event.pos
                                camera_start_x, camera_start_y = camera_x, camera_y
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:  # Left mouse button
                            dragging = False
                            mouse_init = False
                    elif event.type == pygame.MOUSEMOTION:
                        if dragging:
                            if minimap_fullscreen:
                                mouse_x, mouse_y = event.pos
                                camera_x = int(mouse_x * WORLD_WIDTH / SCREEN_WIDTH - SCREEN_WIDTH / 2)
                                camera_y = int(mouse_y * WORLD_HEIGHT / SCREEN_HEIGHT - SCREEN_HEIGHT / 2)
                            else:
                                mouse_x, mouse_y = event.pos
                                minimap_rect = pygame.Rect(SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10, MINIMAP_WIDTH, MINIMAP_HEIGHT)
                                if mouse_init:
                                    relative_mouse_x = mouse_x - (SCREEN_WIDTH - MINIMAP_WIDTH - 10)
                                    relative_mouse_y = mouse_y - 10
                                    camera_x = int(relative_mouse_x * WORLD_WIDTH / MINIMAP_WIDTH - SCREEN_WIDTH / 2)
                                    camera_y = int(relative_mouse_y * WORLD_HEIGHT / MINIMAP_HEIGHT - SCREEN_HEIGHT / 2)
                                else:
                                    dx, dy = event.pos[0] - drag_start_x, event.pos[1] - drag_start_y
                                    camera_x = camera_start_x - dx
                                    camera_y = camera_start_y - dy

                            # Clamp the camera to the bounds of the world
                            camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
                            camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
                elif mode == 1:
                    print(selected)
        
        if not pause:
            if len(interesting.keys()) > maxlifes:
                maxlifes = len(interesting.keys())
            
            SCREEN_UPDATE_TICK_CNT += 1

            # Render world_surface(cells) + update grid
            if SCREEN_UPDATE_TICK_CNT >= SCREEN_UPDATE_TICK * FPS_clock.get_fps() / 30:
                world_surface.fill(COBALT)

                neighbor_count = defaultdict(int)  # Reset neighbor count each tick

                # Count neighbors for each live cell and its neighbors
                cells = interesting.keys()
                for cell in cells:
                    r, c = divmod(cell, MAP_WIDTH)
                    pygame.draw.rect(world_surface, LITTLEBRIGHTORANGE, (c * GAME_CELL_SIZE, r * GAME_CELL_SIZE, GAME_CELL_SIZE, GAME_CELL_SIZE))

                    for neighbor in neighbors(MAP_WIDTH, MAP_HEIGHT,cell):
                        neighbor_count[neighbor] += 1

                interesting = {}

                for cell, count in neighbor_count.items():
                    if count == 3:
                        interesting[cell] = LIVE
                        continue
                    
                    if count == 2 and cell in cells:
                        interesting[cell] = LIVE

                SCREEN_UPDATE_TICK_CNT = 0

        screen.fill(COBALT)

        if minimap_fullscreen:
            # Render the full-screen minimap
            full_minimap = pygame.transform.scale(world_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(full_minimap, (0, 0))
            minimap_rect = pygame.Rect(
                camera_x * (SCREEN_WIDTH / WORLD_WIDTH),
                camera_y * (SCREEN_HEIGHT / WORLD_HEIGHT),
                SCREEN_WIDTH * (SCREEN_WIDTH / WORLD_WIDTH),
                SCREEN_HEIGHT * (SCREEN_HEIGHT / WORLD_HEIGHT)
            )
            pygame.draw.rect(screen, BRIGHTORANGE, minimap_rect, 2)
        else:
            # Calculate the portion of the world to render
            world_rect = pygame.Rect(camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT)
            visible_world = world_surface.subsurface(world_rect)

            # Render the visible portion of the world
            screen.blit(visible_world, (0, 0))

            # Draw the minimap

            # Create minimap surface
            minimap_surface = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
            minimap_surface.set_alpha(200)  # Make the minimap slightly transparent

            minimap_scaled = pygame.transform.scale(world_surface, (MINIMAP_WIDTH, MINIMAP_HEIGHT))
            minimap_surface.blit(minimap_scaled, (0, 0))
            minimap_scale_x = MINIMAP_WIDTH / WORLD_WIDTH
            minimap_scale_y = MINIMAP_HEIGHT / WORLD_HEIGHT
            minimap_rect = pygame.Rect(
                camera_x * minimap_scale_x,
                camera_y * minimap_scale_y,
                SCREEN_WIDTH * minimap_scale_x,
                SCREEN_HEIGHT * minimap_scale_y
            )
            pygame.draw.rect(minimap_surface, BRIGHTORANGE, minimap_rect, 2)

            # Blit the minimap to the main screen
            screen.blit(minimap_surface, (SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10))

            # Draw outer line of minimap
            pygame.draw.rect(screen, BRIGHTORANGE, (SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10, MINIMAP_WIDTH, MINIMAP_HEIGHT), 1)

        # blit log / scores
        life_log = fontP.render(f"Lifes : {len(interesting.keys())}", True, BRIGHTORANGE)
        screen.blit(life_log, (WIDTH - MINIMAP_WIDTH, MINIMAP_HEIGHT+10))
        
        life_max_log = fontP.render(f"Max Lifes : {maxlifes}", True, BRIGHTORANGE)
        screen.blit(life_max_log, (WIDTH - MINIMAP_WIDTH, MINIMAP_HEIGHT+10+log_text_height))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Animate create life buttons
        if scroll_bar_show:
            if life_create_expand_width < life_create_max_expand_width:
                life_create_expand_width += life_create_expand_speed # Slow down the expansion
                if life_create_expand_width > life_create_max_expand_width:
                    life_create_expand_width = life_create_max_expand_width
        else:
            if life_create_expand_width > 0:
                life_create_expand_width -= life_create_expand_speed # Slow down the hiding
                if life_create_expand_width < 0:
                    life_create_expand_width = 0
        
        # display scroll bar toggle button
        if manage_mode == 1 and minimap_fullscreen == False and not dialogs:
            scroll_bar_toggle[0] = life_create_expand_width
            scroll_bar_toggle_text_rect[0] = scroll_bar_toggle_text.get_rect(center=scroll_bar_toggle.center)[0]
            pygame.draw.rect(screen, BRIGHTORANGE, pygame.Rect(scroll_bar_toggle[0],scroll_bar_toggle[1]-2,scroll_bar_toggle[2]+10,scroll_bar_toggle[3]+4))
            pygame.draw.rect(screen, COBALT if scroll_bar_toggle.collidepoint(mouse_pos) else ABITBRIGHTCOBALT, scroll_bar_toggle.move(0,0))
            screen.blit(scroll_bar_toggle_text, scroll_bar_toggle_text_rect)
        
        if scroll_bar_show:
            # display scroll bar
            if manage_mode == 1 and minimap_fullscreen == False and not dialogs:
                life_create_buttons.update(COBALT,BRIGHTCOBALT,BRIGHTORANGE,BRIGHTORANGE,DARKORANGE,DARKCOBALT,life_create_expand_width-165,CELL_SIZE,selected)
        
        if (mode == 1 or pause == True or (mouse_pos[0] > SCREEN_WIDTH - button_expand_width - 450 and mouse_pos[1] > SCREEN_HEIGHT - 250)) and minimap_fullscreen == False and not dialogs:
            button_expand_height += height_expand_speed
            if button_expand_height > max_expand_height:
                button_expand_height = max_expand_height
        else:
            button_expand_height -= height_expand_speed
            if button_expand_height < 0:
                button_expand_height = 0
        
        # Animate additional buttons
        if main_button_expanded:
            if button_expand_width < max_expand_width:
                button_expand_width += expand_speed # Slow down the expansion
                if button_expand_width > max_expand_width:
                    button_expand_width = max_expand_width
        else:
            if button_expand_width > 0:
                button_expand_width -= expand_speed # Slow down the hiding
                if button_expand_width < 0:
                    button_expand_width = 0
        
        if button_expand_height != 0:
            # draw pannel
            screen.blit(pannel_surface, (76 * 5 - button_expand_width, 120-button_expand_height))
            
            # Draw additional buttons
            if button_expand_width > 0:
                for i in range(1, len(buttons)):
                    button_pos_x = buttons[0][0].x - buttons[i][4] + (max_expand_width - button_expand_width)
                    if button_pos_x < buttons[0][0].x:
                        pygame.draw.rect(screen, BRIGHTORANGE, buttons[i][0].move(button_pos_x - buttons[i][0].x, 120-button_expand_height + 10))
                        pygame.draw.rect(screen, COBALT if buttons[i][0].collidepoint(pygame.mouse.get_pos()) else ABITBRIGHTCOBALT, buttons[i][0].move(button_pos_x - buttons[i][0].x, 120-button_expand_height))
                        screen.blit(buttons[i][1], buttons[i][2].move(button_pos_x - buttons[i][0].x, 120-button_expand_height))

            # Draw the main button
            pygame.draw.rect(screen, BRIGHTORANGE, buttons[0][0].move(0, 120-button_expand_height + 10))
            pygame.draw.rect(screen, COBALT if buttons[0][0].collidepoint(mouse_pos) else ABITBRIGHTCOBALT, buttons[0][0].move(0,120-button_expand_height))
            screen.blit(buttons[0][1], buttons[0][2].move(0,120-button_expand_height))
        
        #Animate manage buttons
        if mode == 1 and minimap_fullscreen == False and not dialogs:
            manage_expand_height += height_expand_speed_manage
            if manage_expand_height > max_expand_height_manage:
                manage_expand_height = max_expand_height_manage
        else:
            manage_expand_height -= height_expand_speed_manage
            if manage_expand_height < 0:
                manage_expand_height = 0
        
        if manage_expand_height != 0:
            # draw manage pannel
            screen.blit(manage_pannel_surface, (0, 120-manage_expand_height))
            
            # Draw manage button
            for i in range(len(manage_buttons)):
                pygame.draw.rect(screen, BRIGHTORANGE, manage_buttons[i][0].move(0, 120-manage_expand_height+10))
                manage_color = 0
                if manage_mode-1 == i:
                    manage_color = DARKCOBALT
                elif manage_buttons[i][0].collidepoint(pygame.mouse.get_pos()):
                    manage_color = COBALT
                else:
                    manage_color = ABITBRIGHTCOBALT
                pygame.draw.rect(screen, manage_color, manage_buttons[i][0].move(0, 120-manage_expand_height))
                screen.blit(manage_buttons[i][1], manage_buttons[i][2].move(0, 120-manage_expand_height))

        
        if dialogs:
            currDialog = dialogs[0]
            currDialog.draw()
        
        if display_FPS:
            lifx.blitFPS(screen, fontP, FPS_clock, BRIGHTORANGE)

        pygame.display.update()
        FPS_clock.tick(FPS)
    dialogs.clear()

# map_select main code
def map_select():
    global current_screen, current_game_data
    
    running = True
    
    # map_select const
    BUTTON_WIDTH = WIDTH // 3
    BUTTON_HEIGHT = HEIGHT // 10
    BUTTON_MARGIN = 20
    BORDER_RADIUS = 15
    BORDER_SIZE = 4

    edge_normal_color = DARKORANGE
    button_normal_color = COBALT
    text_normal_color = DARKORANGE
    
    edge_hover_color = ORANGE
    button_hover_color = BRIGHTCOBALT
    text_hover_color = ORANGE
    
    edge_click_color = BITBRIGHTORANGE
    button_click_color = BRIGHTERCOBALT    
    text_click_color = BITBRIGHTORANGE

    # def map buttons(positions)
    buttons = []
    for i in range(5):
        x = (WIDTH - BUTTON_WIDTH) // 2
        y = BUTTON_MARGIN * (i + 1) + BUTTON_HEIGHT * i + (HEIGHT - (BUTTON_MARGIN * 6 + BUTTON_HEIGHT * 5)) // 9*7
        buttons.append(pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT))

    clicked = [False] * len(buttons)

    while running:
        # handle event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        clicked[index] = True
                        current_game_data = index
                        current_screen = 'main_game'
                        running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for index in range(len(clicked)):
                    clicked[index] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = 'main_title'
                    running = False
                elif event.key == pygame.K_r:
                    reset_life()
        
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(COBALT)
        
        draw_life()
        
        title = fontH1.render("Map Select", True, BRIGHTORANGE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        screen.blit(title, title_rect)

        # draw buttons with rounded corners and borders
        for index, button in enumerate(buttons):
            outer_rect = pygame.Rect(button.x - BORDER_SIZE, button.y - BORDER_SIZE, button.width + 2 * BORDER_SIZE, button.height + 2 * BORDER_SIZE)
            
            color = button_normal_color
            text_color = text_normal_color
            edge_color = edge_normal_color
            
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
            
            pygame.draw.rect(screen, edge_color, outer_rect, border_radius=BORDER_RADIUS)

            pygame.draw.rect(screen, color, button, border_radius=BORDER_RADIUS)
            
            map_name = f"Save Data {index + 1}"
            map_text = fontP.render(map_name, True, text_color)
            map_rect = map_text.get_rect(center=button.center)
            screen.blit(map_text, map_rect)

        if display_FPS:
            lifx.blitFPS(screen, fontP, FPS_clock, BRIGHTORANGE)            
        pygame.display.update()
        FPS_clock.tick(FPS)

# laboratory main code
def main_lab():
    global grid, current_screen, display_FPS
    
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
    
    # main loop
    i = 0
    while running:
        # handle event
        for event in pygame.event.get():
            if dialogs:
                currDialog = dialogs[0]
                if currDialog.handle_event(event) == True:
                    save_player_state()
                    save_puzzle_data()
                    current_screen = "lab_select"
                    del currDialog
                    dialogs.clear()
                    running = False
                elif currDialog.handle_event(event) == False:
                    del currDialog
                    dialogs.clear()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if player_state[0][selected_lab-1]:
                        save_player_state()
                        save_puzzle_data()
                        current_screen = "lab_select"
                        running = False
                    else:
                        quitLabDia = lifx.DialogBox(screen, "Save and Exit Lab?", "Press ENTER to Continue\nPress ESCAPE to Discard", width=WIDTH//5, height=HEIGHT//5)
                        dialogs.append(quitLabDia)
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
            if i > LAB_DELAY[selected_lab-1] * FPS_clock.get_fps() / 20:
                player_solution[selected_lab-1] = update_nono(player_solution[selected_lab-1])
                i = 0
        
        if dialogs:
            currDialog = dialogs[0]
            currDialog.draw()
        
        if display_FPS:
            lifx.blitFPS(screen, fontP, FPS_clock, BRIGHTORANGE)        
        pygame.display.update()
        FPS_clock.tick(FPS)

# lab select page main code
def lab_select():
    global current_screen, selected_lab, display_FPS
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
            y = HEIGHT // 5*2 + margin * j + button_height * j - (HEIGHT - (margin * 5 + button_height * 4)) * 2
            buttons.append(pygame.Rect(x, y, button_width, button_height))

    clicked = [False] * len(buttons)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(COBALT)
        
        draw_life()
        
        lab_title = fontH1.render("Laboratory", True, BRIGHTORANGE)
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
                    text_rect = level_number_text.get_rect(center=(button.centerx, button.centery + (i - (len(LAB_NAME[index].split()) - 1) / 2) * CELL_SIZE * 6))
                    screen.blit(level_number_text, text_rect)

        # handle event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
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

        if display_FPS:
            lifx.blitFPS(screen, fontP, FPS_clock, BRIGHTORANGE)        
        pygame.display.update()
        FPS_clock.tick(FPS)

# game title page main code
def settings():
    global current_screen, selected_lab, display_FPS,FPS, display_FPS
    running = True
    
    settings_data = load_data_settings("data/player_data/settings.txt")

    FPS_dropdown = lifx.Dropdown(HEIGHT // 8, HEIGHT // 13*2.5 + int(CELL_SIZE * 4)*1.5, 200, 40, ["30", "45", "60", "90","120"], fontP, BRIGHTCOBALT, BRIGHTORANGE,BRIGHTCOBALT, BRIGHTERCOBALT, default_text=f"{settings_data[0]}")
    FPS_Show_dropdown = lifx.Dropdown(HEIGHT // 8, HEIGHT // 13*4 + int(CELL_SIZE * 4)*1.5, 200, 40, ["Hide","Show"], fontP, BRIGHTCOBALT, BRIGHTORANGE,BRIGHTCOBALT, BRIGHTERCOBALT, default_text=f"{settings_data[1]}")
    
    active_dropdown = False
    not_active_dropdown = [FPS_dropdown,FPS_Show_dropdown]
    
    while running:        
        # handle event
        for event in pygame.event.get():
            if dialogs:
                currDialog = dialogs[0]
                if currDialog.handle_event(event) == True:
                    current_screen = "main_title"
                    del currDialog
                    dialogs.clear()
                    running = False
                elif currDialog.handle_event(event) == False:
                    del currDialog
                    dialogs.clear()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitLabDia = lifx.DialogBox(screen, "Save and Exit Settings?", "Press ENTER to Continue\nPress ESCAPE to Discard", width=WIDTH//5, height=HEIGHT//5)
                    dialogs.append(quitLabDia)
                if event.key == pygame.K_r:
                    reset_life()
            
            if active_dropdown == FPS_dropdown or not active_dropdown:
                newFPS = FPS_dropdown.handle_event(event)
                if newFPS != None:
                    FPS = int(newFPS)
                    settings_data[0] = FPS                    
            
            if active_dropdown == FPS_Show_dropdown or not active_dropdown:
                newShowFPS = FPS_Show_dropdown.handle_event(event)
                if newShowFPS != None:
                    if newShowFPS == "Show":
                        display_FPS = True
                    else:
                        display_FPS = False
                    settings_data[1] = newShowFPS

        screen.fill(COBALT)
        
        draw_life()
        
        lab_title = fontH1.render("Settings", True, BRIGHTORANGE)
        screen.blit(lab_title, (HEIGHT // 13, HEIGHT // 13))
        
        sel_fps_title = fontP.render("Select FPS", True, BRIGHTORANGE)
        screen.blit(sel_fps_title, (HEIGHT // 8, HEIGHT // 13*2.5))

        
        show_fps_title = fontP.render("Show FPS", True, BRIGHTORANGE)
        screen.blit(show_fps_title, (HEIGHT // 8, HEIGHT // 13*4))
        
        for dropdown in not_active_dropdown:
            dropdown.draw(screen)
            if dropdown.expanded == True:
                active_dropdown = dropdown
        
        if active_dropdown in not_active_dropdown:
            not_active_dropdown.remove(active_dropdown)
        
        if active_dropdown:
            active_dropdown.draw(screen)
            if active_dropdown.expanded == False:
                not_active_dropdown.append(active_dropdown)
                active_dropdown = False
        if dialogs:
            currDialog = dialogs[0]
            currDialog.draw()
        
        if display_FPS:
            lifx.blitFPS(screen, fontP, FPS_clock, BRIGHTORANGE)        
        pygame.display.update()
        FPS_clock.tick(FPS)
    
    save_settings_data(settings_data)

# game title page main code
def main_title():
    global current_screen, display_FPS
    running = True
    while running:
        # handle event
        for event in pygame.event.get():
            if dialogs:
                currDialog = dialogs[0]
                if currDialog.handle_event(event) == True:
                    del currDialog
                    dialogs.clear()
                    quit()
                elif currDialog.handle_event(event) == False:
                    del currDialog
                    dialogs.clear()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    current_screen = 'lab_select'
                    running = False
                elif event.key == pygame.K_s:
                    current_screen = 'settings'
                    running = False
                elif event.key == pygame.K_SPACE:
                    current_screen = 'map_select'
                    running = False
                elif event.key == pygame.K_r:
                    reset_life()
                elif event.key == pygame.K_ESCAPE:
                    quitDia = lifx.DialogBox(screen, "Quit?", "Press ENTER to Continue\nPress ESCAPE to Discard", width=WIDTH//5, height=HEIGHT//5)
                    dialogs.append(quitDia)

        screen.fill(COBALT)
        
        draw_life()

        title = fontH1.render("Follow the Life", True, BRIGHTORANGE)
        game = fontP.render(">  Space for Life Field  <", True, BRIGHTORANGE)
        lab_title = fontP.render(">    L for Laboratory    <", True, BRIGHTORANGE)
        setting_title = fontP.render(">     S for Settings     <", True, BRIGHTORANGE)
        quit_title = fontP.render(">     Escape to Quit     <", True, BRIGHTORANGE)
        
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6*2.4))
        game_rect = game.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.15))
        lab_title_rect = lab_title.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.35))
        setting_title_rect = setting_title.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.55))
        quit_title_rect = lab_title.get_rect(center=(WIDTH // 2, HEIGHT // 6*3.75))

        screen.blit(title, title_rect)
        screen.blit(game, game_rect)
        screen.blit(lab_title, lab_title_rect)
        screen.blit(setting_title, setting_title_rect)
        screen.blit(quit_title, quit_title_rect)
        
        if dialogs:
                currDialog = dialogs[0]
                currDialog.draw()
                
        if display_FPS:
            lifx.blitFPS(screen, fontP, FPS_clock, BRIGHTORANGE)
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
        elif current_screen == 'map_select':
            map_select()
        elif current_screen == 'main_game':
            main_game()
        elif current_screen == 'settings':
            settings()

game_loop()