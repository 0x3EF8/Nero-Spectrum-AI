# NERO AI Assistant v6.0

Nero is a professional Desktop AI Assistant featuring a circular audio spectrum visualizer, powered by Google Gemini AI and Microsoft Edge Neural TTS. It is designed with a modern, frameless UI and "Jarvis-like" aesthetics.

## Features

- **Advanced AI**: Powered by Google's Gemini 2.5 Flash model for intelligent responses.
- **Neural Voice**: Uses Microsoft Edge Neural TTS (Siri/Alexa quality) for natural speech.
- **Visualizer**: Real-time circular audio spectrum visualizer with dynamic color gradients (Idle, Listening, Thinking, Speaking modes).
- **Modern UI**: Custom frameless window with a clean, dark-themed interface.
- **Voice Control**: Wake-word free continuous listening loop.
- **Commands**: 
  - "Play [song]" (YouTube)
  - "Open [site]" (Google, YouTube, GitHub, etc.)
  - "What time is it"
  - General conversation

## Project Structure

The project is organized into modular components for maintainability:

```text
Nero/
├── config/           # Configuration
│   └── settings.py   # Global settings (API Keys, Colors, Dimensions)
├── core/             # Core Application
│   └── app.py        # Main Application Logic & Event Loop
├── modules/          # AI & Logic Modules
│   ├── brain.py      # Gemini AI Integration
│   ├── ears.py       # Speech Recognition (STT)
│   └── voice.py      # Neural Text-to-Speech (TTS)
├── ui/               # User Interface
│   ├── components.py # UI Elements (Title Bar, Chat Panel)
│   └── visualizer.py # Circular Spectrum Visualizer class
├── utils/            # Utilities
│   └── setup.py      # Environment & Logging setup
├── main.py           # Application Entry Point
└── requirements.txt  # Python Dependencies
```

## Installation

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: You may need to install `pyaudio` separately if `SpeechRecognition` fails (use `pipwin install pyaudio` on Windows).*

## Usage

Run the application using the main entry point:

```bash
python main.py
```

## Configuration

1. Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

2. Edit `config/settings.py` to change:
   - `VOICE_NAME`: Pick from 'guy', 'jenny', 'aria', 'davis', 'tony', 'jane'.
   - `VOICE_RATE` / `PITCH`: Adjust speech speed and pitch.
   - `SYSTEM_PROMPT`: The personality of the AI.
   - `WIDTH` / `HEIGHT`: Window dimensions.
   - `COLORS`: UI color scheme.

## Controls

- **Left Click + Drag** on Title Bar to move the window.
- **Minimize (-) / Close (x)** buttons in the custom title bar.
- **ESC** to quit.
