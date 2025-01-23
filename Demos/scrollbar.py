import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ITEM_WIDTH = 100
ITEM_HEIGHT = 100
ITEM_MARGIN = 5
NUM_ITEMS = 20
SCROLL_BAR_WIDTH = 20
SCROLL_SPEED = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
LIGHT_GREY = (200, 200, 200)

# Font
FONT = pygame.font.SysFont(None, 36)


class ScrollableItemList:
    def __init__(self, screen):
        self.screen = screen
        self.total_items_height = NUM_ITEMS * (ITEM_HEIGHT + ITEM_MARGIN) - ITEM_MARGIN
        self.scroll_y = 0
        self.scroll_button_height = max(SCREEN_HEIGHT / self.total_items_height * SCREEN_HEIGHT, 20)
        self.scroll_button_y = 0
        self.dragging = False
        self.mouse_offset_y = 0
        self.items = [f"Item {i + 1}" for i in range(NUM_ITEMS)]

    def draw_items(self):
        y = -self.scroll_y
        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(0, y, ITEM_WIDTH, ITEM_HEIGHT)
            if item_rect.colliderect(0, 0, SCREEN_WIDTH - SCROLL_BAR_WIDTH, SCREEN_HEIGHT):
                pygame.draw.rect(self.screen, LIGHT_GREY if item_rect.collidepoint(pygame.mouse.get_pos()) else WHITE, item_rect)
                text_surface = FONT.render(item, True, BLACK)
                self.screen.blit(text_surface, ((ITEM_WIDTH - text_surface.get_width()) // 2,
                                                y + (ITEM_HEIGHT - text_surface.get_height()) // 2))
            y += ITEM_HEIGHT + ITEM_MARGIN

    def draw_scroll_bar(self):
        scroll_bar_rect = pygame.Rect(ITEM_WIDTH, 0, SCROLL_BAR_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, GREY, scroll_bar_rect)
        scroll_button_rect = pygame.Rect(ITEM_WIDTH, self.scroll_button_y, SCROLL_BAR_WIDTH, self.scroll_button_height)
        pygame.draw.rect(self.screen, WHITE, scroll_button_rect)

    def update_scroll(self):
        scroll_ratio = self.scroll_button_y / (SCREEN_HEIGHT - self.scroll_button_height)
        self.scroll_y = scroll_ratio * (self.total_items_height - SCREEN_HEIGHT)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                if ITEM_WIDTH <= mouse_x <= ITEM_WIDTH + SCROLL_BAR_WIDTH:
                    if self.scroll_button_y <= mouse_y <= self.scroll_button_y + self.scroll_button_height:
                        self.dragging = True
                        self.mouse_offset_y = mouse_y - self.scroll_button_y
                    else:
                        self.scroll_button_y = mouse_y - self.scroll_button_height / 2
                        self.scroll_button_y = max(0, min(self.scroll_button_y, SCREEN_HEIGHT - self.scroll_button_height))
                        self.mouse_offset_y = self.scroll_button_height / 2
                        self.dragging = True
                        self.update_scroll()
                else:
                    y = -self.scroll_y
                    for index, item in enumerate(self.items):
                        item_rect = pygame.Rect(0, y, ITEM_WIDTH, ITEM_HEIGHT)
                        if item_rect.collidepoint(mouse_x, mouse_y):
                            print(f"{item} clicked!")
                            break
                        y += ITEM_HEIGHT + ITEM_MARGIN
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.scroll_button_y = mouse_y - self.mouse_offset_y
                self.scroll_button_y = max(0, min(self.scroll_button_y, SCREEN_HEIGHT - self.scroll_button_height))
                self.update_scroll()
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * SCROLL_SPEED
            self.scroll_y = max(0, min(self.scroll_y, self.total_items_height - SCREEN_HEIGHT))
            scroll_ratio = self.scroll_y / (self.total_items_height - SCREEN_HEIGHT)
            self.scroll_button_y = scroll_ratio * (SCREEN_HEIGHT - self.scroll_button_height)

    def update(self):
        self.screen.fill(BLACK)
        self.draw_items()
        self.draw_scroll_bar()
        pygame.display.flip()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scrollable Items with Scroll Button")

    scrollable_list = ScrollableItemList(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scrollable_list.handle_event(event)
        
        scrollable_list.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
