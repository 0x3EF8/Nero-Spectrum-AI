from utils.setup import setup_environment
from core.app import NeroAI

if __name__ == "__main__":
    setup_environment()
    try:
        nero = NeroAI()
        nero.run()
    except Exception as e:
        # if it crashes, print why
        print(f"Error: {e}")
