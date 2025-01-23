import pygame
import sys

class DialogBox:
    def __init__(self, screen, text, width=400, height=200):
        self.screen = screen
        self.text = text
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 24)
        self.text_lines = text.split('\n')

        # Calculate dialog box position
        screen_width, screen_height = self.screen.get_size()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Colors
        self.bg_color = (200, 200, 200)
        self.border_color = (0, 0, 0)
        self.text_color = (0, 0, 0)

    def draw(self):
        # Draw the dialog box
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)

        # Render and draw the text
        for i, line in enumerate(self.text_lines):
            line_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(line_surface, (self.x + 20, self.y + 20 + i * 30))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return False
        return True

def main():
    # Initialize Pygame
    pygame.init()

    # Screen settings
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pygame Dialog Box Example")

    # Create a DialogBox instance
    dialog_text = "This is a simple dialog box.\nPress Enter to continue."
    dialog_box = DialogBox(screen, dialog_text)

    # Main loop
    running = True
    show_dialog = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if show_dialog:
                show_dialog = dialog_box.handle_event(event)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the dialog box if needed
        if show_dialog:
            dialog_box.draw()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()