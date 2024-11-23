from openai import OpenAI
import speech_recognition as sr
import os

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something...")
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("API request failed.")

# client = OpenAI()
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Tell me about early astronomy"
#         }
#     ]
# )
# print(completion.choices[0].message.content)

