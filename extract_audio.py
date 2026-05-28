import ffmpeg
import os

def extract_audio(video_path, audio_output_path):
    """
    Strips the audio from a video file and saves it as a WAV file
    optimized for AI transcription (16kHz, mono).
    """
    
    if not os.path.exists(video_path):
        print(f"❌ Error: Could not find the video at '{video_path}'")
        return
    
    print(f"⏳ Extracting audio from {video_path}...")

    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_output_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"✅ Success! Audio ready for AI at '{audio_output_path}'")

    except ffmpeg.Error as e:
        print("❌ FFmpeg Error! Ensure FFmpeg is installed on your OS.")
        if e.stderr:
            print(e.stderr.decode('utf8'))

def burn_subtitles(video_path, srt_path, output_video_path):
    """
    Takes the original video and the new SRT file, and hardcodes 
    the text directly onto the video frames.
    """
    print("🎬 Burning subtitles into the video (this might take a moment)...")
    try:
        (
            ffmpeg
            .input(video_path)
            # Added vcodec and acodec to guarantee the web browser can play it!
            .output(
                output_video_path, 
                # We changed FreeSerif to Noto Sans Gurmukhi!
                vf=f"subtitles={srt_path}:force_style='Fontname=Noto Sans Gurmukhi,FontSize=24'", 
                vcodec="libx264", 
                acodec="aac"
            )
            
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"✅ Subtitled video ready at '{output_video_path}'!")
        return output_video_path
        
    except ffmpeg.Error as e:
        print("❌ FFmpeg Error while burning subtitles!")
        if e.stderr:
            print(e.stderr.decode('utf8'))
        return None
    
if __name__ == "__main__":
    input_video = "sample_video.mp4"
    output_audio = "extracted_audio.wav"
    
    extract_audio(input_video, output_audio)