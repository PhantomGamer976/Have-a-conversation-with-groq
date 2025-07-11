import keyboard
import os
from groq import Groq
import pyttsx3
import speech_recognition as sr

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    api_key = "THE_API_KEY_HERE"  # Replace with your actual API key
    client = Groq(api_key=api_key)
    personality = "PUT YOUR PERSONALITY HERE. This is the personality of the AI assistant." 
    
                    

    print("Press 'q' to start listening, or 'esc' to quit.")
    while True:
        if keyboard.is_pressed('q'):
            print("Key 'q' pressed - starting to listen.")
            user_input = listen_to_speech()
            if user_input is None:
                continue
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": personality},
                    {"role": "user", "content": user_input}
                ],
                model="llama3-8b-8192",
            )

            ai_response = chat_completion.choices[0].message.content
            print(f"AI says: {ai_response}")
            speak_text(ai_response)

            while keyboard.is_pressed('q'):
                pass

        if keyboard.is_pressed('esc'):
            print("Escape pressed, exiting.")
            break


main()
