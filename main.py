import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes


def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech output not supported in Colab.")


def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
    except Exception as e:
        print("Could not understand, say that again please...")
        return "None"
    return command.lower()


def run_assistant():
    wish_user()
    while True:
        query = take_command()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com/")

        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com/")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "exit" in query or "bye" in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")


run_assistant()
