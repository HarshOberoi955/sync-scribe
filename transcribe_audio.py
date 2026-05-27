import whisper
import os
from deep_translator import GoogleTranslator

def transcribe_and_sync(audio_path):
    # We use the "base" model here. It's fast and doesn't require a massive GPU.
    # Later, you can change this to "small" or "medium" for even higher accuracy!
    print("⏳ Loading the Whisper AI model (this might take a few seconds)...")
    model = whisper.load_model("small")
    
    print(f"🎙️ Listening to '{audio_path}' and transcribing...")
    result = model.transcribe(audio_path, language="en")
    
    print("\n✅ Transcription Complete! Here are the synced timestamps:\n")
    print("-" * 50)
    
    # Whisper automatically breaks the audio into "segments"
    for segment in result["segments"]:
        start_time = round(segment["start"], 2)
        end_time = round(segment["end"], 2)
        text = segment["text"].strip()
        
        # Print it out nicely formatted
        print(f"[{start_time}s -> {end_time}s] {text}")
        
    print("-" * 50)
    
    # We will return this data so we can use it in Phase 3
    return result["segments"]

# --- Test the script ---
if __name__ == "__main__":
    # Point this to the audio file we generated in Phase 1
    audio_file = "extracted_audio.wav"
    
    if os.path.exists(audio_file):
        transcribe_and_sync(audio_file)
    else:
        print(f"❌ Error: Could not find '{audio_file}'. Did you delete it?")

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
    """Converts raw seconds into the strict HH:MM:SS,mmm format for SRT."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def save_to_srt(segments, output_filename):
    """Write the time-synced translated segments to an SRT file."""
    print(f"\n💾 Saving subtitles to '{output_filename}'...")

    with open(output_filename, 'w', encoding='utf-8') as f:
        for index, segment in enumerate(segments, start=1):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])

            f.write(f"{index}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{segment['text']}\n\n")

    print(f"✅ Success! Your subtitle file is ready at '{output_filename}'")

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