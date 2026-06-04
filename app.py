import gradio as gr
import os
# Make sure your other files (youtube_downloader, extract_audio, transcribe_audio) are imported here
from youtube_downloader import download_youtube_video
from extract_audio import extract_audio, burn_subtitles
from transcribe_audio import transcribe_and_sync, translate_segments, save_to_srt

# 📱 ULTRACLEAN iOS STYLED CONFIGURATION
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #070913 0%, #0c152b 45%, #082126 100%) !important;
    background-attachment: fixed !important;
}
.subpanel.options, ul.options, .dropdown-menu, li.item {
    background-color: #161d30 !important;
    color: #ffffff !important;
}
li.item.selected, li.item:hover {
    background: linear-gradient(90deg, #00b4db 0%, #0083b0 100%) !important;
    color: white !important;
}
.selected-item { color: #ffffff !important; }
"""

# 🌟 THE LIVING ENGINE WITH LIVE PROGRESS UPDATES
def process_video(video_file, youtube_url, source_lang, target_lang, enable_diarization, progress=gr.Progress()):
    video_to_process = None
    
    # Phase 1: Gathering File Source
    if youtube_url and youtube_url.strip():
        progress(0.1, desc="🌍 Fetching YouTube Video...")
        video_to_process = download_youtube_video(youtube_url)
    elif video_file:
        video_to_process = video_file
    else:
        raise gr.Error("Please upload a local video or paste a valid YouTube link!")

    # Phase 2: Isolation
    progress(0.3, desc="⏳ Splitting Audio Tracks from Video...")
    audio_path = "temp_audio.wav"
    extract_audio(video_to_process, audio_path)
    
    # Phase 3: AI Core Brain Transcription
    progress(0.5, desc="🎙️ Running AI Transcription (Whisper)...")
    hf_token = os.getenv("HF_TOKEN")
    
    # Pass your variables to your core engine
    final_segments = transcribe_and_sync(audio_path, source_lang, target_lang, enable_diarization, hf_token)
    
    # Phase 4: SRT Generations
    progress(0.7, desc="📝 Formatting SRT Subtitle Streams...")
    srt_path = "temp_subtitles.srt"
    save_to_srt(final_segments, srt_path)
    
    # Phase 5: Hardburning Video Overlay
    progress(0.9, desc="🎬 Multiplexing & Burning Subtitles into Video...")
    output_video = "final_output.mp4"
    burn_subtitles(video_to_process, srt_path, output_video)
    
    progress(1.0, desc="✅ SyncScribe Operations Complete!")
    return output_video, srt_path


# 🏗️ RECONFIGURED BLOCKS ARCHITECTURE
with gr.Blocks(css=custom_css, theme=gr.themes.Default(primary_hue="cyan", neutral_hue="slate").set(
    background_fill_primary_dark="rgba(15, 22, 42, 0.45)",
    background_fill_secondary_dark="rgba(21, 30, 54, 0.65)",
    block_background_fill_dark="rgba(21, 30, 54, 0.65)",
    border_color_accent_dark="#00b4db",           
    block_label_text_color_dark="#00d2ff",        
    button_primary_background_fill_dark="linear-gradient(135deg, #00b4db 0%, #0083b0 100%)",
    button_primary_text_color_dark="#ffffff",
    button_primary_background_fill_hover_dark="linear-gradient(135deg, #00d2ff 0%, #00b4db 100%)",
    input_background_fill_dark="#0f1626",
)) as demo:
    
    gr.Markdown("# 🎙️ SyncScribe: AI Auto-Subtitles")
    gr.Markdown("### Upload a video or paste a YouTube link, pick your target language layout, and let the AI process the text tracks.")
    
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Upload your Video (.mp4)")
            url_input = gr.Textbox(label="OR Paste a YouTube Link here", placeholder="https://www.youtube.com/watch?v=...")
            
            with gr.Row():
                src_lang = gr.Dropdown(choices=["en", "hi", "pa", "es", "fr", "de"], value="en", label="1. Spoken Language")
                tgt_lang = gr.Dropdown(choices=["en", "hi", "pa", "es", "fr", "de"], value="hi", label="2. Subtitle Language")
            
            diarize_check = gr.Checkbox(label="👥 Track and Label Speakers (e.g. [Speaker 00], [Speaker 01])", value=False)
            
            with gr.Row():
                clear_btn = gr.Button("Clear", variant="secondary")
                submit_btn = gr.Button("Submit", variant="primary")
                
        with gr.Column():
            video_output = gr.Video(label="🎬 Watch your Subtitled Video!")
            file_output = gr.File(label="Download Subtitles (.srt)")

    # Wiring up action triggers
    submit_btn.click(
        fn=process_video,
        inputs=[video_input, url_input, src_lang, tgt_lang, diarize_check],
        outputs=[video_output, file_output]
    )
    
    # Quick clear binding
    clear_btn.click(
        fn=lambda: (None, "", "en", "hi", False, None, None),
        inputs=[],
        outputs=[video_input, url_input, src_lang, tgt_lang, diarize_check, video_output, file_output]
    )

if __name__ == "__main__":
    demo.launch()