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
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Access sensitive data from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UBIDOTS_API_URL = os.getenv("UBIDOTS_API_URL")
DEVICE_LABEL = os.getenv("DEVICE_LABEL")  # Ambil DEVICE_LABEL dari .env

UBIDOTS_TOKEN = "BBUS-8rMLXoEFppMoI2rt7r9zFIOEu53CTe"
headers = {"X-Auth-Token": UBIDOTS_TOKEN}

# === SEND TO TELEHGRAM ===
def send_telegram_alert(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        st.warning(f"Gagal kirim pesan: {response.text}")

# === GET UBIDOTS VARIABLE VALUE ===
def get_ubidots_variable_value(var_label):
    """
    Mengambil nilai variabel dari Ubidots berdasarkan label variabel.
    """
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{var_label}/lv"
    try:
        response = requests.get(url, headers=headers)
        print(f"[{datetime.now()}] Response Status: {response.status_code}, Response Text: {response.text}")
        if response.status_code == 200:
            return float(response.text)
        else:
            return None
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")  # Log error with timestamp
        return None

# === INITIALIZE SESSION STATE ===    
temp = get_ubidots_variable_value("temperature") 
hum = get_ubidots_variable_value("humidity") 
alert = get_ubidots_variable_value("alert") 
latitude = get_ubidots_variable_value("latitude") 
longitude = get_ubidots_variable_value("longitude") 
flame = get_ubidots_variable_value("flame") 

print(f"DEBUG - Temperature: {temp}")
print(f"DEBUG - Humidity: {hum}")
print(f"DEBUG - Alert: {alert}")
print(f"DEBUG - Latitude: {latitude}")
print(f"DEBUG - Longitude: {longitude}")
 
# === SIDEBAR CONTROLS ===
st.sidebar.header("🔧 Configuration")

mode = st.sidebar.radio("🌗 Select Mode", ["Day", "Night"])
is_night = mode == "Night"

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
img = Image.open('Helmaware_Header.jpg')
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
metric_col3.metric("📍 Latitude", f"{latitude:.5f}" if latitude is not None else "Unknown")
metric_col4.metric("📍 Longitude", f"{longitude:.5f}" if longitude is not None else "Unknown")

# === LINE CHARTS ===
st.markdown("## 📈 Sensor Data Over Time")

# Line chart for temperature
st.markdown("### 🌡️ Temperature Over Time")
temp_data = {
    'Time': pd.date_range(start='2025-04-01', periods=10, freq='D'),
    'Temperature': np.random.uniform(20, 35, 10),
}
temp_df = pd.DataFrame(temp_data)
st.line_chart(temp_df.set_index('Time')['Temperature'])

# Line chart for humidity
st.markdown("### 💧 Humidity Over Time")
hum_data = {
    'Time': pd.date_range(start='2025-04-01', periods=10, freq='D'),
    'Humidity': np.random.uniform(30, 80, 10),
}
hum_df = pd.DataFrame(hum_data)
st.line_chart(hum_df.set_index('Time')['Humidity'])

# === MODEL LOADING ===
model = YOLO("smoke_detection.pt")

# === PARAMETER ===
CAMERA_SNAPSHOT_URL = 'http://172.20.10.2/capture'  # pastikan ini URL snapshot, bukan stream
area_thresh = 10000  # ambang batas area objek

# === INISIALISASI SESSION STATE ===
if "logs" not in st.session_state:
    st.session_state.logs = []
if "alert" not in st.session_state:
    st.session_state.alert = 0

def trigger_alert():
    st.session_state.alert = 1
    # Kamu bisa tambahkan logika kirim Telegram di sini

def reset_alert_if_needed():
    st.session_state.alert = 0

# === GET FRAME FROM CAMERA ===
def get_camera_frame(url):
    try:
        response = requests.get(url, timeout=5)
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return frame
    except:
        return None

# === DETEKSI BAHAYA SECARA LOOP (SEMI-REALTIME) ===
st.markdown('<h2 style="text-align: left;">📷 Live Kamera & Deteksi Bahaya (YOLOv8)</h2>', unsafe_allow_html=True)
run_detection = st.checkbox("🔁 Jalankan Deteksi Real-Time")

placeholder = st.empty()

while run_detection:
    frame = get_camera_frame(CAMERA_SNAPSHOT_URL)

    if frame is not None:
        results = model(frame)[0]
        annotated = results.plot()
        hazard_detected = False

        for box in results.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            x1, y1, x2, y2 = box.xyxy[0]
            area = (x2 - x1) * (y2 - y1)

            if label == "person" and area > area_thresh:
                hazard_detected = True
                trigger_alert()
                st.session_state.logs.append(
                    f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 {label.upper()} - Area: {int(area)}"
                )
                break
            elif label == "person":
                st.session_state.logs.append(
                    f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ {label.upper()} detected - Area: {int(area)} (too small)"
                )
                break

        if not hazard_detected:
            reset_alert_if_needed()

        placeholder.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
    else:
        placeholder.warning("⚠️ Gagal membaca gambar dari kamera.")

    time.sleep(2)  # delay antar frame

# === TAMPILKAN LOG ===
with st.expander("📝 Log Deteksi"):
    for log in reversed(st.session_state.logs[-10:]):
        st.markdown(log)

            
# === FLAME SENSOR ===
st.markdown("<h3 class='big-font'>🔥 Flame Sensor Status</h3>", unsafe_allow_html=True)
if flame:
    st.error("🔥 Flame Detected! Take Immediate Action!")
else:
    st.success("✅ No Flame Detected.")

# === MAP SECTION ===
st.markdown("<h3 class='big-font'>📍 Real-Time Worker Location Map</h3>", unsafe_allow_html=True)

# Buat DataFrame lokasi
location_data = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})

