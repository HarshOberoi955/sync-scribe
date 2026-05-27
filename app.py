import gradio as gr
import os
# Import your amazing functions from the other file!
from transcribe_audio import transcribe_and_sync, translate_segments, save_to_srt

def generate_subtitles(audio_filepath, target_lang):
    """
    This is the wrapper function. Gradio will pass the uploaded file path 
    and the selected language to this function when the user clicks 'Submit'.
    """
    if audio_filepath is None:
        return None
        
    print(f"📥 Received file: {audio_filepath}")
    
    # 1. We define what the final file should be named
    output_filename = "final_subtitles.srt"
    
    # 2. Run your AI pipeline!
    english_segments = transcribe_and_sync(audio_filepath)
    translated_segments = translate_segments(english_segments, target_lang=target_lang)
    save_to_srt(translated_segments, output_filename)
    
    # 3. Return the file path so the web interface can download it
    return output_filename

# --- The Web Interface Design ---
print("🚀 Starting SyncScribe Web UI...")

interface = gr.Interface(
    fn=generate_subtitles,
    
    # Define what the user sees on the left side (Inputs)
    inputs=[
        gr.Audio(type="filepath", label="Drop your Audio file here"),
        gr.Dropdown(
            choices=["es", "fr", "de", "hi", "it", "ja"], 
            value="es", 
            label="Translation Language (es=Spanish, fr=French, etc.)"
        )
    ],
    
    # Define what the user sees on the right side (Outputs)
    outputs=gr.File(label="Download your Subtitles (.srt)"),
    
    # Make it look pretty
    title="🎙️ SyncScribe: AI Auto-Subtitles",
    description="Drop an audio file below, pick a language, and let the AI generate perfect time-synced subtitles.",
    theme="default"
)

# Launch the local server
if __name__ == "__main__":
    interface.launch()