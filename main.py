import datetime
import json
import os
import wave
import webbrowser

import pyaudio
import pyjokes
import wikipedia
from transformers import AutoModelForCausalLM, AutoTokenizer
from TTS.api import TTS
from vosk import KaldiRecognizer, Model

tts = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False
)


def speak(text):
    print(f"Assistant: {text}")
    tts.tts_to_file(text=text, file_path="output.wav")
    os.system("aplay output.wav")


# Initialize DistilGPT2
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")


def ask_llm(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs, max_new_tokens=100, pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


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
        command = recognizer.recognize_google(audio, language="en-in")
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
