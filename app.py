import yt_dlp
import whisper
import easyocr
import cv2
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Reel Summary API")
downloads_dir = Path.home() / "programming" / "REELS_SUM" / "download"

# Load models once (startup)
print("Loading models...")
whisper_model = whisper.load_model("base")
ocr_reader = easyocr.Reader(['en', 'fr'])
print(" Ready!")

class ReelRequest(BaseModel):
    url: str

@app.post("/process-reel/")
async def process_reel(request: ReelRequest):
    # Download
    downloads_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {"outtmpl": str(downloads_dir / "%(id)s.%(ext)s"), "format": "bestvideo*+bestaudio/best", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(request.url, download=True)
        vid_path = ydl.prepare_filename(info)
    
    # Whisper
    result = whisper_model.transcribe(str(vid_path))
    transcript = result["text"]
    
    # OCR (sample frames)
    cap = cv2.VideoCapture(str(vid_path))
    ocr_texts = []
    frame_count = 0
    while cap.isOpened() and frame_count < 30:
        ret, frame = cap.read()
        if not ret: break
        if frame_count % 30 == 0:
            results = ocr_reader.readtext(frame)
            frame_text = " | ".join([text[1] for text in results if text[2] > 0.5])
            if frame_text.strip():
                ocr_texts.append(frame_text)
        frame_count += 1
    cap.release()
    
    summary = f"🎤 Audio: {transcript[:300]}...\n Texts: {'; '.join(ocr_texts[:5])}"
    
    return {
        "video_path": str(vid_path),
        "transcript": transcript,
        "ocr_texts": ocr_texts,
        "summary": summary
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)