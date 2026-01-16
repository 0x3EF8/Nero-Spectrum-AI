import os
import time
import pygame
import asyncio
import tempfile
from config.settings import Config

class Voice:
    """
    Handles the talking part.
    Using Edge TTS because it sounds way better than the default robot voice windows has.
    """
    # These are the microsoft azure neural voices. They sound pretty realistic.
    VOICES = {
        'guy': 'en-US-GuyNeural',           # Standard male voice
        'jenny': 'en-US-JennyNeural',       # Standard female voice
        'aria': 'en-US-AriaNeural',         # A bit more expressive
        'davis': 'en-US-DavisNeural',       # Calm dude
        'tony': 'en-US-TonyNeural',         # Friendly dude
        'jane': 'en-US-JaneNeural',         # Warm female voice
    }
    
    # sticking with what you set in settings.py
    try:
        CURRENT_VOICE = VOICES[Config.VOICE_NAME]
    except KeyError:
        print(f"Warning: Voice '{Config.VOICE_NAME}' not found. Defaulting to Jenny.")
        CURRENT_VOICE = VOICES['jenny']
    
    @staticmethod
    def speak(text, visualizer=None):
        """Actually generates the mp3 and plays it"""
        if visualizer:
            visualizer.set_mode("speaking")
        try:
            import edge_tts
            
            async def _generate_speech():
                # Talk to the edge tts api
                communicate = edge_tts.Communicate(
                    text=text,
                    voice=Voice.CURRENT_VOICE,
                    rate=Config.VOICE_RATE,
                    volume=Config.VOICE_VOLUME,
                    pitch=Config.VOICE_PITCH
                )
                
                # dump it to a temp file so we can play it
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_path = temp_file.name
                temp_file.close()
                
                await communicate.save(temp_path)
                return temp_path
            
            # run the async function
            audio_path = asyncio.run(_generate_speech())
            
            # play it using pygame mixer
            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # wait until it's done talking
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # clean up the temp file so we don't fill up the drive
            pygame.mixer.music.unload()
            try:
                os.remove(audio_path)
            except:
                pass
                
        except Exception as e:
            # if internet is down or something breaks, fall back to the oldschool windows voice
            try:
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                voices = speaker.GetVoices()
                for i in range(voices.Count):
                    if "David" in voices.Item(i).GetDescription():
                        speaker.Voice = voices.Item(i)
                        break
                speaker.Rate = 1
                speaker.Speak(text)
            except:
                pass
        finally:
            if visualizer:
                visualizer.set_mode("idle")
