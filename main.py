import os
import tkinter
import threading
import time
from openai import OpenAI
import speech_recognition as sr

def create_gui(main_color):
    window = tkinter.Tk()
    window.title('Hey Machine')

    window.geometry("400x600")
    window.minsize(400,600)
    window.maxsize(600, 10000)

    window.configure(bg=main_color)

    tkinter.Label(window, bg=main_color, text="Hey Machine", fg='black').pack(pady = 10)

    navbar = tkinter.Frame(window, bg=main_color, height = 30)
    navbar.pack(fill='x', padx=40)

    previous = tkinter.Button(
        navbar, 
        text='<', 
        bg=main_color, 
        bd=0, 
        highlightthickness=0, 
        highlightbackground=main_color,  
    )
    previous.grid(row=0, column=0)

    next = tkinter.Button(
        navbar,
        text='>', 
        bg=main_color, 
        bd=0, 
        highlightthickness=0, 
        highlightbackground=main_color,  
    )
    next.grid(row=0, column=1)

    play = tkinter.Button(
        navbar,
        text='▶', 
        command = create_thread,
        bg=main_color, 
        bd=0, 
        highlightthickness=0, 
        highlightbackground=main_color,  
    )
    play.grid(row=0, column=2)

    container = tkinter.Frame(window, height=400, bg='white', bd=2, relief='solid')
    container.pack(fill='x', padx=40)

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

    return window

def create_thread():
    print("Starting thread...")
    thread = threading.Thread(target=main())
    thread.daemon = True
    thread.start()

def main():
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
            {"role": "system", "content": "You are a helpful assistant who gives slight concise answers."},
            {"role": "user", "content": command}
        ]
    )
    response = completion.choices[0].message.content
    print("Response:\n", response)

if __name__ == "__main__":
    client = OpenAI()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    color = '#f15e22'
    window = create_gui(color)
    window.mainloop()
                
