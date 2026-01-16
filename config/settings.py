import os
from dotenv import load_dotenv

# Load env vars from .env file
load_dotenv()

class Config:
    WIDTH = 950
    HEIGHT = 650  # made it a bit taller for the header
    VISUALIZER_WIDTH = 500  # visualizer sits on the left
    CHAT_WIDTH = 450  # text chat goes on the right
    FPS = 60
    TITLE = "NERO"
    TITLE_BAR_HEIGHT = 35  # custom header height
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    TITLE_BG = (15, 15, 25)  # dark blue-ish for the top bar
    CHAT_BG = (12, 12, 20)   # slightly lighter for the chat area
    CLOSE_HOVER = (232, 17, 35)  # making it red when you hover close
    MIN_HOVER = (50, 50, 70)  # slight highlight for minimize
    
    # UI Colors
    CHAT_USER_ACCENT = (0, 200, 150)
    CHAT_NERO_ACCENT = (0, 200, 255)
    CHAT_USER_BG = (20, 35, 30)
    CHAT_NERO_BG = (20, 30, 40)
    CHAT_TEXT = (180, 180, 200)
    
    # APP
    BG_COLOR = (5, 5, 15)
    
    # AI Stuff
    # Grabs the key from your .env file so you don't leak it on github lol
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash"
    SYSTEM_PROMPT = """You are NERO, an advanced AI assistant like JARVIS.
You are sophisticated and speak elegantly. Address user as "Sir" occasionally.
Keep responses concise (1-2 sentences) for voice. You ARE Nero."""

    # Voice Settings
    # Pick one: 'guy', 'jenny', 'aria', 'davis', 'tony', 'jane'
    VOICE_NAME = 'jenny'
    VOICE_RATE = "+25%"  # Speed: +0% is normal, +25% is snappy
    VOICE_VOLUME = "+0%" # Volume: +0% is default
    VOICE_PITCH = "+0Hz" # Pitch: +0Hz is default
