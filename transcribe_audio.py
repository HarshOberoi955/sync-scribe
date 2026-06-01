import whisper
import os
from deep_translator import GoogleTranslator

def transcribe_and_sync(audio_path, source_lang="en", target_lang="en"):
    print("⏳ Loading the MASSIVE Whisper 'Large' model (this will take a while)...")
    
    # 🔥 THE UPGRADE: We are officially using the smartest model available!
    model = whisper.load_model("large")
    
    # If going from Punjabi/Hindi -> English, let Whisper do it natively
    if target_lang == "en" and source_lang != "en":
        print(f"🎙️ Listening to {source_lang} and translating DIRECTLY to English...")
        result = model.transcribe(
            audio_path,
            language=source_lang,
            task="translate", 
            condition_on_previous_text=False
        )
    else:
        print(f"🎙️ Listening and transcribing in {source_lang}...")
        hint = "ਇਹ ਪੰਜਾਬੀ ਵਿੱਚ ਇੱਕ ਆਡੀਓ ਹੈ।" if source_lang == "pa" else None
        result = model.transcribe(
            audio_path,
            language=source_lang,
            initial_prompt=hint,
            condition_on_previous_text=False
        )
    
    return result["segments"]

def translate_segments(segments, target_lang='es'):
    """
    Takes the timestamps and text from Whisper, translates the text, 
    and perfectly maps it back to the original timestamps.
    """
    print(f"\n🌍 Translating to {target_lang}...")
    
    # 🚨 This was the missing line that caused the error!
    translator = GoogleTranslator(source='auto', target=target_lang)
    
    translated_segments = []
    for segment in segments:
        original_text = segment["text"].strip()
        
        # Translate the text
        translated_text = translator.translate(original_text)
        
        # Create a new segment keeping original time, but new text
        translated_segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": translated_text
        })
        
        # Print progress
        start_time = round(segment["start"], 2)
        print(f"[{start_time}s] {translated_text}")
        
    return translated_segments

def format_timestamp(seconds):
    """Converts raw seconds into the strict SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def save_to_srt(segments, filepath):
    """Saves the translated segments to a standard .srt file with UTF-8 encoding."""
    print(f"💾 Saving subtitles to '{filepath}'...")
    
    # The encoding="utf-8" guarantees Hindi and Punjabi characters are saved safely!
    with open(filepath, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            # Write the strict SRT format
            f.write(f"{i+1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")
            
    print(f"✅ Success! Your subtitle file is ready at '{filepath}'")

# --- Test the script ---
if __name__ == "__main__":
    audio_file = "extracted_audio.wav"
    output_srt = "spanish_subtitles.srt"
    
    if os.path.exists(audio_file):
        # 1. Transcribe (English)
        english_segments = transcribe_and_sync(audio_file)
        
        # 2. Translate (Spanish)
        spanish_segments = translate_segments(english_segments, target_lang='es')
        
        # 3. Save as Subtitle file
        save_to_srt(spanish_segments, output_srt)
        
    else:
        print(f"❌ Error: Could not find '{audio_file}'.")