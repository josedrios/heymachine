import speech_recognition as sr
import pyttsx3

def listen_for_prefix(recognizer, microphone, engine, keyword="hey josie"):
    while True:
        print("Waiting for prefix...")
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10)  
            command = recognizer.recognize_google(audio).lower() 
            print("Phrase:", command)
            
            if keyword in command:
                print("Prefix detected, waiting for command...")
                engine.say("Whats up daddy")
                engine.runAndWait()
                return True  
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            print("ERR: Coulnd not understand/No prefix detected")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

def get_command(recognizer, microphone):
    with microphone as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=10)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("Command:", command)
        return command
    except sr.UnknownValueError:
        print("ERR: Could not understand")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
    return None

def process_command(recognizer, microphone, command):
    print("Processing command:", command)
    command = command.upper()
    print("Processed command:", command)

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()

    while True:
        if listen_for_prefix(recognizer, microphone, engine,keyword="hey josie"):
            command = get_command(recognizer, microphone)
            if command:
                process_command(recognizer, microphone, command)

                
