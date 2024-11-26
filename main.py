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
    main_color = '#f15e22'
    
    # TKINTER CODE
    window = tkinter.Tk()
    window.title('Hey Machine')

    window.geometry("400x600")
    window.minsize(400,600)
    window.maxsize(600, 10000)

    window.configure(bg=main_color)

    tkinter.Label(window, bg=main_color, text="Hey Machine", fg='black').pack(pady = 10)
    container = tkinter.Frame(window, height=400, bg='white', bd=2, relief='solid')
    container.pack(fill='x', pady=10, padx=40)

    response = tkinter.Canvas(container, bg='white', height=400, highlightthickness=0)
    response.pack(side="left", fill='both', expand=True)

    # Add a vertical scrollbar alongside the canvas
    scrollbar = tkinter.Scrollbar(container, orient=tkinter.VERTICAL, command=response.yview)
    scrollbar.pack(side="right", fill=tkinter.Y)

    # Configure canvas and scrollbar
    response.configure(yscrollcommand=scrollbar.set)
    response.bind('<Configure>', lambda e: response.configure(scrollregion=response.bbox('all')))

    # Create a frame inside the canvas for content
    frame = tkinter.Frame(response, bg='white')
    response.create_window((10, 10), window=frame, anchor='nw')

    # Add content to the frame
    for i in range(50):  # Add multiple labels to create overflow
        tkinter.Label(frame, text=f"Line {i+1}", bg="red").pack(anchor="w", pady=2)

    window.mainloop()

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

                
