# 🚧 HelmAware: Smart Construction Hazard Detection System

HelmAware is a real-time hazard detection and alert system designed to improve safety on construction sites. It uses a combination of ESP32 sensor modules, a YOLOv8-based object detection model, a user-friendly Streamlit dashboard, and Telegram notifications to detect smoke, flame, motion, and unauthorized presence, alert workers, and notify supervisors.

---

## 📖 Project Overview

Construction sites are prone to various safety hazards such as smoke, fire, unauthorized access, and environmental changes. HelmAware provides a smart solution by integrating:

- Live camera monitoring and YOLOv8 detection
- Multiple safety sensors connected to ESP32 microcontrollers
- Automatic alert and escalation system via Telegram
- An interactive web dashboard for real-time visualization and alert acknowledgement

---

## 🚀 Key Features

- 🔍 **YOLOv8 Detection**  
  Detects smoke, people, or other hazardous objects in real time using a custom YOLOv8 model.

- 📷 **Live Camera Feed**  
  Real-time video streaming via ESP32-CAM displayed on a Streamlit dashboard.

- 🌡 **Multi-Sensor Integration**  
  Real-time data from:
  - **Flame Sensor Module** for detecting fire
  - **DHT11 Sensor** for temperature and humidity
  - **PIR Sensor** for motion detection
  - **Ultrasonic Module** for distance and presence detection
  - **GPS Module** for precise location logging
  - **Buzzer Module** for sound-based local alerts

- 🚨 **Smart Alert System**  
  Alerts triggered by detected hazards (via camera or sensor) update the dashboard and require user acknowledgement.

- 🔔 **Telegram Notification Bot**  
  If alerts are ignored for 10 seconds, a Telegram bot sends messages to a group of supervisors.

- ✅ **Acknowledgement Button**  
  A button to confirm and reset the alert on the Streamlit dashboard.

- 📊 **Event Logging**  
  All detected hazards and system responses are logged and displayed in real time.

- 🤖 **AI Assistant Chat**  
  Integrated with Gemini API to assist users with contextual safety and system queries.

---

## ⚙️ How It Works

1. **Live Stream & Detection**
   - Stream video from ESP32-CAM into the Streamlit app.
   - Use YOLOv8 to detect specific hazard classes like “person” or “smoke.”

2. **Sensor Monitoring**
   - Sensors connected to ESP32 send data to Ubidots platform.
   - Dashboard fetches temperature, humidity, flame, GPS, and motion data.

3. **Alert Handling**
   - If hazard is detected (either by camera or sensor), the system:
     - Sets `alert = 1`
     - Displays warning on dashboard
     - Starts a 10-second timer
   - If no user response, Telegram notification is triggered.

4. **User Acknowledgement**
   - User can press “OK” button to stop the alert and reset state.

---

## 🔧 Hardware Components

| Component               | Description                                |
|------------------------|--------------------------------------------|
| **ESP32-CAM Module**   | For capturing and streaming real-time video |
| **ESP32 WROOM Module** | Main controller for receiving sensor data   |
| **DHT11 Sensor**       | Measures temperature and humidity           |
| **Flame Sensor**       | Detects fire or sudden flame presence       |
| **PIR Sensor**         | Detects motion around the equipment         |
| **Ultrasonic Sensor**  | Measures distance to detect proximity       |
| **GPS Module**         | Logs the physical location of the device    |
| **Buzzer Module**      | Sounds alarm during hazardous events        |

---

## 🛠️ Tech Stack

- **Model**: YOLOv8 (Ultralytics)
- **Backend**: Python (OpenCV, requests, Streamlit)
- **Frontend**: Streamlit
- **IoT Platform**: Ubidots
- **Messaging**: Telegram Bot API
- **Hardware**: ESP32-CAM, ESP32 WROOM, various sensors

## ▶️ Links & Resources

- 📹 [Demo Video](https://your-video-link.com)  
- 📄 [Presentation Slides (PPT)](https://your-slides-link.com)  
- 🌐 [Live Deployment (Streamlit)](https://your-streamlit-app-link.com)  
- 📊 [Ubidots Dashboard](https://your-ubidots-dashboard-link.com)  

## 🤝 Contributors
- **Deira Aisya Refani** : Back End & IoT Developer
- **Finanazwa Ayesha** : Product Designer
- **Regina Joan Medea Jati Laksono** : Front End Developer
- **Yusuf Imantaka Bastari** : ML Developer

