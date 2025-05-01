import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import time
import random

# === SIDEBAR CONTROLS ===
st.sidebar.header("🔧 Configuration")

# Day/Night toggle
mode = st.sidebar.radio("🌗 Select Mode", ["Day", "Night"])
is_night = mode == "Night"

# Camera toggle
enable_camera = st.sidebar.checkbox("Enable Camera Input", value=True)
temp_thresh = st.sidebar.slider("Temperature Alert Threshold (°C)", 25.0, 40.0, 30.0)
humidity_thresh = st.sidebar.slider("Humidity Alert Threshold (%)", 30.0, 90.0, 70.0)

# Real-time location input
latitude = st.sidebar.number_input("Latitude", value=37.7749)
longitude = st.sidebar.number_input("Longitude", value=-122.4194)

# Simulated flame sensor toggle
simulate_flame = st.sidebar.checkbox("🔥 Simulate Flame Detected", value=False)

# Simulated OLED display text
simulate_oled_text = f"""Temp Alert: >{temp_thresh}°C
Humidity Alert: >{humidity_thresh}%
Flame: {'YES' if simulate_flame else 'NO'}"""

# === DYNAMIC STYLING ===
background_color = "#00256c" if is_night else "#f0f2f6"
text_color = "white" if is_night else "#333"
card_color = "#003366" if is_night else "#ffffff"
chart_template = "plotly_dark" if is_night else "plotly_white"

# === CUSTOM CSS ===
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

        .camera-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
img = Image.open('helmaware_header.jpg')
st.image(img)

st.markdown(f"<h1 class='header'>Welcome to HelmAware ({mode} Mode)</h1>", unsafe_allow_html=True)

# === SENSOR SIMULATION ===
st.markdown("<h3 class='big-font'>Temperature & Humidity Data</h3>", unsafe_allow_html=True)

data = {
    'Time': pd.date_range(start='2025-04-01', periods=10, freq='D'),
    'Temperature': np.random.uniform(20, 35, 10),
    'Humidity': np.random.uniform(30, 80, 10),
}
df = pd.DataFrame(data)

if df['Temperature'].max() > temp_thresh:
    st.warning("🚨 Maximum temperature exceeds the set threshold!")

if df['Humidity'].max() > humidity_thresh:
    st.warning("💧 Maximum humidity exceeds the set threshold!")

col1, col2 = st.columns(2)
with col1:
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=df['Time'], y=df['Temperature'], mode='lines+markers', name='Temperature (°C)', line=dict(color='red')))
    fig_temp.update_layout(title='Temperature Over Time', xaxis_title='Time', yaxis_title='Temperature (°C)', template=chart_template)
    st.plotly_chart(fig_temp)

with col2:
    fig_humidity = go.Figure()
    fig_humidity.add_trace(go.Scatter(x=df['Time'], y=df['Humidity'], mode='lines+markers', name='Humidity (%)', line=dict(color='blue')))
    fig_humidity.update_layout(title='Humidity Over Time', xaxis_title='Time', yaxis_title='Humidity (%)', template=chart_template)
    st.plotly_chart(fig_humidity)

# === CAMERA SECTION ===
if enable_camera:
    st.markdown("<h3 class='big-font'>Camera</h3>", unsafe_allow_html=True)
    picture = st.camera_input("Capture Image")
    if picture:
        st.image(picture, caption="Captured Image", use_column_width=True)

# === FLAME SENSOR ===
st.markdown("<h3 class='big-font'>🔥 Flame Sensor Status</h3>", unsafe_allow_html=True)
if simulate_flame:
    st.error("🔥 Flame Detected! Take Immediate Action!")
else:
    st.success("✅ No Flame Detected.")

# === OLED DISPLAY ===
st.markdown("<h3 class='big-font'>🖥️ OLED Display</h3>", unsafe_allow_html=True)
with st.container():
    st.code(simulate_oled_text, language="text")
st.caption("This simulates what an OLED display connected to a Raspberry Pi might show in real-time.")

# === MAP SECTION ===
st.markdown("<h3 class='big-font'>📍 Real-Time Worker Location Map</h3>", unsafe_allow_html=True)
location_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
st.map(location_data)

st.text("Refreshing map every 5 seconds...")
time.sleep(5)




# === CHATBOX ===
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