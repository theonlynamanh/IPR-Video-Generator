import React, { useState } from "react";
import axios from "axios";

function App() {
  const [images, setImages] = useState([]);
  const [audio, setAudio] = useState(null);
  const [videoUrl, setVideoUrl] = useState("");

  const handleImageChange = (e) => {
    setImages([...e.target.files]);
  };

  const handleAudioChange = (e) => {
    setAudio(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    images.forEach((img) => formData.append("images", img));
    formData.append("audio", audio);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setVideoUrl(response.data.video_url);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Tạo Video từ Ảnh & Âm Thanh</h1>

      <div style={{ marginBottom: "20px" }}>
        <label>Chọn ảnh:</label>
        <input type="file" multiple accept="image/*" onChange={handleImageChange} />
      </div>

      <div style={{ marginBottom: "20px" }}>
        <label>Chọn file âm thanh:</label>
        <input type="file" accept="audio/mp3" onChange={handleAudioChange} />
      </div>

      <button onClick={handleUpload} style={{ padding: "10px 20px", background: "blue", color: "white", border: "none", cursor: "pointer" }}>
        Tạo Video
      </button>

      {videoUrl && (
        <div style={{ marginTop: "20px" }}>
          <h2>Video đã tạo:</h2>
          <video controls width="600">
            <source src={videoUrl} type="video/mp4" />
          </video>
        </div>
      )}
    </div>
  );
}
export default App;