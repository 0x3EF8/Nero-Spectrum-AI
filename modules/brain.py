import google.generativeai as genai
from config.settings import Config
from modules.system import SystemController

class Brain:
    """
    The intelligence layer. Connects to Gemini and manages system tools.
    """
    
    def __init__(self):
        # Fire up the system controller
        self.sys = SystemController()
        
        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_KEY)
        
        # Define the tools we want to give the AI access to
        self.tools = [
            self.sys.set_volume,
            self.sys.adjust_volume,
            self.sys.mute_volume,
            self.sys.unmute_volume,
            self.sys.set_brightness,
            self.sys.media_play_pause,
            self.sys.media_next,
            self.sys.media_prev,
            self.sys.get_system_health,
            self.sys.open_app,
            self.sys.close_app
        ]
        
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            system_instruction=Config.SYSTEM_PROMPT,
            tools=self.tools
        )
        
        # Keep chat history for context
        self.chat_session = self.model.start_chat(enable_automatic_function_calling=True)

    def think(self, user_text, visualizer=None):
        """
        Processes user input, calls tools if needed, and returns a text response.
        """
        if visualizer:
            visualizer.mode = "thinking"
            
        try:
            # Send message to Gemini
            response = self.chat_session.send_message(user_text)
            return response.text
        except Exception as e:
            print(f"Brain Error: {e}")
            return "I'm having trouble connecting to my neural network, Sir."
