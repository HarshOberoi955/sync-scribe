# 🎙️ SyncScribe: AI Auto-Subtitles

SyncScribe is a local, AI-powered pipeline that automatically extracts audio from media files, transcribes the speech with precise timestamps, translates it into multiple languages, and generates industry-standard `.srt` subtitle files.

## 🚀 Features
* **Audio Extraction:** Uses `ffmpeg` to rip and format audio from video files.
* **Smart Transcription:** Powered by OpenAI's `Whisper` for highly accurate, time-synced text generation.
* **Seamless Translation:** Uses `deep-translator` to convert text while preserving strict subtitle timestamps.
* **Web UI:** Includes a drag-and-drop web interface built with `Gradio`.

## 🛠️ Tech Stack
* Python
* OpenAI Whisper (PyTorch)
* Gradio
* FFmpeg

## 💻 How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the web app: `python app.py`