import pygame

class DialogBox:
    def __init__(self, screen, title, text, width=400, height=200):
        self.screen = screen
        self.title = title
        self.text = text
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 24)
        self.title_font = pygame.font.SysFont('arial', 28, bold=True)
        self.text_lines = text.split('\n')

        # Calculate dialog box position
        screen_width, screen_height = self.screen.get_size()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Colors
        self.bg_color = (23, 38, 55)
        self.border_color = (233, 200, 68)
        self.text_color = (233, 200, 68)

    def draw(self):
        # Draw the dialog box
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)

        # Render and draw the title
        title_surface = self.title_font.render(self.title, True, self.text_color)
        self.screen.blit(title_surface, (self.x + 20, self.y + 10))

        # Draw a line below the title
        pygame.draw.line(self.screen, self.border_color, (self.x + 20, self.y + 50), (self.x + self.width - 20, self.y + 50), 2)

        # Render and draw the text
        for i, line in enumerate(self.text_lines):
            line_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(line_surface, (self.x + 20, self.y + 60 + i * 30))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_ESCAPE:
                return False

def blitFPS(screen, fontP, FPS_clock,BRIGHTORANGE):
    FPS_title = fontP.render(f"FPS: {FPS_clock.get_fps()}", True, BRIGHTORANGE)
    screen.blit(FPS_title, (10,10))

class Dropdown:
    def __init__(self, x, y, width, height, options, font, bg, tg, sl, hc, default_text="Select an option"):
        self.rect = pygame.Rect(x, y, width, height)
        self.bgcolor = bg
        self.tgcolor = tg
        self.slcolor = sl
        self.hcolor = hc
        self.options = options
        self.font = font
        self.selected = default_text
        self.expanded = False
        self.hovered_option = -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.bgcolor, self.rect)
        text = self.font.render(self.selected, True, self.tgcolor)
        surface.blit(text, (self.rect.x + 10, self.rect.y + 5))

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                color = self.slcolor if i != self.hovered_option else self.hcolor
                pygame.draw.rect(surface, color, option_rect)
                option_text = self.font.render(option, True, self.tgcolor)
                surface.blit(option_text, (option_rect.x + 10, option_rect.y + 5))

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
                        return self.selected
        elif event.type == pygame.MOUSEMOTION:
            if self.expanded:
                self.hovered_option = -1
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.hovered_option = i
                        break

