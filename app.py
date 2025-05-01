import streamlit as st
import cv2
import time
import numpy as np
from geopy.distance import geodesic
import pandas as pd
from PIL import Image
from datetime import datetime
import requests
from paho.mqtt import publish
from ultralytics import YOLO

# === SIDEBAR CONTROLS ===
st.sidebar.header("🔧 Configuration")

mode = st.sidebar.radio("🌗 Select Mode", ["Day", "Night"])
is_night = mode == "Night"

enable_camera = st.sidebar.checkbox("Enable Camera Stream", value=True)
temp_thresh = st.sidebar.slider("Temperature Alert Threshold (°C)", 25.0, 40.0, 30.0)
humidity_thresh = st.sidebar.slider("Humidity Alert Threshold (%)", 30.0, 90.0, 70.0)

latitude = st.sidebar.number_input("Latitude", value=37.7749)
longitude = st.sidebar.number_input("Longitude", value=-122.4194)

simulate_flame = st.sidebar.checkbox("🔥 Simulate Flame Detected", value=False)

simulate_oled_text = f"""Temp Alert: >{temp_thresh}°C
Humidity Alert: >{humidity_thresh}%
Flame: {'YES' if simulate_flame else 'NO'}"""

# === DYNAMIC STYLING ===
background_color = "#00256c" if is_night else "#f0f2f6"
text_color = "white" if is_night else "#333"
card_color = "#003366" if is_night else "#ffffff"
chart_template = "plotly_dark" if is_night else "plotly_white"

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Darker+Grotesque&display=swap');

        body {{
            background-color: {background_color};
            font-family: 'Darker Grotesque', sans-serif;
        }}

        h1, h2, h3, p {{
            color: {text_color};
        }}

        .big-font {{
            font-size: 30px;
            color: {text_color};
        }}

        .header {{
            text-align: center;
        }}

        .card {{
            background-color: {card_color};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
        }}
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
img = Image.open('helmaware_header.jpg')
st.image(img)

# === SENSOR SIMULATION ===
data = {
    'Time': pd.date_range(start='2025-04-01', periods=10, freq='D'),
    'Temperature': np.random.uniform(20, 35, 10),
    'Humidity': np.random.uniform(30, 80, 10),
}
df = pd.DataFrame(data)
latest_temp = df['Temperature'].iloc[-1]
latest_hum = df['Humidity'].iloc[-1]

# === TOP METRICS BAR ===
st.markdown("## 🔍 Real-Time Sensor Overview")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("🌡️ Temperature", f"{latest_temp:.1f} °C")
metric_col2.metric("💧 Humidity", f"{latest_hum:.1f} %")
metric_col3.metric("📍 Latitude", f"{latitude:.5f}")
metric_col4.metric("📍 Longitude", f"{longitude:.5f}")

# === MODEL LOADING ===
model = YOLO("yolov8n.pt")  # Pastikan model YOLOv8 sudah terdownload dengan benar

# === DETECTION FUNCTION ===
def hazard_detection_stream(CAMERA_SNAPSHOT_URL, model, area_thresh, trigger_alert, reset_alert_if_needed):
    with st.container():
        st.markdown('<h2 style="text-align: left;">📷 Live Kamera & Deteksi Bahaya (YOLOv8)</h2>', unsafe_allow_html=True)

        cap = cv2.VideoCapture(CAMERA_SNAPSHOT_URL)

        if not cap.isOpened():
            st.error("❌ Gagal membuka stream dari ESP32-CAM.")
        else:
            ret, frame = cap.read()
            cap.release()

            if ret and frame is not None:
                results = model(frame)[0]
                annotated = results.plot()
                hazard_detected = False

                for box in results.boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    x1, y1, x2, y2 = box.xyxy[0]
                    area = (x2 - x1) * (y2 - y1)

                    if label == "person":
                        if area > area_thresh:
                            hazard_detected = True
                            trigger_alert()
                            st.session_state.logs.append(
                                f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 {label.upper()} - Area: {int(area)}"
                            )
                        else:
                            st.session_state.logs.append(
                                f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ {label.upper()} detected - Area: {int(area)} (too small)"
                            )
                        break  # Stop after first person

                if not hazard_detected:
                    reset_alert_if_needed()

                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
            else:
                st.warning("⚠️ Gagal membaca frame dari stream.")
# === KAMERA STREAM ===
# Definisikan URL kamera di sini
CAMERA_SNAPSHOT_URL = 'http://your_camera_ip_or_url_here'  # Gantilah dengan URL kamera yang benar

# Penggunaan cv2.VideoCapture
cap = cv2.VideoCapture(CAMERA_SNAPSHOT_URL)

