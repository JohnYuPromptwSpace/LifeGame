import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 750, 500
WORLD_WIDTH, WORLD_HEIGHT = 3200, 2400
MINIMAP_SIZE = 5
MINIMAP_WIDTH, MINIMAP_HEIGHT = SCREEN_WIDTH / MINIMAP_SIZE, SCREEN_HEIGHT / MINIMAP_SIZE  # Size of the minimap
BACKGROUND_COLOR = (30, 30, 30)
FPS = 60

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrollable Screen with Dragging and Minimap")

# Create a surface larger than the screen to represent the world
world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
world_surface.fill(BACKGROUND_COLOR)

# Drawing some example objects in the world
for x in range(0, WORLD_WIDTH, 100):
    for y in range(0, WORLD_HEIGHT, 100):
        pygame.draw.rect(world_surface, (200, 0, 0), (x, y, 50, 50))

# Create the minimap surface
minimap_surface = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
minimap_surface.set_alpha(200)  # Make the minimap slightly transparent

# Pre-render the minimap
minimap_scaled = pygame.transform.scale(world_surface, (MINIMAP_WIDTH, MINIMAP_HEIGHT))

# Camera settings
camera_x, camera_y = 0, 0
dragging = False
drag_start_x, drag_start_y = 0, 0
camera_start_x, camera_start_y = 0, 0
minimap_fullscreen = False

# Main loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                minimap_rect = pygame.Rect(SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10, MINIMAP_WIDTH, MINIMAP_HEIGHT)
                if minimap_fullscreen:
                    dragging = True
                    camera_x = int(mouse_x * WORLD_WIDTH / SCREEN_WIDTH - SCREEN_WIDTH / 2)
                    camera_y = int(mouse_y * WORLD_HEIGHT / SCREEN_HEIGHT - SCREEN_HEIGHT / 2)
                elif minimap_rect.collidepoint(mouse_x, mouse_y):
                    dragging = True
                    relative_mouse_x = mouse_x - (SCREEN_WIDTH - MINIMAP_WIDTH - 10)
                    relative_mouse_y = mouse_y - 10
                    camera_x = int(relative_mouse_x * WORLD_WIDTH / MINIMAP_WIDTH - SCREEN_WIDTH / 2)
                    camera_y = int(relative_mouse_y * WORLD_HEIGHT / MINIMAP_HEIGHT - SCREEN_HEIGHT / 2)
                else:
                    dragging = True
                    drag_start_x, drag_start_y = event.pos
                    camera_start_x, camera_start_y = camera_x, camera_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                if minimap_fullscreen:
                    mouse_x, mouse_y = event.pos
                    camera_x = int(mouse_x * WORLD_WIDTH / SCREEN_WIDTH - SCREEN_WIDTH / 2)
                    camera_y = int(mouse_y * WORLD_HEIGHT / SCREEN_HEIGHT - SCREEN_HEIGHT / 2)
                else:
                    mouse_x, mouse_y = event.pos
                    minimap_rect = pygame.Rect(SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10, MINIMAP_WIDTH, MINIMAP_HEIGHT)
                    if minimap_rect.collidepoint(mouse_x, mouse_y):
                        relative_mouse_x = mouse_x - (SCREEN_WIDTH - MINIMAP_WIDTH - 10)
                        relative_mouse_y = mouse_y - 10
                        camera_x = int(relative_mouse_x * WORLD_WIDTH / MINIMAP_WIDTH - SCREEN_WIDTH / 2)
                        camera_y = int(relative_mouse_y * WORLD_HEIGHT / MINIMAP_HEIGHT - SCREEN_HEIGHT / 2)

                        # Clamp camera position to minimap boundaries
                        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
                        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))
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

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

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
        pygame.draw.rect(screen, (255, 0, 0), minimap_rect, 2)
    else:
        # Calculate the portion of the world to render
        world_rect = pygame.Rect(camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT)
        visible_world = world_surface.subsurface(world_rect)

        # Render the visible portion of the world
        screen.blit(visible_world, (0, 0))

        # Draw the minimap
        minimap_surface.blit(minimap_scaled, (0, 0))
        minimap_scale_x = MINIMAP_WIDTH / WORLD_WIDTH
        minimap_scale_y = MINIMAP_HEIGHT / WORLD_HEIGHT
        minimap_rect = pygame.Rect(
            camera_x * minimap_scale_x,
            camera_y * minimap_scale_y,
            SCREEN_WIDTH * minimap_scale_x,
            SCREEN_HEIGHT * minimap_scale_y
        )
        pygame.draw.rect(minimap_surface, (255, 0, 0), minimap_rect, 2)

        # Blit the minimap to the main screen
        screen.blit(minimap_surface, (SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10))

    pygame.display.update()
    clock.tick(FPS)
