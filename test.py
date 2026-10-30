import yt_dlp
from pathlib import Path

base_dir = Path.home() / "programming" / "REELS_SUM" / "download"
base_dir.mkdir(parents=True, exist_ok=True)

# Use YOUR real public Reel URL here (instagram.com/reel/ABC123...)
url = input("Paste Instagram Reel URL: ").strip()

ydl_opts = {
    "outtmpl": str(base_dir / "%(id)s.%(ext)s"),
    "format": "bestvideo*+bestaudio/best",  # More flexible
    "quiet": False,  # Show progress
}

print(f"Downloading {url}...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    file_path = ydl.prepare_filename(info)
    print(f"✅ Downloaded: {file_path}")