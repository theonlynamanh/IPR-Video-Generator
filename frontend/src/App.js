import React, { useState } from "react";
import axios from "axios";

function App() {
  const [images, setImages] = useState([]);
  const [bgm, setBgm] = useState(null);
  const [videoUrl, setVideoUrl] = useState("");
  const [script, setScript] = useState("");

  const handleImageChange = (e) => {
    setImages([...e.target.files]);
  };

  const handleScriptChange = (e) => {
    setScript(e.target.value);
  };

  const handleBgmChange = (e) => {
    setBgm(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    images.forEach((img) => formData.append("images", img));
    formData.append("bgm", bgm);
    formData.append("script", script);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setVideoUrl(response.data.video_url);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Tạo Video từ Ảnh kết hợp chuyển đổi văn bản thành giọng nói</h1>

      <div style={{ marginBottom: "20px" }}>
        <label>Chọn ảnh:</label>
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleImageChange}
        />
      </div>
      <div style={{ marginBottom: "20px" }}>
        <label>Nhập văn bản:</label>
        <br />
        <textarea
          value={script}
          onChange={handleScriptChange}
          rows="4"
          cols="50"
          placeholder="Nhập lời thoại tại đây. Ví dụ: Câu 1. Câu 2. Câu 3."
        />
      </div>
      <div style={{ marginBottom: "20px" }}>
        <label>Chọn file nhạc nền:</label>
        <input type="file" accept="bgm/mp3" onChange={handleBgmChange} />
      </div>

      <button
        onClick={handleUpload}
        style={{
          padding: "10px 20px",
          background: "blue",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Tạo Video
      </button>

      {videoUrl && (
        <div style={{ marginTop: "20px" }}>
          <h2>Video đã tạo:</h2>
          <video controls width="600">
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default App;
