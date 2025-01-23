import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Button properties
button_width = 100
button_height = 50
button_color = BLUE
button_hover_color = RED
button_x = SCREEN_WIDTH // 2
button_y = SCREEN_HEIGHT // 2

# Additional buttons
additional_buttons = []
num_additional_buttons = 5

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Click Example')

# Font setup
font = pygame.font.Font(None, 36)

def draw_button(x, y, color, text):
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (button_width - text_surface.get_width()) // 2, y + (button_height - text_surface.get_height()) // 2))

def main():
    running = True
    show_additional_buttons = False
    button_expand_width = 0
    max_expand_width = (button_width + 10) * num_additional_buttons
    expand_speed = 4  # Slower animation speed
    
    while running:
        screen.fill(WHITE)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    show_additional_buttons = not show_additional_buttons

        # Draw main button
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Animate additional buttons
        if show_additional_buttons:
            if button_expand_width < max_expand_width:
                button_expand_width += expand_speed  # Slow down the expansion
        else:
            if button_expand_width > 0:
                button_expand_width -= expand_speed  # Slow down the hiding
        
        # Draw additional buttons
        if button_expand_width > 0:
            for i in range(num_additional_buttons):
                button_pos_x = button_x - (i + 1) * (button_width + 10) + (max_expand_width - button_expand_width)
                if button_pos_x < button_x:
                    draw_button(button_pos_x, button_y, button_color, f'Button {i + 1}')
        
        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            draw_button(button_x, button_y, button_hover_color, 'Click Me')
        else:
            draw_button(button_x, button_y, button_color, 'Click Me')

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
