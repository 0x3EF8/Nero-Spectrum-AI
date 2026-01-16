# Nero AI

A frameless desktop AI assistant featuring a reactive audio spectrum visualizer, powered by Google Gemini."

## What it does

- **Smart Conversation**: It uses Gemini so you can chat with it about almost anything.
- **Natural Voice**: I hooked up Microsoft Edge's TTS so it sounds pretty realistic, not robotic.
- **Audio Visualizer**: The circle in the middle dances to the music or voice. I spent some time tuning the physics so it feels satisfying to watch! 
- **Modern Look**: It's just a simple dark window without the usual borders.
- **Helpful Commands**:
  - "Play [song]" (It opens YouTube for you)
  - "Open [site]" (Like Google or GitHub)
  - "What time is it"
  - Or just say "Hello" and chat!

## How it's built

I tried to keep the code organized so it's easy to understand:

```text
Nero/
├── config/           # Where all the settings live (colors, keys)
├── core/             # The main loop that runs everything
├── modules/          # The brains (AI) and voice (TTS) logic
├── ui/               # The visuals (Drawing the circle and window)
├── utils/            # Boring setup stuff
└── main.py           # Start here!
```

## How to run it

If you want to try it out:

1. You'll need Python 3.10 or newer.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a free API key from Google AI Studio and put it in a `.env` file:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
4. Run it:
   ```bash
   python main.py
   ```

Feel free to break it or make it better! Controls are simple:
- Drag the title bar to move it around.
- Click the speech bubble to hide the chat.
- ESC to quit if needed.

Enjoy!
