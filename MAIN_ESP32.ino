#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>


// --- WiFi ---
const char *ssid = "Yusuf iPhone 13";
const char *password = "kepokamubabi";

// --- Ubidots ---
String ubidotsToken = "BBUS-8rMLXoEFppMoI2rt7r9zFIOEu53CTe";
String deviceLabel = "esp32-sic6-stage3";
String alertLabel = "alert";

// --- Variable Labels (di Ubidots) ---
String tempLabel = "temperature";
String humLabel = "humidity";
String latLabel = "latitude";     
String lonLabel = "longitude";    

// --- Sensor & Aktuator ---
#define DHTPIN 19
#define DHTTYPE DHT11
#define BUZZERPIN 5
#define FLAME_SENSOR_PIN 18 // Pin untuk DO flame sensor-
#define GPS_RX_PIN 16  // GPS TX terhubung ke RX ESP32
#define GPS_TX_PIN 17  // GPS RX terhubung ke TX ESP32
#define TRIG_PIN 22   // Pin untuk Trigger
#define ECHO_PIN 23   // Pin untuk Echo

DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
HardwareSerial gpsSerial(1); // gunakan UART1

void sendToUbidots(String label, float value) {
  HTTPClient http;
  String url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + deviceLabel + "/";
  http.begin(url);
  http.addHeader("X-Auth-Token", ubidotsToken);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"" + label + "\":" + String(value, 6) + "}";
  int httpCode = http.POST(payload);

  if (httpCode > 0) {
    Serial.println("✅ Data " + label + " terkirim: " + String(value));
  } else {
    Serial.println("❌ Gagal kirim data " + label);
  }

  http.end();
}

int getUbidotsAlert() {
  HTTPClient http;
  String url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + deviceLabel + "/" + alertLabel + "/lv";

  http.begin(url);
  http.addHeader("X-Auth-Token", ubidotsToken);
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    http.end();
    return payload.toInt();
  } else {
    Serial.println("❌ Gagal ambil alert dari Ubidots");
    http.end();
    return 0;
  }
}

void setup() {
  Serial.begin(9600);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("🔌 Menghubungkan WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Tersambung");

  dht.begin();
  pinMode(BUZZERPIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);  // Pin trig sebagai output
  pinMode(ECHO_PIN, INPUT);   // Pin echo sebagai input

  // GPS setup
  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
  Serial.println("🚀 Sistem siap kirim data ke Ubidots!");
}

void loop() {
  float suhu = dht.readTemperature();
  float kelembapan = dht.readHumidity();

  if (isnan(suhu) || isnan(kelembapan)) {
    Serial.println("❌ Gagal baca DHT!");
  } else {
    Serial.print("Suhu: ");
    Serial.print(suhu);
    Serial.print(" °C, Kelembapan: ");
    Serial.println(kelembapan);

    sendToUbidots(tempLabel, suhu);
    sendToUbidots(humLabel, kelembapan);
  }

  // Mengirim sinyal trigger (pulse pendek)
  digitalWrite(TRIG_PIN, LOW);  
  delayMicroseconds(2);          
  digitalWrite(TRIG_PIN, HIGH); 
  delayMicroseconds(10);        
  digitalWrite(TRIG_PIN, LOW);

  // Membaca durasi sinyal echo
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Menghitung jarak (dalam cm)
  float distance = duration * 0.034 / 2;  // Kecepatan suara 343 m/s (0.034 cm/μs)

  // Menampilkan jarak ke serial monitor
  Serial.print("Jarak: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Baca GPS
  while (gpsSerial.available() > 0) {
    char c = gpsSerial.read();
    Serial.write(c); // cetak karakter GPS mentah ke Serial Monitor
    gps.encode(c);   // tetap diproses juga ke TinyGPS++
  }

  if (gps.location.isValid()) {
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();

    Serial.print("\nLatitude: ");
    Serial.println(latitude, 6);
    Serial.print("Longitude: ");
    Serial.println(longitude, 6);

    sendToUbidots(latLabel, latitude);
    sendToUbidots(lonLabel, longitude);
  } else {
    Serial.println("\n❌ GPS belum dapat lokasi fix");
  }


  if (gps.location.isValid()) {
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();

    Serial.print("Latitude: ");
    Serial.println(latitude, 6);
    Serial.print("Longitude: ");
    Serial.println(longitude, 6);

    sendToUbidots(latLabel, latitude);
    sendToUbidots(lonLabel, longitude);
  } else {
    Serial.println("❌ GPS belum dapat lokasi");
  }

  // Ambil alert dari Ubidots
  int alertStatus = getUbidotsAlert();
  Serial.print("📥 Status alert dari Ubidots: ");
  Serial.println(alertStatus);

  // Baca status flame sensor (DO)
  int flameStatus = digitalRead(FLAME_SENSOR_PIN);
  if (flameStatus == HIGH) {
    Serial.println("🔥 Api terdeteksi!");
    digitalWrite(BUZZERPIN, HIGH); // Aktifkan buzzer jika api terdeteksi
  } else {
    Serial.println("🔒 Tidak ada api.");
    digitalWrite(BUZZERPIN, LOW); // Matikan buzzer jika tidak ada api
  }

  // Logika buzzer berdasarkan suhu, kelembapan, dan flame sensor
  bool suhuBahaya = suhu > 50;
  bool lembapBahaya = kelembapan > 80;
  bool alertDariUbidots = alertStatus == 1;
  bool apiTerbaca = flameStatus == HIGH;

  if (suhuBahaya || lembapBahaya || alertDariUbidots || apiTerbaca) {
    Serial.println("🚨 Buzzer ON");
    digitalWrite(BUZZERPIN, HIGH);
  } else {
    digitalWrite(BUZZERPIN, LOW);
  }

  // Logika Buzzer (misal, jika jarak kurang dari 10 cm)
  if (distance < 10) {
    Serial.println("🚨 Jarak terlalu dekat!");
    digitalWrite(BUZZERPIN, HIGH);  // Menyalakan buzzer
  } else {
    digitalWrite(BUZZERPIN, LOW);   // Mematikan buzzer
  }

  // Kirim data jarak ke Ubidots
  sendToUbidots("distance", distance);

}
