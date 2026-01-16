import speech_recognition as sr

class Ears:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # threshold for background noise
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
    
    def listen(self, visualizer=None):
        if visualizer:
            visualizer.set_mode("listening")
        try:
            with sr.Microphone() as source:
                # adjust for room noise quickly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=12)
                if visualizer:
                    visualizer.set_mode("thinking")
                # ship it to google for recognition
                text = self.recognizer.recognize_google(audio)
                return text.lower().strip()
        except:
            return None
        finally:
            if visualizer:
                visualizer.set_mode("idle")
