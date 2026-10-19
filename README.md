# AI Video Transcriber & Translator 🎥

An easy, privacy-first pipeline that downloads audio from YouTube, transcribes it with OpenAI's Whisper, then proofreads and translates the transcript locally using an Ollama LLM (for example: deepseek-r1). The project produces time-aligned .srt subtitle files in the original language and in any target languages you configure.

---

## ✨ Highlights

- YouTube integration via yt-dlp for automatic audio extraction.
- Sentence-level splitting for accurate subtitle timing.
- Local AI proofreading (reduces transcription errors and hallucinations) using Ollama models.
- Multi-language output: produces separate .srt files per target language.
- Privacy-first: everything runs locally — no cloud uploads required.

---

## 🚀 Prerequisites

- Python 3.9 or newer
- FFmpeg (for audio processing)
  - Windows: choco install ffmpeg
  - macOS: brew install ffmpeg
  - Debian/Ubuntu: sudo apt install ffmpeg
- yt-dlp (or youtube-dl fork) for downloading YouTube audio
- Ollama: install from https://ollama.com/ and pull a local model such as deepseek-r1
- Whisper (local): openai/whisper or whisper.cpp binding, depending on your preferred setup

Note: numpy and other Python dependencies are managed in requirements.txt.

---

## 🔧 Installation

1. Clone the repository and enter the project directory:

```bash
git clone https://github.com/OmarSoudan/AI-video-transcriber-and-translator.git
cd AI-video-transcriber-and-translator
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Pull an Ollama model locally (example):

```bash
ollama pull deepseek-r1
```

4. Copy the example environment file and edit if needed:

```bash
cp .env.example .env
# Edit .env to point to local model names, output folder, languages, etc.
```

---

## 💻 Usage

Run the main script and provide a YouTube URL (or pass a URL via CLI if implemented):

```bash
python main.py
```

Typical outputs:
- transcription_en.srt — proofread English subtitles
- transcription_[lang].srt — translated subtitles for each target language

If your repo exposes CLI flags, run `python main.py --help` to see options for input URL, output directory, languages, and verbosity.

---

## 🛠️ Implementation notes

- Audio extraction: yt-dlp downloads audio and FFmpeg converts/extracts the audio stream.
- Transcription: Whisper performs sentence-level or chunked transcription to improve timing and alignment.
- Proofreading & translation: a local Ollama model (e.g., deepseek-r1) post-processes the raw transcript to fix errors and produce translations while preserving timestamps.
- SubRip (.srt) generation: sentence-level segments are written with accurate start/end times for best player compatibility.

---

## 📝 Example .gitignore (recommended)

```text
# Python
__pycache__/
*.py[cod]

# Virtual environments
.env
.venv/
venv/

# Large media & temporary files
*.mp3
*.wav
*.srt
temp_audio*
```

---

## 📝 License

This project is released under the MIT License. See LICENSE for details.

---

## 🙋 Pro Tips

- Use a local Ollama model for best privacy and performance; choose one with good natural-language editing behavior for proofreading tasks.
- When transcribing long videos, increase chunk sizes to reduce model invocation overhead but ensure chunks still respect sentence boundaries for accurate timing.
- Keep large media files out of version control — add them to .gitignore before committing.

---

If you'd like, I can also add a short CLI usage section (examples of flags) or a minimal config example for .env. Let me know which you'd prefer.
