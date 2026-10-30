import easyocr
import cv2
from pathlib import Path
import numpy as np

# Same video path as Whisper
vid_path = Path.home() / "programming" / "REELS_SUM" / "DT6yw_JCOFQ.mp4"  # UPDATE!

reader = easyocr.Reader(['en', 'fr'])  # English + French (your location)

cap = cv2.VideoCapture(str(vid_path))
frame_count = 0
texts = []

print("Scanning frames for text...")
while cap.isOpened() and frame_count < 20:  # First 20s max
    ret, frame = cap.read()
    if not ret: break
    
    if frame_count % 30 == 0:  # Every ~1s
        results = reader.readtext(frame)
        frame_text = " | ".join([text[1] for text in results])
        if frame_text.strip():
            texts.append(f"Frame {frame_count}s: {frame_text}")
            print(f"Frame {frame_count}s: {frame_text}")
    
    frame_count += 1
cap.release()

print(f"\n {len(texts)} texts found!")
for t in texts[-5:]:  # Last 5
    print(t)