# Tampilkan peta hanya jika data lokasi valid
if location_data[["latitude", "longitude"]].notnull().all(axis=1).any():
    st.map(location_data.dropna(subset=["latitude", "longitude"]))
else:
    st.info("📌 Lokasi belum tersedia karena GPS belum mengirimkan data.")

st.text("Refreshing map every 5 seconds...")

flame_detected = flame  # Status flame (simulasi)

# === CHATBOT SECTION ===
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Inisialisasi session state
if 'alert_time' not in st.session_state:
    st.session_state.alert_time = None
if 'alert_sent' not in st.session_state:
    st.session_state.alert_sent = False
if 'alert_resolved' not in st.session_state:
    st.session_state.alert_resolved = False

# Logika saat alert aktif
if alert == 1 and not st.session_state.alert_resolved:
    st.markdown("### Status Alert: 🚨 Bahaya Terdeteksi")

    # Tombol OK aktif
    ok_pressed = st.button("✅ OK", type="primary")

    if st.session_state.alert_time is None:
        st.session_state.alert_time = time.time()

    if ok_pressed:
        st.success("👍 Tindakan telah dikonfirmasi.")
        st.session_state.alert_time = None
        st.session_state.alert_sent = False
        st.session_state.alert_resolved = True  # tandai sudah diselesaikan
    else:
        elapsed = time.time() - st.session_state.alert_time
        if elapsed > 10 and not st.session_state.alert_sent:
            send_telegram_alert(
                "🚨 [HelmAware] Bahaya terdeteksi tapi belum ada respon selama 10 detik!",
                BOT_TOKEN,
                CHAT_ID
            )
            st.session_state.alert_sent = True

# Jika alert bukan 1 atau sudah diselesaikan
else:
    st.markdown("### Status Alert: ✅ Aman")
    st.button("✅ OK", disabled=True, type="secondary")
    st.session_state.alert_time = None
    st.session_state.alert_sent = False
    st.session_state.alert_resolved = False  # reset kalau sudah tidak bahaya


# === KONFIGURASI GEMINI ===
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent?key={GEMINI_API_KEY}"

def get_gemini_response(prompt, temp, hum, alert, latitude, longitude, flame_detected):
    # Data sensor sebagai konteks
    sensor_info = f"""
    Berikut adalah data sensor terbaru dari helm cerdas:
    - 🌡️ Suhu: {temp:.1f}°C
    - 💧 Kelembapan: {hum:.1f}%
    - 📍 Lokasi: Latitude {latitude:.5f}, Longitude {longitude:.5f}
    - 🔥 Status Flame: {'Terdeteksi' if flame_detected else 'Tidak Terdeteksi'}
    - 🚨 Status Bahaya: {'Bahaya terdeteksi' if alert == 1 else 'Tidak ada bahaya terdeteksi'}
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
        reply = get_gemini_response(prompt, temp, hum, alert, latitude, longitude, flame_detected)

    st.chat_message("assistant").write(reply)

from datetime import datetime
