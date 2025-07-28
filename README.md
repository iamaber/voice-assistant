# Voice Assistant using DistilGPT2 + Coqui TTS + Vosk (Offline STT)

This is an offline voice assistant built with lightweight components:
- 🗣️ **Vosk** for Offline Speech Recognition.
- 🧠 **DistilGPT2** for lightweight conversational AI.
- 🔊 **Coqui TTS** for realistic text-to-speech responses.
- Additional features like Wikipedia search, opening websites, telling jokes, etc.

---

## 🛠️ Features
- Fully Offline Speech Recognition (Vosk).
- Lightweight LLM (DistilGPT2) for open-ended conversations.
- Natural-sounding neural voice (Coqui TTS).
- Command execution (Wikipedia search, open YouTube/Google, tell jokes, show time).
- Simple and modular Python project.

---

## 🚀 Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/iamaber/voice-assistant
    cd voice-assistant
    ```

2. **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Vosk Model (Offline STT):**
    - Visit: [Vosk Models](https://alphacephei.com/vosk/models)
    - Download: `vosk-model-small-en-us-0.15`
    - Extract it in the project directory.

---

## 🏃‍♂️ How to Run
```bash
python main.py
