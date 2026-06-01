import yt_dlp
import os

def download_youtube_video(url, output_filename="youtube_download.mp4"):
    """Downloads a YouTube video and saves it as an MP4."""
    print(f"\n🌍 Fetching YouTube video: {url}")

    if os.path.exists(output_filename):
        os.remove(output_filename)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_filename,
        'quiet': True, 
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Success! YouTube video saved as '{output_filename}'")
        return output_filename
    except Exception as e:
        print(f"❌ Error downloading YouTube video: {e}")
        return None