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

vosk_model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(vosk_model, 16000)

def take_command():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "")
            if command != "":
                print(f"You said: {command}")
                stream.stop_stream()
                stream.close()
                p.terminate()
                return command.lower()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")

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
            speak("Let me think...")
            response = ask_llm(query)
            speak(response)
            if "exit" in response or "bye" in response:
                speak("Goodbye! Have a nice day!")
                break


run_assistant()
