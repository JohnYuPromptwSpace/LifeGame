import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 30
MENU_WIDTH, MENU_HEIGHT = 200, 40
OPTIONS = ["Option 1", "Option 2", "Option 3"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
HOVER_COLOR = (150, 150, 150)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pygame Drop-Down Menu')

font = pygame.font.Font(None, FONT_SIZE)

class Dropdown:
    def __init__(self, x, y, width, height, options, font, bg, tg, sl, default_text="Select an option"):
        self.rect = pygame.Rect(x, y, width, height)
        self.bgcolor = bg
        self.tgcolor = tg
        self.slcolor = sl
        self.options = options
        self.font = font
        self.selected = default_text
        self.expanded = False
        self.hovered_option = -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.bgcolor, self.rect)
        text = self.font.render(self.selected, True, self.tgcolor)
        surface.blit(text, (self.rect.x + 10, self.rect.y + 10))

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                color = self.slcolor if i != self.hovered_option else HOVER_COLOR
                pygame.draw.rect(surface, color, option_rect)
                option_text = self.font.render(option, True, self.tgcolor)
                surface.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected = option
                        self.expanded = False
        elif event.type == pygame.MOUSEMOTION:
            if self.expanded:
                self.hovered_option = -1
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.hovered_option = i
                        break

dropdown = Dropdown(100, 100, MENU_WIDTH, MENU_HEIGHT, OPTIONS, font, WHITE, BLACK, GRAY)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        dropdown.handle_event(event)

    screen.fill(BLUE)
    dropdown.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
