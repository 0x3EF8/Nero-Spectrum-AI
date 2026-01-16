from google import genai
from config.settings import Config

class Brain:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=Config.GEMINI_KEY)
            self.ready = True
            self.history = []  # keeping track of what we said
        except Exception as e:
            print(f"Brain init error: {e}")
            self.ready = False
    
    def think(self, prompt, visualizer=None):
        if visualizer:
            visualizer.set_mode("thinking")
        if not self.ready:
            return "My AI systems are offline."
        try:
            # remember what the user said
            self.history.append(f"User: {prompt}")
            
            # keep the context short so we don't blow up the context window/costs
            recent_history = self.history[-6:] if len(self.history) > 6 else self.history
            context = "\n".join(recent_history)
            full_prompt = f"{Config.SYSTEM_PROMPT}\n\n{context}\nNero:"
            
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=full_prompt
            )
            
            result = response.text.strip()
            self.history.append(f"Nero: {result}")
            return result
        except Exception as e:
            print(f"Brain think error: {e}")
            # simple fallback if the main request fails
            try:
                response = self.client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=f"You are Nero, an AI assistant. Respond briefly to: {prompt}"
                )
                return response.text.strip()
            except Exception as e2:
                print(f"Brain fallback error: {e2}")
                return f"I heard you say: {prompt}. My AI connection is having issues."
