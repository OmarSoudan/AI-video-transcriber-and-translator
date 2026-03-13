# AI Video Transcriber & Translator 🎥

An automated pipeline that downloads YouTube audio, transcribes it using OpenAI's **Whisper**, and then uses **Ollama (DeepSeek-R1)** to proofread and translate the transcript into multiple `.srt` subtitle files.

## ✨ Features
* **YouTube Integration**: Automatic audio extraction via `yt-dlp`.
* **High Accuracy**: Sentence-level splitting for better subtitle timing.
* **AI Proofreading**: Automatically fixes transcription "hallucinations" or typos using local LLMs.
* **Multi-language**: Generates separate SRT files for various target languages.
* **Privacy-First**: Runs entirely locally via Whisper and Ollama.

---

## 🚀 Setup Instructions

### 1. Prerequisites
You must have the following installed on your system:
* **Python 3.9+**
* **FFmpeg**: Required for audio processing.
    * *Windows*: `choco install ffmpeg`
    * *Mac*: `brew install ffmpeg`
    * *Linux*: `sudo apt install ffmpeg`
* **Ollama**: [Download here](https://ollama.com/) and pull your preferred model:
  ```bash
  ollama pull deepseek-r1
2. Installation
Clone the repository and install the Python dependencies:

Bash
git clone [https://github.com/your-username/repo-name.git](https://github.com/your-username/repo-name.git)
cd repo-name
pip install -r requirements.txt
3. Configuration
Copy the example environment file and edit it if necessary:

Bash
cp .env.example .env
🛠 Usage
Run the main script and provide a YouTube URL when prompted:

Bash
python main.py
The script will output:

transcription_en.srt (The proofread English version)

transcription_[lang].srt (The translated versions)

📝 License
MIT License. Feel free to use and modify!


---

### Pro-Tip for your GitHub Repo:
Before you `git push`, make sure to create a **.gitignore** file so you don't accidentally upload your large audio files or local environment settings:

**`.gitignore`**
```text
# Python
__pycache__/
*.py[cod]

# Environments
.env
.venv
env/

# Project Specific
*.mp3
*.srt
temp_audio*
