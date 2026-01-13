import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize the tools
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    # Initialize command as an empty string to avoid UnboundLocalError
    command = "" 
    try:
        with sr.Microphone() as source:
            print('Listening...')
            # Adjust for ambient noise for better accuracy
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(f"User said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Network error.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return command

def run_alexa():
    command = take_command()
    
    # Check if command is empty before processing
    if not command:
        return

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk("I couldn't find any information on that person.")
        except wikipedia.exceptions.DisambiguationError:
            talk("There are too many results for that. Can you be more specific?")
            
    elif 'date' in command:
        talk('sorry, I have a headache')
        
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
        
    elif 'joke' in command:
        talk(pyjokes.get_joke())
        
    else:
        talk('Please say the command again.')
        
while True:
    run_alexa()
