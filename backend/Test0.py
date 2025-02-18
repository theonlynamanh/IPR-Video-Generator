from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from moviepy import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    concatenate_audioclips, CompositeAudioClip
)
from gtts import gTTS
import shutil
import os

app = FastAPI()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.mount("/videos", StaticFiles(directory=UPLOAD_FOLDER), name="videos")

@app.post("/upload_content/")
async def upload_content(
    images: list[UploadFile] = File(...),
    script: str = Form(...),
    bgm: UploadFile = File(...)
):
    # Validate that the bgm file is an audio file and has an .mp3 extension
    if not bgm.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Background music file must be an audio file.")
    if not bgm.filename.lower().endswith('.mp3'):
        raise HTTPException(status_code=400, detail="Background music file must be in MP3 format.")

    # Save images
    image_paths = []
    for image in images:
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_paths.append(image_path)

    # Save background music file
    bgm_path = os.path.join(UPLOAD_FOLDER, bgm.filename)
    with open(bgm_path, "wb") as buffer:
        shutil.copyfileobj(bgm.file, buffer)
    
    # Process the script: split into sentences (assuming sentences are separated by a period)
    sentences = [s.strip() for s in script.split('.') if s.strip()]
    num_segments = min(len(sentences), len(image_paths))

    tts_clips = []
    image_clips = []

    for i in range(num_segments):
        sentence = sentences[i]
        tts_path = os.path.join(UPLOAD_FOLDER, f"tts_{i}.mp3")
        tts = gTTS(sentence, lang="en")
        tts.save(tts_path)
        tts_audio = AudioFileClip(tts_path)
        tts_clips.append(tts_audio)
        # Set image clip duration equal to the TTS audio duration for the sentence
        clip = ImageClip(image_paths[i]).with_duration(tts_audio.duration)
        image_clips.append(clip)

    # Concatenate image clips and TTS audio clips
    video_clip = concatenate_videoclips(image_clips, method="compose")
    final_tts_audio = concatenate_audioclips(tts_clips)

    # Load and adjust the background music (BGM)
    bgm_audio = AudioFileClip(bgm_path).with_duration(final_tts_audio.duration)

    # Combine TTS audio with BGM
    final_audio = CompositeAudioClip([final_tts_audio, bgm_audio])
    final_video = video_clip.with_audio(final_audio)

    # Write the final video to disk
    output_path = os.path.join(UPLOAD_FOLDER, "output.mp4")
    final_video.write_videofile(output_path, fps=24)

    return {"video_url": f"http://127.0.0.1:8000/videos/output.mp4"}
