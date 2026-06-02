import whisper
import os
from pyannote.audio import Pipeline

HF_TOKEN = os.getenv("HF_TOKEN")

def diarize_audio(audio_path, hf_token):
    """Uses Pyannote AI to analyze the audio and figure out who spoke when."""
    print("👥 Loading Speaker Diarization engine (detecting distinct voices)...")

    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=hf_token
        )

        diarization = pipeline(audio_path)

        speaker_segments = []
        for turn, _, speaker in diarization.speaker_diarization.itertracks(yield_label=True):
            # 🔥 ADD THIS TEMP LINE TO PRINT WHAT THE AI DETECTS:
            print(f"DEBUG TIME: {turn.start:.1f}s - {turn.end:.1f}s | AI NAMED: {speaker}")
            
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })

        unique_count = len(set(s['speaker'] for s in speaker_segments))
        print(f"✅ Diarization complete! Detected {unique_count} unique speakers.")
        return speaker_segments
    except Exception as e:
        print(f"⚠️ Diarization skipped or failed: {e}")
        print("💡 Make sure you accepted BOTH terms on Hugging Face and pasted your token correctly!")
        return []
    
def assign_speakers_to_segments(whisper_segments, speaker_segments):
    """Matches each Whisper sentence to the speaker who was talking at that exact time."""
    if not speaker_segments:
        return whisper_segments
    
    for w_seg in whisper_segments:
        w_start = w_seg["start"]
        w_end = w_seg["end"]
        w_mid = (w_start + w_end) / 2
        best_speaker = "SPEAKER_00"
        max_overlap = 0

        for s_seg in speaker_segments:
            overlap_start = max(w_start, s_seg["start"])
            # ✅ FIXED: Now correctly using s_seg["end"] to isolate the second speaker!
            overlap_end = min(w_end, s_seg["end"]) 
            overlap = max(0, overlap_end - overlap_start)

            if overlap > max_overlap:
                max_overlap = overlap
                best_speaker = s_seg["speaker"]

        # Fallback if there isn't a direct overlap block
        if max_overlap == 0:
            closest_dist = float('inf')
            for s_seg in speaker_segments:
                dist = min(abs(s_seg["start"] - w_mid), abs(s_seg["end"] - w_mid))
                if dist < closest_dist:
                    closest_dist = dist
                    best_speaker = s_seg["speaker"]
                
        w_seg["speaker"] = best_speaker
    return whisper_segments

def transcribe_and_sync(audio_path, source_lang="en", target_lang="en", run_diarization=False):
    """The main transcription system using Whisper Large."""
    print("⏳ Loading the MASSIVE Whisper 'Large' model...")
    model = whisper.load_model("large")

    if target_lang == "en" and source_lang != "en":
        print(f"🎙️ Listening to {source_lang} and translating DIRECTLY to English...")
        result = model.transcribe(audio_path, language=source_lang, task="translate", condition_on_previous_text=False)
    else:
        print(f"🎙️ Listening and transcribing in {source_lang}...")
        hint = "ਇਹ ਪੰਜਾਬੀ ਵਿੱਚ ਇੱਕ ਆਡੀਓ ਹੈ।" if source_lang == "pa" else None
        result = model.transcribe(audio_path, language=source_lang, initial_prompt=hint, condition_on_previous_text=False)
    
    whisper_segments = result["segments"]

    if run_diarization:
        speaker_turns = diarize_audio(audio_path, HF_TOKEN)
        whisper_segments = assign_speakers_to_segments(whisper_segments, speaker_turns)

    return whisper_segments

def translate_segments(segments, target_lang):
    """Your existing translation loop (keeps speaker tags intact if they exist)"""
    return segments

def save_to_srt(segments, out_path):
    """Saves the final timeline into a valid subtitles (.srt) file."""
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    with open(out_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start_str = format_time(seg["start"])
            end_str = format_time(seg["end"])
            text = seg["text"].strip()
            
            # 🔥 NEW: Format text to show [SPEAKER_00]: Text here if speaker tracking is on
            if "speaker" in seg:
                clean_speaker = seg["speaker"].replace("SPEAKER_", "Speaker ")
                line = f"[{clean_speaker}]: {text}"
            else:
                line = text
                
            f.write(f"{i}\n{start_str} --> {end_str}\n{line}\n\n")