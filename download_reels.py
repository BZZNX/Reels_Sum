import yt_dlp
from pathlib import Path

base_dir = Path.home() / "programming" / "reel-su" / "download"
base_dir.mkdir(parents=True, exist_ok=True)

url = "https://www.instagram.com/reel/DT6yw_JCOFQ/" 

ydl_opts = {
    "outtmpl": str(base_dir / "%(id)s.%(ext)s"),
    "format": "best[height<=720]",  # HD but fast
    "quiet": True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    file_path = ydl.prepare_filename(info)
    print(f"Downloaded: {file_path}")



    



