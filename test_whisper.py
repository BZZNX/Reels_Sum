import whisper
from pathlib import Path

# Path to your downloaded file (copy from Step 2)
vid_path = Path.home() / "programming" / "REELS_SUM" / "download" / "DUCq38mgDP0.mp4"  

model = whisper.load_model("base")  # Fast (30s), good enough

print("Transcribing...")
result = model.transcribe(str(vid_path))
print("🎤 TRANSCRIPT:")
print(result["text"])
print(f"\nSegments: {len(result['segments'])}")