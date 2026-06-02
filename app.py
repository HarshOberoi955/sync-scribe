import gradio as gr
import os
from extract_audio import extract_audio, burn_subtitles
from transcribe_audio import transcribe_and_sync, translate_segments, save_to_srt
from youtube_downloader import download_youtube_video

# 1. Add 'enable_diarization' to your inputs!
def process_video(video_filepath, youtube_url, source_lang, target_lang, enable_diarization):
    """The Master Pipeline: Video In -> Subtitled Video Out"""
    if youtube_url and youtube_url.strip() != "":
        video_to_process = download_youtube_video(youtube_url)
    elif video_filepath:
        video_to_process = video_filepath
    else:
        return None, None
        
    if not video_to_process:
        return None, None
    
    print(f"\n📥 Processing video: {video_to_process}")

    temp_audio = "temp_audio.wav"
    temp_srt = "temp_subtitles.srt"
    final_video = "final_output.mp4"

    extract_audio(video_to_process, temp_audio)
    
    # 2. Pass the checkbox value straight into your transcription function!
    transcribed_segments = transcribe_and_sync(
        temp_audio, 
        source_lang=source_lang, 
        target_lang=target_lang,
        run_diarization=enable_diarization
    )

    if target_lang != "en" and source_lang != target_lang:
        print(f"🌍 Running text translator for {target_lang}...")
        final_segments = translate_segments(transcribed_segments, target_lang=target_lang)
    else:
        final_segments = transcribed_segments

    save_to_srt(final_segments, temp_srt)
    output_video = burn_subtitles(video_to_process, temp_srt, final_video)

    return output_video, temp_srt

# --- THE UPDATED WEB UI ---
interface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Upload your Video (.mp4)"),
        gr.Textbox(
            label="OR Paste a YouTube Link here",
            placeholder="https://www.youtube.com/watch?v=..."
        ),
        gr.Dropdown(
            choices=["en", "hi", "pa", "es", "fr", "de"],
            value="en",
            label="1. Spoken Language"
        ),
        gr.Dropdown(
            choices=["en", "hi", "pa", "es", "fr", "de"],
            value="hi",
            label="2. Subtitle Language"
        ),
        # 🔥 NEW: The Speaker Diarization Checkbox!
        gr.Checkbox(
            label="👥 Track and Label Speakers (e.g. [Speaker 00], [Speaker 01])", 
            value=False
        )
    ],
    outputs=[
        gr.Video(label="🎬 Watch your Subtitled Video!"),
        gr.File(label="Download Subtitles (.srt)")
    ],
    title="🎙️ SyncScribe: AI Auto-Subtitles",
    description="Upload a video OR paste a YouTube link, pick your language, and let the AI do the rest!",
)

if __name__ == "__main__":
    interface.launch()