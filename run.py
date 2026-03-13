import os
import yt_dlp
import whisper
import datetime
import asyncio
import ollama
from typing import List, Dict, Any

class Config:
    """Configuration settings for the Transcriber."""
    AUDIO_TMP = "temp_audio.mp3"
    MODEL_SIZE = "medium"
    OLLAMA_MODEL = "deepseek-r1"
    TARGET_LANGUAGES = {
        'English': 'en',
        'Arabic': 'ar',
        'French': 'fr',
        'Spanish': 'es',
        'German': 'de',
        'Italian': 'it',
    }

class TranscriptionTool:
    def __init__(self):
        self.model = None

    def _get_ollama_response(self, prompt: str) -> str:
        """Internal helper to communicate with Ollama."""
        try:
            response = ollama.chat(
                model=Config.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print(f"[!] Ollama error: {e}")
            return ""

    def download_audio(self, url: str):
        """Downloads audio from YouTube using yt-dlp."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # Removed hardcoded FFmpeg path for portability
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Ensure the file is named correctly regardless of yt-dlp's extension behavior
        if os.path.exists("temp_audio.mp3"):
            os.replace("temp_audio.mp3", Config.AUDIO_TMP)

    def transcribe(self, file_path: str) -> List[Dict]:
        """Transcribes audio using OpenAI Whisper."""
        if not self.model:
            print(f"Loading Whisper model ({Config.MODEL_SIZE})...")
            self.model = whisper.load_model(Config.MODEL_SIZE)
            
        result = self.model.transcribe(file_path, fp16=False, word_timestamps=True)
        return self._split_into_sentences(result["segments"])

    def _split_into_sentences(self, segments: List[Dict]) -> List[Dict]:
        """Groups Whisper word-level timestamps into full sentences."""
        new_segments = []
        for seg in segments:
            words = seg.get('words', [])
            sentence = []
            for word_data in words:
                sentence.append(word_data)
                if word_data['word'].strip().endswith(('.', '!', '?')):
                    new_segments.append({
                        'start': sentence[0]['start'],
                        'end': sentence[-1]['end'],
                        'text': ' '.join(w['word'].strip() for w in sentence)
                    })
                    sentence = []
            if sentence: # Catch leftovers
                new_segments.append({
                    'start': sentence[0]['start'],
                    'end': sentence[-1]['end'],
                    'text': ' '.join(w['word'].strip() for w in sentence)
                })
        return new_segments

    def format_srt_time(self, seconds: float) -> str:
        """Converts seconds to SRT timestamp format (00:00:00,000)."""
        td = datetime.timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int(td.microseconds / 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def write_srt(self, segments: List[Dict], filename: str):
        """Writes processed segments to an SRT file."""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segments, 1):
                f.write(f"{i}\n")
                f.write(f"{self.format_srt_time(seg['start'])} --> {self.format_srt_time(seg['end'])}\n")
                f.write(f"{seg['text']}\n\n")

    async def ai_process(self, text: str, task: str, lang: str = None) -> str:
        """Handles both proofreading and translation via Ollama."""
        if task == "proofread":
            prompt = f"Proofread this transcript. Fix grammar/spelling only. Keep technical terms. Return ONLY the corrected text.\n\nText: {text}"
        else:
            prompt = f"Translate this text to {lang}. Keep names and technical terms unchanged. Return ONLY the translation.\n\nText: {text}"
        
        return self._get_ollama_response(prompt)

    def cleanup(self):
        """Removes temporary files."""
        if os.path.exists(Config.AUDIO_TMP):
            os.remove(Config.AUDIO_TMP)

async def main():
    tool = TranscriptionTool()
    url = input("Enter YouTube URL: ")

    try:
        print("--- Phase 1: Downloading ---")
        tool.download_audio(url)

        print("--- Phase 2: Transcribing ---")
        raw_segments = tool.transcribe(Config.AUDIO_TMP)

        # Process Base Proofreading
        print("--- Phase 3: AI Proofreading ---")
        proofread_segments = []
        for s in raw_segments:
            corrected = await tool.ai_process(s['text'], "proofread")
            proofread_segments.append({**s, 'text': corrected})
        
        tool.write_srt(proofread_segments, "transcription_en.srt")
        print("Saved: transcription_en.srt")

        # Process Translations
        print("--- Phase 4: Translating ---")
        for name, code in Config.TARGET_LANGUAGES.items():
            if name == "English": continue
            
            translated_segments = []
            for s in proofread_segments:
                trans = await tool.ai_process(s['text'], "translate", lang=name)
                translated_segments.append({**s, 'text': trans})
            
            output_name = f"transcription_{code}.srt"
            tool.write_srt(translated_segments, output_name)
            print(f"Saved: {output_name}")

    finally:
        tool.cleanup()
        print("\nProcess complete.")

if __name__ == "__main__":
    asyncio.run(main())
