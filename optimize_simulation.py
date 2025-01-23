import pygame
import numpy as np
from collections import defaultdict
import pyautogui
from numba import njit

pygame.init()

FPS = 60
FPS_clock = pygame.time.Clock()

BRIGHTERCOBALT = (25, 41, 59)
BRIGHTCOBALT = (32, 52, 71)
BITBRIGHTCOBALT = (30, 48, 67)
COBALT = (23, 38, 55)

BRIGHTORANGE = (233, 200, 68)
BITBRIGHTORANGE = (192, 153, 69)
LITTLEBRIGHTORANGE = (164, 145, 62)
ORANGE = (117, 109, 79)
BITDARKORANGE = (86, 76, 55)
DARKORANGE = (73, 68, 55)
DARKERORANGE = (36, 47, 55)

fontP = pygame.font.SysFont('monospace', 5 * 6, bold=True)

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

def load_game_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = set()
    for line in lines:
        row = tuple([int(char) for char in line.strip().split(",")])
        result.add(row)

    return result

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
    DEAD = 0
    LIVE = 16

    def update_track_cell():
        track_cell = np.zeros((MAP_HEIGHT * MAP_WIDTH), dtype=bool)
        for pos in current_map:
            track_cell[pos[1] * MAP_WIDTH + pos[0]] = 1
        return track_cell

    def uninteresting(cell):
        if cell in interesting:
            del interesting[cell]

    def rest_in_peace(cell):
        pass

    def be_born(cell):
        interesting[cell] = LIVE + 3  # 태어난 후 상태 업데이트
        for neighbor in neighbors(cell):
            if neighbor not in interesting:
                interesting[neighbor] = DEAD + 1
            else:
                interesting[neighbor] += 1

    def not_possible(cell):
        raise ValueError("불가능한 상태입니다.")

    def die(cell):
        interesting[cell] = DEAD + 2  # 죽은 후 상태 업데이트
        for neighbor in neighbors(cell):
            if neighbor in interesting:
                interesting[neighbor] -= 1
                if interesting[neighbor] == 0:
                    uninteresting(neighbor)

    def stay_alive(cell):
        pass

    @njit
    def neighbors(cell, MAP_WIDTH, MAP_HEIGHT):
        r, c = divmod(cell, MAP_WIDTH)
        neighbor_indices = [
            (r - 1) * MAP_WIDTH + (c - 1), (r - 1) * MAP_WIDTH + c, (r - 1) * MAP_WIDTH + (c + 1),
            r * MAP_WIDTH + (c - 1), r * MAP_WIDTH + (c + 1),
            (r + 1) * MAP_WIDTH + (c - 1), (r + 1) * MAP_WIDTH + c, (r + 1) * MAP_WIDTH + (c + 1)
        ]
        return [i for i in neighbor_indices if 0 <= i < MAP_WIDTH * MAP_HEIGHT]

    # 동작 리스트 정의
    actions = {
        0: uninteresting,
        1: rest_in_peace,
        2: rest_in_peace,
        3: be_born,
        4: rest_in_peace,
        5: rest_in_peace,
        6: rest_in_peace,
        7: rest_in_peace,
        8: rest_in_peace,
        9: not_possible,
        10: not_possible,
        11: not_possible,
        12: not_possible,
        13: not_possible,
        14: not_possible,
        15: not_possible,
        16: die,
        17: die,
        18: stay_alive,
        19: stay_alive,
        20: die,
        21: die,
        22: die,
        23: die,
        24: die
    }

    # Load current map (live cell positions)
    current_map = load_game_map(f"save_data{1}.txt")
    interesting = {pos[1] * MAP_WIDTH + pos[0]: LIVE + 3 for pos in current_map}

    SCREEN_UPDATE_TICK_CNT = 0
    SCREEN_UPDATE_TICK = 1

    track_cell = update_track_cell()  # Changed to numpy array for faster access
    pause = False

    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))

    # Camera settings
    camera_x, camera_y = 0, 0
    dragging = False
    drag_start_x, drag_start_y = 0, 0
    camera_start_x, camera_start_y = 0, 0
    minimap_fullscreen = False
    mouse_init = False

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Toggle fullscreen minimap with 'F' key
                    minimap_fullscreen = not minimap_fullscreen
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_SPACE:
                    pause = not pause

        if not pause:
            SCREEN_UPDATE_TICK_CNT += 1

            # Render world_surface(cells) + update grid
            if SCREEN_UPDATE_TICK_CNT >= SCREEN_UPDATE_TICK * FPS_clock.get_fps() / 30:
                world_surface.fill(COBALT)

                neighbor_count = defaultdict(int)  # Reset neighbor count each tick

                # Count neighbors for each live cell and its neighbors
                for cell in interesting.keys():
                    r, c = divmod(cell, MAP_WIDTH)
                    pygame.draw.rect(world_surface, LITTLEBRIGHTORANGE, (c * GAME_CELL_SIZE, r * GAME_CELL_SIZE, GAME_CELL_SIZE, GAME_CELL_SIZE))

                    for neighbor in neighbors(cell, MAP_WIDTH, MAP_HEIGHT):
                        if neighbor != cell:
                            neighbor_count[neighbor] += 1

                new_interesting = defaultdict(int)

                for cell, count in neighbor_count.items():
                    if count == 3 or (count == 2 and track_cell[cell]):
                        new_interesting[cell] = LIVE + 3 if count == 3 else interesting[cell]
                
                for cell in list(interesting.keys()):
                    actions[interesting[cell]](cell)

                interesting = new_interesting
                track_cell = update_track_cell()  # Update track cell once per tick

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

        FPS_title = fontP.render(f"FPS: {FPS_clock.get_fps()}", True, BRIGHTORANGE)

        screen.blit(FPS_title, (10, 10))

        pygame.display.update()
        FPS_clock.tick(FPS)

if __name__ == "__main__":
    main_game()