with st.container():
    st.markdown('<h2 style="text-align: left;">📷 Live Kamera & Deteksi Bahaya (YOLOv8)</h2>', unsafe_allow_html=True)

    cap = cv2.VideoCapture(CAMERA_SNAPSHOT_URL)

    if not cap.isOpened():
        st.error("❌ Gagal membuka stream dari ESP32-CAM.")
    else:
        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            results = model(frame)[0]
            annotated = results.plot()
            hazard_detected = False

            for box in results.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                x1, y1, x2, y2 = box.xyxy[0]
                area = (x2 - x1) * (y2 - y1)

                if label == "person":
                    if area > area_thresh:
                        hazard_detected = True
                        trigger_alert()
                        st.session_state.logs.append(
                            f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 {label.upper()} - Area: {int(area)}"
                        )
                    else:
                        st.session_state.logs.append(
                            f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ {label.upper()} detected - Area: {int(area)} (too small)"
                        )
                    break  # Stop after first person

            if not hazard_detected:
                reset_alert_if_needed()

            st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
        else:
            st.warning("⚠️ Gagal membaca frame dari stream.")

            
# === FLAME SENSOR ===
st.markdown("<h3 class='big-font'>🔥 Flame Sensor Status</h3>", unsafe_allow_html=True)
if simulate_flame:
    st.error("🔥 Flame Detected! Take Immediate Action!")
else:
    st.success("✅ No Flame Detected.")

# === MAP SECTION ===
st.markdown("<h3 class='big-font'>📍 Real-Time Worker Location Map</h3>", unsafe_allow_html=True)
location_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
st.map(location_data)

st.text("Refreshing map every 5 seconds...")

# === CHATBOT SECTION ===
# Ambil data sensor
temp = get_ubidots_variable_value("temperature")
hum = get_ubidots_variable_value("humidity")
alert = get_ubidots_variable_value("alert")

# === KONFIGURASI GEMINI ===
GEMINI_API_KEY = 'AIzaSyAqBof9P4D2d85k3YtopLOI_k3kJdYybvw'
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent?key={GEMINI_API_KEY}"

def get_gemini_response(prompt, temp, hum, alert):
    GEMINI_API_KEY = 'AIzaSyAqBof9P4D2d85k3YtopLOI_k3kJdYybvw'
    GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent?key={GEMINI_API_KEY}"

    # Data sensor sebagai konteks
    sensor_info = f"""
    Berikut adalah data sensor terbaru dari helm cerdas:
    - Suhu: {temp:.1f}°C
    - Kelembapan: {hum:.1f}%
    - Status Bahaya: {'Bahaya terdeteksi' if alert == 1 else 'Tidak ada bahaya terdeteksi'}
    """

    # Prompt akhir untuk dikirim ke Gemini
    full_prompt = f"""
    Anda adalah asisten keselamatan dari sistem helm cerdas di dalam proyek konstruksi. Jawablah pertanyaan pengguna berdasarkan informasi ini:
    {sensor_info}

    Pertanyaan pengguna: {prompt}
    """

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ Error dari Gemini API. Status: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"⚠️ Terjadi error: {str(e)}"

# === INTERFACE CHAT ===
st.title("🛠️ HelmAware Chat Bot")

prompt = st.chat_input("💬 Tanyakan sesuatu tentang kondisi sensor atau keselamatan...")

if prompt:
    st.chat_message("user").write(prompt)
    prompt = prompt.lower()
    reply = ""

    # Jawaban langsung berdasarkan keyword
    if "suhu" in prompt or "temperature" in prompt:
        reply = f"🌡️ Sensor saat ini mendeteksi suhu sekitar **{temp:.1f}°C**." if temp else "⚠️ Data suhu tidak tersedia."
    elif "kelembapan" in prompt or "humidity" in prompt:
        reply = f"💧 Kelembapan saat ini sekitar **{hum:.1f}%**." if hum else "⚠️ Data kelembapan tidak tersedia."
    elif "bahaya" in prompt or "alert" in prompt or "status" in prompt:
        if alert == 1:
            reply = "🚨 **Bahaya terdeteksi!** Segera lakukan pemeriksaan dan evakuasi bila perlu!"
        elif alert == 0:
            reply = "✅ Saat ini tidak terdeteksi kondisi berbahaya."
        else:
            reply = "⚠️ Status bahaya tidak bisa diambil sekarang."
    else:
        # Kirim ke Gemini dengan data sensor sebagai konteks
        reply = get_gemini_response(prompt, temp, hum, alert)

    st.chat_message("assistant").write(reply)