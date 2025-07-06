#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "tu_ssid";
const char* password = "tu_contraseña";
const char* serverUrl = "http://tu_servidor_python:puerto/receptor";

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conexión WiFi establecida");
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
}

void loop() {
  // Capturar imagen y detección de caras
  // Crear JSON con los datos de detección de caras

  DynamicJsonDocument jsonDoc(1024);
  // Agregar datos de detección de caras al JSON

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonDoc.as<String>());
  if (httpResponseCode > 0) {
    Serial.printf("Detecciones de caras enviadas al servidor con código de respuesta: %d\n", httpResponseCode);
  } else {
    Serial.printf("Error al enviar detecciones de caras al servidor (%s)\n", http.errorToString(httpResponseCode).c_str());
  }
  http.end();

  delay(1000); // Puedes ajustar el intervalo de envío de detecciones de caras según tus necesidades
}
