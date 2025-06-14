import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp
import numpy as np
import time
from scripts.drawing_logic import DrawingLogic

# Konfigurasi halaman
st.set_page_config(page_title="🎨 LuxDraw AI", layout="wide", page_icon="🧠")

# CSS modern & responsif
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #f2f4fc;
            padding: 1.5rem 1rem;
            width: 300px !important;
        }
        .stButton>button {
            background-color: #8c52ff;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #6e42cc;
        }
        .status-box {
            background-color: #ffffffcc;
            border: 2px solid #8c52ff;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
            font-size: 16px;
            font-weight: bold;
        }
        .block-container {
            padding: 2rem 2rem 4rem 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi drawing logic & MediaPipe
mp_hands = mp.solutions.hands
drawing_logic = DrawingLogic()

# === FIX: Video processor didefinisikan dulu di atas
class LuxDrawProcessor(VideoProcessorBase):
    def __init__(self, logic_instance):
        self.logic = logic_instance
        self.hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape
        img = cv2.flip(img, 1)

        if self.logic.canvas is None:
            self.logic.initialize_canvas(img.shape)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.logic.toggle_modes(hand_landmarks.landmark)
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_coords = (int(index_tip.x * w), int(index_tip.y * h))
                self.logic.draw(img, index_coords)

        self.logic.process_canvas()

        # Tampilkan idle timer (opsional)
        if self.logic.idle_start_time:
            elapsed = time.time() - self.logic.idle_start_time
            cv2.putText(img, f"Idle Timer: {round(elapsed,1)}s", (30, h - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        combined = cv2.addWeighted(img, 1, self.logic.canvas, 1, 0)
        return av.VideoFrame.from_ndarray(combined, format="bgr24")


# ===================== START STREAMLIT UI =====================

st.title("🧠 LuxDraw AI")
st.caption("🎨 Real-Time Gesture Drawing + Math OCR — Fun, Modern, Interactive!")

# Sidebar
with st.sidebar:
    st.header("📊 Status AI")
    result = drawing_logic.get_result()
    st.markdown(f"<div class='status-box'>🧠 Mode Aktif: <b>{drawing_logic.status_text}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-box'>✏️ Ekspresi Terbaca: <b>{result.get('detected_text', '')}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-box'>✅ Evaluasi: <b>{result.get('status_text', '')}</b></div>", unsafe_allow_html=True)

    if st.button("🔍 Paksa Proses Ekspresi (Manual)"):
        drawing_logic.process_canvas()
        st.rerun()

# Stream kamera real-time
st.subheader("📷 Kamera & Kanvas Real-Time")
webrtc_streamer(key="luxdraw-stream", video_processor_factory=lambda: LuxDrawProcessor(drawing_logic))

# Info
with st.expander("ℹ️ Panduan Penggunaan"):
    st.markdown("""
    - 🖐️ Gunakan gesture **menunjuk** untuk menggambar.
    - ✊ Gunakan **mengepal** untuk menghapus.
    - Saat **Idle 7 detik**, AI akan membaca & menghitung ekspresi otomatis.
    - 🎨 Klik warna di atas kanvas untuk mengganti warna.
    """)

# Footer
st.markdown("---")
st.markdown("📌 Dibuat dengan ❤️ oleh LuxDraw • Powered by MediaPipe, OpenCV, EasyOCR, WebRTC")
