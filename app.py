import gradio as gr
import os
from extract_audio import extract_audio, burn_subtitles
from transcribe_audio import transcribe_and_sync, translate_segments, save_to_srt

def process_video(video_filepath, source_lang, target_lang):
    """The Master Pipeline: Video In -> Subtitled Video Out"""
    if video_filepath is None:
        return None, None
    
    print(f"\n📥 Received video: {video_filepath}")
    
    # 1. Define our filenames FIRST
    temp_audio = "temp_audio.wav"
    temp_srt = "temp_subtitles.srt"
    final_video = "final_output.mp4"

    # 3. Transcribe (and optionally let Whisper translate to English natively)
    # We pass BOTH source and target languages now
    transcribed_segments = transcribe_and_sync(temp_audio, source_lang=source_lang, target_lang=target_lang)
    
    # 4. Translate the text (ONLY if we aren't already done!)
    if target_lang != "en" and source_lang != target_lang:
        print(f"🌍 Running text translator for {target_lang}...")
        final_segments = translate_segments(transcribed_segments, target_lang=target_lang)
    else:
        # Whisper already translated it to English, or it's the same language
        final_segments = transcribed_segments 

    
    save_to_srt(final_segments, temp_srt)

    output_video = burn_subtitles(video_filepath, temp_srt, final_video)

    return output_video, temp_srt

interface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Upload your Video (.mp4)"),

        gr.Dropdown(
            choices=["en", "hi", "pa", "es", "fr", "de"], 
            value="en", 
            label="1. Spoken Language (What is the person speaking?)"
        ),

        gr.Dropdown(
            choices=["en", "hi", "pa", "es", "fr", "de"], 
            value="hi", 
            label="2. Subtitle Language (What should the text say?)"
        )
    ],
    outputs=[
        gr.Video(label="🎬 Watch your Subtitled Video!"),
        gr.File(label="Download Subtitles (.srt)")
    ],
    title="🎙️ SyncScribe: AI Auto-Subtitles",
    description="Upload a video, tell the AI what language is being spoken, and pick your subtitle language!",
)

if __name__ == "__main__":
    interface.launch()