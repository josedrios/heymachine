import os
import tkinter
from openai import OpenAI
import speech_recognition as sr

# pip3.11 install ...
def listen_for_prefix(recognizer, microphone, prefixes):
    while True:
        print("State: Waiting...")
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=20)  
            command = recognizer.recognize_google(audio).lower() 
            print(f"State: Text received :'{command}'")
            
            if command in prefixes:
                print("State\033[92m: Prefix detected\033[0m")
                return True  
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            print("State: Not Understandable/Timeout Error")
        except sr.RequestError as e:
            print("State: {e}")

def get_command(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=12)
        print("Listening for command...")
    try:
        command = recognizer.recognize_google(audio).lower()
        print("Command:", command)
        return command
    except sr.UnknownValueError:
        print("ERR: Could not understand")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
    return None

def process_command(client, command):
    print("Processing command:", command)
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ]
    )
    print("Response:\n", completion.choices[0].message.content)

if __name__ == "__main__":
    client = OpenAI()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    m = tkinter.Tk()
    m.mainloop()

    prefixes = [
        'yo machine',
        'hello machine',
        'hey machine',
        'hi machine',
        'howdy machine',
        'sup machine',
        # Common misinterpretations
        'time machine',
        'play machine',
        'your machine',
        'neo machine',
        'slot machine',
        ]

    while True:
        if listen_for_prefix(recognizer, microphone, prefixes):
            command = get_command(recognizer, microphone)
            if command:
                process_command(client, command)

                
