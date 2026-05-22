# Speedy J.A.R.V.I.S. like Personal Assistant

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Ollama](https://img.shields.io/badge/Powered_by-Ollama_Llama3-orange)

Speedy is a cutting-edge, offline, open-source personal AI assistant built with Python. Powered by **Meta's Llama 3** (running locally via Ollama) and wrapped in a stunning, highly detailed **Iron Man-inspired Web HUD**, Speedy brings a true sci-fi experience to your desktop.

## ✨ Features

* **Ultra-Detailed Sci-Fi HUD:** A massive web-based UI featuring complex hexagon grids, pulsing arc reactors, and an Iron Man centerpiece.
* **100% Offline AI:** Chat with your assistant entirely offline using Ollama and the Llama 3 model—no API keys or subscriptions required.
* **Live Hardware Telemetry:** 
  * Real-time CPU, RAM, and GPU (NVIDIA) usage monitoring.
  * Live Top-5 Process tracking (Who is eating your RAM/CPU?).
  * Live Upload/Download Network Radar.
* **Privacy Monitors:** Actively scans your Windows Registry and Audio Core to alert you if apps are currently using your Microphone, Camera, or Speakers.
* **Voice Recognition & Speech:** Fully equipped with local speech-to-text (`SpeechRecognition`) and text-to-speech (`pyttsx3`).

## 🚀 Installation

### 1. Prerequisites
- **Python 3.8+**
- **Ollama:** Download and install from [ollama.com](https://ollama.com/)

### 2. Clone the Repository
```bash
git clone https://github.com/UthkarshMandloi/Spdeey-lama-based-persional-assistent.git
cd Spdeey-lama-based-persional-assistent
```

### 3. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Download the Llama 3 Model
Ensure Ollama is running, then pull the model:
```bash
ollama pull llama3
```

## 💻 Usage

Run the main script to launch the HUD and awaken Speedy:
```bash
python speedy.py
```
- Speedy will greet you and enter "Standby" mode. 
- Say **"Speedy"** to wake him up, and then speak your commands!

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.