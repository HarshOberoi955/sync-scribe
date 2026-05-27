import gradio as gr
import os
from extract_audio import extract_audio, burn_subtitles
from transcribe_audio import transcribe_and_sync, translate_segments, save_to_srt

def process_video(video_filepath, target_lang):
    """The Master Pipeline: Video In -> Subtitled Video Out"""
    if video_filepath is None:
        return None, None
    
    print(f"\n📥 Received video: {video_filepath}")
    temp_audio = "temp_audio.wav"
    temp_srt = "temp_subtitles.srt"
    final_video = "final_output.mp4"

    extract_audio(video_filepath, temp_audio)
    english_segments = transcribe_and_sync(temp_audio)
    translated_segments = translate_segments(english_segments, target_lang=target_lang)
    save_to_srt(translated_segments, temp_srt)
    burn_subtitles(video_filepath, temp_srt, final_video)
    return final_video, temp_srt

print("🚀 Starting SyncScribe Web UI...")

interface = gr.Interface(
    fn=process_video,

    inputs=[
        gr.Video(label="Upload your Video (.mp4)"),
        gr.Dropdown(
            choices=["en", "fr", "de", "hi", "it", "ja", "pa"],
            value="en",
            label="Translation Language (es=Spanish, hi=Hindi, pa=Punjabi, etc.)"
        )
    ],

    outputs=[
        gr.Video(label="🎬 Watch your Subtitled Video!"),
        gr.File(label="Download Subtitles (.srt)")
    ],

    title="🎙️ SyncScribe: AI Auto-Subtitles",
    description="Upload a video, pick a language, and the AI will hardcode translated subtitles directly onto your video!",
)

if __name__ == "__main__":
    interface.launch()