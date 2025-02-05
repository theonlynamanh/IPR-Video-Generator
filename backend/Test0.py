from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import shutil
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Nếu muốn an toàn hơn, thay "*" bằng ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức HTTP (POST, GET, ...)
    allow_headers=["*"],  # Cho phép tất cả headers
)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_files(images: list[UploadFile] = File(...), audio: UploadFile = File(...)):
    # Lưu ảnh
    image_paths = []
    for image in images:
        img_path = f"{UPLOAD_FOLDER}/{image.filename}"
        with open(img_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_paths.append(img_path)

    # Lưu file âm thanh
    audio_path = f"{UPLOAD_FOLDER}/{audio.filename}"
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Tạo video
    video_path = generate_video(image_paths, audio_path)
    
    return {"video_url": f"http://127.0.0.1:8000/download/{os.path.basename(video_path)}"}

def generate_video(image_files, audio_file):
    duration_per_image = 3
    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration  

    # Lặp ảnh để vừa với thời lượng âm thanh
    image_clips = []
    current_duration = 0
    index = 0
    while current_duration < audio_duration:
        img = image_files[index % len(image_files)]
        clip = ImageClip(img).with_duration(duration_per_image)
        image_clips.append(clip)
        current_duration += duration_per_image
        index += 1

    # Cắt video theo âm thanh
    final_video = concatenate_videoclips(image_clips, method="compose").with_audio(audio).subclipped(0, audio_duration)
    output_path = f"{UPLOAD_FOLDER}/output.mp4"
    final_video.write_videofile(output_path, fps=24)

    return output_path

@app.get("/download/{filename}")
def download_video(filename: str):
    return FileResponse(f"{UPLOAD_FOLDER}/{filename}", media_type="video/mp4", filename=filename)
# uvicorn Test0:app --reload
