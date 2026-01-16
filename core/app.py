import pygame
import threading
import datetime
import pywhatkit
import webbrowser
import ctypes
import ctypes.wintypes

from config.settings import Config
from ui.visualizer import CircularSpectrum
from ui.components import UIComponents
from modules.voice import Voice
from modules.ears import Ears
from modules.brain import Brain

class NeroAI:
    def __init__(self):
        pygame.init()
        
        # no frame because we want it to look futuristic
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption(Config.TITLE)
        
        # grabbing the window handle so we can minimize it properly later
        self.hwnd = pygame.display.get_wm_info()['window']
        
        self.clock = pygame.time.Clock()
        
        # window dragging stuff
        self.dragging = False
        self.drag_offset = (0, 0)
        
        # load up some fonts
        self.fonts = {
            'title_bar': pygame.font.Font(None, 18),
            'btn': pygame.font.Font(None, 22),
            'chat': pygame.font.Font(None, 22),
            'chat_small': pygame.font.Font(None, 18),
            'chat_header': pygame.font.Font(None, 26)
        }
        
        # put the visualizer in the middle of the left panel
        center_x = Config.VISUALIZER_WIDTH // 2
        center_y = Config.TITLE_BAR_HEIGHT + (Config.HEIGHT - Config.TITLE_BAR_HEIGHT) // 2
        
        self.visualizer = CircularSpectrum(self.screen, center_x, center_y)
        self.ui = UIComponents(self.screen, self.fonts)
        self.ears = Ears()
        self.brain = Brain()
        
        # store the chat history here
        self.conversation = []  # List of {'role': 'user'/'nero', 'text': '...', 'time': '...'}
        self.scroll_offset = 0
        self.max_visible_messages = 12
        
        # app state
        self.running = True
        self.status = "Initializing..."
        self.message = ""
        self.user_text = ""
        self.listening = False
        self.chat_visible = True
        self.mouse_pos = (0, 0)
        
    def toggle_chat(self):
        """Hides or shows the chat panel and resizes the window"""
        self.chat_visible = not self.chat_visible
        new_width = Config.WIDTH if self.chat_visible else Config.VISUALIZER_WIDTH
        self.screen = pygame.display.set_mode((new_width, Config.HEIGHT), pygame.NOFRAME)
        # Re-init UI to update hitbox positions for the new size
        self.ui = UIComponents(self.screen, self.fonts)
        
    def minimize_window(self):
        """Uses windows api to minimize the window since we don't have a normal title bar"""
        ctypes.windll.user32.ShowWindow(self.hwnd, 6)  # SW_MINIMIZE = 6
    
    def add_message(self, role, text):
        """Pushes a new message to the list"""
        timestamp = datetime.datetime.now().strftime('%H:%M')
        self.conversation.append({
            'role': role,
            'text': text,
            'time': timestamp
        })
        # keeps the chat scrolled to the bottom
        if len(self.conversation) > self.max_visible_messages:
            self.scroll_offset = len(self.conversation) - self.max_visible_messages
            
    def process_command(self, text):
        """Decides what to do with what you said"""
        self.user_text = text
        self.add_message('user', text)
        
        if any(w in text for w in ['goodbye', 'bye', 'exit', 'quit']):
            self.status = "Speaking..."
            self.message = "Goodbye, Sir. It was my pleasure."
            self.add_message('nero', self.message)
            Voice.speak(self.message, self.visualizer)
            self.running = False
            return
        
        if 'play ' in text:
            song = text.replace('play', '').strip()
            self.status = "Speaking..."
            self.message = f"Playing {song} for you, Sir."
            self.add_message('nero', self.message)
            Voice.speak(self.message, self.visualizer)
            pywhatkit.playonyt(song)
            return
        
        if any(w in text for w in ['what time', 'time is it']):
            current = datetime.datetime.now().strftime('%I:%M %p')
            self.status = "Speaking..."
            self.message = f"The time is {current}, Sir."
            self.add_message('nero', self.message)
            Voice.speak(self.message, self.visualizer)
            return
        
        sites = {'youtube': 'https://youtube.com', 'google': 'https://google.com',
                 'github': 'https://github.com', 'facebook': 'https://facebook.com'}
        for site, url in sites.items():
            if site in text and 'open' in text:
                self.status = "Speaking..."
                self.message = f"Opening {site} for you, Sir."
                self.add_message('nero', self.message)
                Voice.speak(self.message, self.visualizer)
                webbrowser.open(url)
                return
        
        self.status = "Thinking..."
        response = self.brain.think(text, self.visualizer)
        self.status = "Speaking..."
        self.message = response
        self.add_message('nero', response)
        Voice.speak(response, self.visualizer)
    
    def listen_thread(self):
        """The ear thread that runs in the background"""
        self.status = "Listening..."
        text = self.ears.listen(self.visualizer)
        if text:
            self.process_command(text)
        self.status = "Ready"
        self.listening = False
    
    def greet(self):
        """Say hello when we start up"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning, Sir"
        elif hour < 18:
            greeting = "Good afternoon, Sir"
        else:
            greeting = "Good evening, Sir"
        
        self.message = f"{greeting}. Nero online and ready to assist."
        self.add_message('nero', self.message)
        self.status = "Speaking..."
        Voice.speak(self.message, self.visualizer)
        self.status = "Ready"
    
    def run(self):
        """The main game loop"""
        threading.Thread(target=self.greet, daemon=True).start()
        
        while self.running:
            dt = self.clock.tick(Config.FPS) / 1000.0
            self.mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Close button
                        if self.ui.close_rect.collidepoint(event.pos):
                            self.running = False
                        # Minimize button
                        elif self.ui.min_rect.collidepoint(event.pos):
                            self.minimize_window()
                        # Chat toggle button
                        elif self.ui.chat_rect.collidepoint(event.pos):
                            self.toggle_chat()
                        # Title bar drag
                        elif self.ui.title_rect.collidepoint(event.pos):
                            self.dragging = True
                            mouse_x, mouse_y = event.pos
                            rect = ctypes.wintypes.RECT()
                            ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.byref(rect))
                            self.drag_offset = (mouse_x, mouse_y)
                            
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                        
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # Move the window
                        cursor_pos = ctypes.wintypes.POINT()
                        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor_pos))
                        new_x = cursor_pos.x - self.drag_offset[0]
                        new_y = cursor_pos.y - self.drag_offset[1]
                        ctypes.windll.user32.SetWindowPos(self.hwnd, 0, new_x, new_y, 0, 0, 0x0001)
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            if not self.listening and "Ready" in self.status:
                self.listening = True
                threading.Thread(target=self.listen_thread, daemon=True).start()
            
            self.visualizer.update(dt)
            
            # Render everything
            self.screen.fill(Config.BG_COLOR)
            self.visualizer.draw()
            self.ui.draw_title_bar(self.mouse_pos)
            
            # Only draw chat if it's visible
            if self.chat_visible:
                self.ui.draw_chat_panel(self.conversation, self.scroll_offset, self.max_visible_messages, self.status)
            
            pygame.display.flip()
        
        pygame.quit()
