import pygame
from config.settings import Config

class UIComponents:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        
        # Grab width dynamically so we can resize the window
        width = screen.get_width()
        
        # Hitboxes for the buttons
        self.btn_size = 30
        self.close_rect = pygame.Rect(width - self.btn_size, 0, self.btn_size, Config.TITLE_BAR_HEIGHT)
        self.min_rect = pygame.Rect(width - self.btn_size * 2, 0, self.btn_size, Config.TITLE_BAR_HEIGHT)
        # Button to hide the chat
        self.chat_rect = pygame.Rect(width - self.btn_size * 3, 0, self.btn_size, Config.TITLE_BAR_HEIGHT)
        self.title_rect = pygame.Rect(0, 0, width - self.btn_size * 3, Config.TITLE_BAR_HEIGHT)

    def draw_title_bar(self, mouse_pos):
        """Renders that custom top bar since we turned off the OS one"""
        width = self.screen.get_width()
        
        # Background
        pygame.draw.rect(self.screen, Config.TITLE_BG, (0, 0, width, Config.TITLE_BAR_HEIGHT))
        
        # Little border line at the bottom
        pygame.draw.line(self.screen, (30, 30, 50), (0, Config.TITLE_BAR_HEIGHT - 1), 
                        (width, Config.TITLE_BAR_HEIGHT - 1), 1)
        
        # Fake icon thingy on the left
        pygame.draw.circle(self.screen, (0, 255, 255), (15, Config.TITLE_BAR_HEIGHT // 2), 5)
        pygame.draw.circle(self.screen, (0, 200, 200), (15, Config.TITLE_BAR_HEIGHT // 2), 3)
        
        # App Title
        title = self.fonts['title_bar'].render("NERO", True, (100, 100, 120))
        self.screen.blit(title, (28, Config.TITLE_BAR_HEIGHT // 2 - title.get_height() // 2))
        
        # Chat toggle button logic
        chat_hover = self.chat_rect.collidepoint(mouse_pos)
        if chat_hover:
            pygame.draw.rect(self.screen, Config.MIN_HOVER, self.chat_rect)
        # Draw a little bubble icon
        cx, cy = self.chat_rect.centerx, self.chat_rect.centery
        chat_color = (150, 150, 170) if not chat_hover else (255, 255, 255)
        pygame.draw.rect(self.screen, chat_color, (cx - 6, cy - 5, 12, 10), 1)
        pygame.draw.line(self.screen, chat_color, (cx - 2, cy + 5), (cx + 2, cy + 5), 1) # simple detail
        
        # Minimize button logic
        min_hover = self.min_rect.collidepoint(mouse_pos)
        if min_hover:
            pygame.draw.rect(self.screen, Config.MIN_HOVER, self.min_rect)
        # Draw the little line
        line_y = Config.TITLE_BAR_HEIGHT // 2
        pygame.draw.line(self.screen, (150, 150, 170) if not min_hover else (255, 255, 255),
                        (self.min_rect.x + 10, line_y), (self.min_rect.x + 20, line_y), 2)
        
        # Close button logic
        close_hover = self.close_rect.collidepoint(mouse_pos)
        if close_hover:
            pygame.draw.rect(self.screen, Config.CLOSE_HOVER, self.close_rect)
        # Draw the X
        x_color = (150, 150, 170) if not close_hover else (255, 255, 255)
        cx, cy = self.close_rect.centerx, self.close_rect.centery
        pygame.draw.line(self.screen, x_color, (cx - 5, cy - 5), (cx + 5, cy + 5), 2)
        pygame.draw.line(self.screen, x_color, (cx + 5, cy - 5), (cx - 5, cy + 5), 2)

    def draw_chat_panel(self, conversation, scroll_offset, max_visible_messages, status):
        """Draws the chat history and the status pill at the bottom"""
        panel_x = Config.VISUALIZER_WIDTH
        panel_y = Config.TITLE_BAR_HEIGHT
        panel_width = Config.CHAT_WIDTH
        panel_height = Config.HEIGHT - Config.TITLE_BAR_HEIGHT
        
        # Background rect
        pygame.draw.rect(self.screen, Config.CHAT_BG, 
                        (panel_x, panel_y, panel_width, panel_height))
        
        # Vertical divider line
        pygame.draw.line(self.screen, (30, 30, 50), 
                        (panel_x, panel_y), (panel_x, Config.HEIGHT), 2)
        
        # "CONVERSATION" header
        header_text = self.fonts['chat_header'].render("CONVERSATION", True, (80, 80, 100))
        self.screen.blit(header_text, (panel_x + 20, panel_y + 15))
        
        # Line under header
        pygame.draw.line(self.screen, (30, 30, 50),
                        (panel_x + 15, panel_y + 45), (panel_x + panel_width - 15, panel_y + 45), 1)
        
        # Start calculating message positions
        msg_start_y = panel_y + 60
        msg_height = 45
        
        # Only show what fits
        visible_messages = conversation[scroll_offset:scroll_offset + max_visible_messages]
        
        for i, msg in enumerate(visible_messages):
            y_pos = msg_start_y + i * msg_height
            
            if y_pos + msg_height > Config.HEIGHT - 20:
                break
            
            # Pick colors based on who is talking
            if msg['role'] == 'user':
                # User (You)
                color = Config.CHAT_USER_ACCENT
                prefix = "You"
                bg_color = Config.CHAT_USER_BG
            else:
                # The AI (Nero)
                color = Config.CHAT_NERO_ACCENT
                prefix = "Nero"
                bg_color = Config.CHAT_NERO_BG
            
            # Draw bubble
            msg_rect = pygame.Rect(panel_x + 10, y_pos, panel_width - 20, msg_height - 5)
            pygame.draw.rect(self.screen, bg_color, msg_rect, border_radius=8)
            
            # Little accent strip on the left
            pygame.draw.line(self.screen, color,
                           (panel_x + 12, y_pos + 5), (panel_x + 12, y_pos + msg_height - 10), 3)
            
            # Name and timestamp
            name_text = self.fonts['chat_small'].render(f"{prefix}  •  {msg['time']}", True, color)
            self.screen.blit(name_text, (panel_x + 22, y_pos + 5))
            
            # Actual text (chopped if too long)
            max_chars = 45
            display_text = msg['text'][:max_chars] + "..." if len(msg['text']) > max_chars else msg['text']
            msg_text = self.fonts['chat_small'].render(display_text, True, Config.CHAT_TEXT)
            self.screen.blit(msg_text, (panel_x + 22, y_pos + 24))
        
        # Status pill at the bottom
        status_y = Config.HEIGHT - 35
        pygame.draw.rect(self.screen, (20, 20, 35),
                        (panel_x + 10, status_y, panel_width - 20, 25), border_radius=5)
        
        # Status dot color and text
        if "Listen" in status:
            dot_color = (0, 255, 150)
            status_text = "Listening..."
        elif "Speak" in status:
            dot_color = (255, 100, 200)
            status_text = "Speaking..."
        elif "Think" in status:
            dot_color = (150, 100, 255)
            status_text = "Thinking..."
        else:
            dot_color = (0, 255, 255)
            status_text = "Ready"
        
        # draw the dot manually so we don't depend on fonts having special chars
        pygame.draw.circle(self.screen, dot_color, (panel_x + 25, status_y + 12), 4)
        
        status_render = self.fonts['chat_small'].render(status_text, True, dot_color)
        self.screen.blit(status_render, (panel_x + 38, status_y + 5))
