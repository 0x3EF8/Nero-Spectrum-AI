import psutil
import screen_brightness_control as sbc
from AppOpener import open as app_open, close as app_close
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import win32api
import win32con

class SystemController:
    """
    Handles all low-level system interactions for Nero.
    - Audio (Volume)
    - Media (Play/Pause/Next)
    - Hardware (Brightness, CPU/RAM)
    - Apps (Open/Close)
    """
    
    def __init__(self):
        # We don't init audio here because it's thread-dependent.
        # We will init it on demand in the methods.
        pass

    def _get_volume_interface(self):
        """Helper to get the volume interface for the current thread"""
        try:
            # Initialize COM for this thread
            CoInitialize()
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            return cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            print(f"[System] API Error: {e}")
            return None

    def set_volume(self, level: int):
        """Sets system volume (0-100)"""
        volume = self._get_volume_interface()
        if not volume: return "Audio unavailable"
        
        # Clamp between 0-100
        level = max(0, min(100, level))
        scalar = level / 100.0
        
        volume.SetMasterVolumeLevelScalar(scalar, None)
        return f"Volume set to {level}%"

    def get_volume(self):
        volume = self._get_volume_interface()
        if not volume: return 0
        return int(volume.GetMasterVolumeLevelScalar() * 100)
    
    def adjust_volume(self, change: int):
        """Relative volume change (+10, -20 etc)"""
        current = self.get_volume()
        return self.set_volume(current + change)

    def mute_volume(self):
        volume = self._get_volume_interface()
        if not volume: return
        volume.SetMute(1, None)
        return "System muted"
    
    def unmute_volume(self):
        volume = self._get_volume_interface()
        if not volume: return
        volume.SetMute(0, None)
        return "System unmuted"

    def get_brightness(self):
        try:
            return sbc.get_brightness()[0]
        except:
            return 50 # Default failover

    def set_brightness(self, level: int):
        """Sets generic screen brightness"""
        try:
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except Exception as e:
            return f"Could not set brightness: {e}"

    def media_play_pause(self):
        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "Toggled media playback"

    def media_next(self):
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "Skipped to next track"

    def media_prev(self):
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, 0, 0)
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "Back to previous track"

    def get_system_health(self):
        """Returns string summary of CPU/RAM"""
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        return f"CPU Usage: {cpu}%, RAM Usage: {ram}%"

    def open_app(self, app_name_str):
        """Uses AppOpener to fuzzy match and open app"""
        try:
            # We strip common phrases to help the fuzzy matcher
            clean_name = app_name_str.lower().replace("open ", "").replace("launch ", "").strip()
            app_open(clean_name, match_closest=True, output=False)
            return f"Launching {clean_name}"
        except Exception as e:
            return f"Failed to launch {app_name_str}: {e}"

    def close_app(self, app_name_str):
        try:
             clean_name = app_name_str.lower().replace("close ", "").replace("kill ", "").strip()
             app_close(clean_name, match_closest=True, output=False)
             return f"Closing {clean_name}"
        except:
            # Fallback to older method if AppOpener fails
            return "Could not close app via AppOpener (try generic name)"
