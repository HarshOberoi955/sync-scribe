# 🎙️ SyncScribe: Multi-Lingual AI Subtitle Generator & Speaker Diarization

SyncScribe is an end-to-end multimedia processing application designed to fetch videos, auto-transcribe spoken speech patterns, differentiate distinct human speakers using AI voiceprint characteristics, and burn translation tracks natively back into the exported layout files.

---

## ⚡ Key Core Features

* **Dual Media Loading Engine:** Supports raw local mp4 handling alongside automated background audio streams extraction straight from live YouTube frames.
* **Deep Neural Speech Transcription:** Implements state-of-the-art multi-lingual tracking frameworks using OpenAI's **Whisper-Large** deep layers.
* **Vocal Biometric Cluster Allocation:** Interacts with gated **Pyannote 3.1** models to build real-time vocal frequency fingerprints, classifying speakers cleanly without training data.
* **Dynamic Translation Pipeline:** Features flexible translation mappings, allowing audio streams from one dialect to turn into synchronized foreign SRT subtitle tracks.
* **Premium iOS Glassmorphism Interface:** Uses custom-themed, ultra-clean Gradio Blocks styling built optimized for distance viewing tracking.

---

## 🛠️ Architecture Flow Topology

1. **Extraction Pipeline:** Video Data ➔ FFmpeg Stream Separation ➔ Compressed WAV Target Isolation.
2. **Diarization Processing:** Audio Block ➔ Pyannote Audio Embedding Extraction ➔ Agglomerative Clustering ➔ Speaker Timeline Matrix.
3. **Transcription Merging:** Audio Snippets ➔ Whisper-Large Transcription Matrix ➔ Overlap Time-Stamp Matching ➔ Synchronized SRT Translation Stream Assembly.
4. **Multiplexing Generation:** Source Video File + Final SRT File ➔ Hardburned Libass Filter Layers ➔ Production-Ready MP4 Delivery.

---

## 🚀 Rapid Local Deploy Installation

### 1. Prerequisites Setup
Make sure your system contains a modern functional wrapper configuration of **FFmpeg**:
```bash
# Ubuntu/Linux Mint Installation
sudo apt update && sudo apt install ffmpeg -y