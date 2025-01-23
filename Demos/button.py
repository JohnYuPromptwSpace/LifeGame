import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Button Example')

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define button properties
button_color = BLUE
button_hover_color = GREEN
button_rect = pygame.Rect(270, 190, 100, 50)

# Define font
font = pygame.font.Font(None, 36)
font.set_bold(True)  # Make the font bold

# Define the button text
button_text = font.render('||', True, WHITE)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Button clicked!")

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check if the mouse is over the button
    if button_rect.collidepoint(mouse_pos):
        current_button_color = button_hover_color
    else:
        current_button_color = button_color

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the button
    pygame.draw.rect(screen, current_button_color, button_rect)

    # Draw the text on the button
    screen.blit(button_text, button_text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