class ScrollableItemList:
    def __init__(self,screen,NUM_ITEMS,ITEM_HEIGHT,ITEM_WIDTH,ITEM_MARGIN,SCREEN_WIDTH,SCROLL_HEIGHT,SCROLL_BAR_WIDTH,FONT,items):
        self.NUM_ITEMS = NUM_ITEMS
        self.ITEM_HEIGHT = ITEM_HEIGHT
        self.ITEM_WIDTH = ITEM_WIDTH
        self.ITEM_MARGIN = ITEM_MARGIN
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCROLL_HEIGHT = SCROLL_HEIGHT
        self.SCROLL_BAR_WIDTH = SCROLL_BAR_WIDTH
        self.FONT = FONT
        self.screen = screen
        self.total_items_height = NUM_ITEMS * (ITEM_HEIGHT + ITEM_MARGIN) - ITEM_MARGIN
        self.scroll_y = 0
        self.scroll_button_height = max(SCROLL_HEIGHT / self.total_items_height * SCROLL_HEIGHT, 20)
        self.scroll_button_y = 0
        self.dragging = False
        self.SCROLL_SPEED = 20
        self.mouse_offset_y = 0
        self.items = items

    def draw_items(self,FOCUS_COLOR,BTN_COLOR,TXT_COLOR,ON_COLOR,ADJX,CELL_SIZE,selected,player_state,LIFE_NAME):
        y = -self.scroll_y
        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(0, y, self.ITEM_WIDTH, self.ITEM_HEIGHT)
            color = FOCUS_COLOR if item_rect.collidepoint(pygame.mouse.get_pos()) else BTN_COLOR
            if item == selected:
                color = ON_COLOR
            if item_rect.colliderect(0, 0, self.SCREEN_WIDTH - self.SCROLL_BAR_WIDTH, self.SCROLL_HEIGHT):
                pygame.draw.rect(self.screen, TXT_COLOR, item_rect.move(ADJX,3))
                pygame.draw.rect(self.screen, color, item_rect.move(ADJX,0))
                
                try:
                    if player_state[0][LIFE_NAME[item]] == 1:
                        for i in range(len(item.split())):
                            text_surface = self.FONT.render(item.split()[i], True, TXT_COLOR)
                            self.screen.blit(text_surface, ((self.ITEM_WIDTH - text_surface.get_width()) // 2+ADJX,
                                                        y + (self.ITEM_HEIGHT - text_surface.get_height()) // 2 + (i - (len(item.split()) - 1) / 2) * CELL_SIZE * 4))
                except:
                    if item == "Buckaroo":
                        if player_state[0][-1] == 1:
                            for i in range(len(item.split())):
                                text_surface = self.FONT.render(item.split()[i], True, TXT_COLOR)
                                self.screen.blit(text_surface, ((self.ITEM_WIDTH - text_surface.get_width()) // 2+ADJX,
                                                            y + (self.ITEM_HEIGHT - text_surface.get_height()) // 2 + (i - (len(item.split()) - 1) / 2) * CELL_SIZE * 4))
                    else:
                        for i in range(len(item.split())):
                            text_surface = self.FONT.render(item.split()[i], True, TXT_COLOR)
                            self.screen.blit(text_surface, ((self.ITEM_WIDTH - text_surface.get_width()) // 2+ADJX,
                                                        y + (self.ITEM_HEIGHT - text_surface.get_height()) // 2 + (i - (len(item.split()) - 1) / 2) * CELL_SIZE * 4))
            y += self.ITEM_HEIGHT + self.ITEM_MARGIN

    def draw_scroll_bar(self,SCROLL_BTN_COLOR,SCROLL_BAR_COLOR,ADJX):
        scroll_bar_rect = pygame.Rect(self.ITEM_WIDTH, 0, self.SCROLL_BAR_WIDTH, self.SCROLL_HEIGHT)
        pygame.draw.rect(self.screen, SCROLL_BAR_COLOR, scroll_bar_rect.move(ADJX,0))
        scroll_button_rect = pygame.Rect(self.ITEM_WIDTH, self.scroll_button_y, self.SCROLL_BAR_WIDTH, self.scroll_button_height)
        pygame.draw.rect(self.screen, SCROLL_BTN_COLOR, scroll_button_rect.move(ADJX,0))

    def update_scroll(self):
        scroll_ratio = self.scroll_button_y / (self.SCROLL_HEIGHT - self.scroll_button_height)
        self.scroll_y = scroll_ratio * (self.total_items_height - self.SCROLL_HEIGHT)

    def handle_event(self, event,selected):
        clicked = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                
                if mouse_y >= self.SCROLL_HEIGHT:
                    return clicked
                
                if self.ITEM_WIDTH <= mouse_x <= self.ITEM_WIDTH + self.SCROLL_BAR_WIDTH:
                    if self.scroll_button_y <= mouse_y <= self.scroll_button_y + self.scroll_button_height:
                        clicked = 2
                        self.dragging = True
                        self.mouse_offset_y = mouse_y - self.scroll_button_y
                    else:
                        clicked = 2
                        self.scroll_button_y = mouse_y - self.scroll_button_height / 2
                        self.scroll_button_y = max(0, min(self.scroll_button_y, self.SCROLL_HEIGHT - self.scroll_button_height))
                        self.mouse_offset_y = self.scroll_button_height / 2
                        self.dragging = True
                        self.update_scroll()
                else:
                    y = -self.scroll_y
                    for index, item in enumerate(self.items):
                        item_rect = pygame.Rect(0, y, self.ITEM_WIDTH, self.ITEM_HEIGHT)
                        if item_rect.collidepoint(mouse_x, mouse_y):
                            if item != selected and clicked in [1,2]:
                                clicked = item
                            else:
                                clicked = None
                            break
                        y += self.ITEM_HEIGHT + self.ITEM_MARGIN
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                clicked = 2
                mouse_x, mouse_y = event.pos
                self.scroll_button_y = mouse_y - self.mouse_offset_y
                self.scroll_button_y = max(0, min(self.scroll_button_y, self.SCROLL_HEIGHT - self.scroll_button_height))
                self.update_scroll()
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * self.SCROLL_SPEED
            self.scroll_y = max(0, min(self.scroll_y, self.total_items_height - self.SCROLL_HEIGHT))
            scroll_ratio = self.scroll_y / (self.total_items_height - self.SCROLL_HEIGHT)
            self.scroll_button_y = scroll_ratio * (self.SCROLL_HEIGHT - self.scroll_button_height)
        return clicked

    def update(self,FOCUS_COLOR, BTN_COLOR, TXT_COLOR,SCROLL_BTN_COLOR, SCROLL_BAR_COLOR,ON_COLOR,ADJX,CELL_SIZE,selected,player_state,LIFE_NAME):
        self.draw_items(FOCUS_COLOR, BTN_COLOR, TXT_COLOR,ON_COLOR,ADJX,CELL_SIZE,selected,player_state,LIFE_NAME)
        self.draw_scroll_bar(SCROLL_BTN_COLOR, SCROLL_BAR_COLOR,ADJX)