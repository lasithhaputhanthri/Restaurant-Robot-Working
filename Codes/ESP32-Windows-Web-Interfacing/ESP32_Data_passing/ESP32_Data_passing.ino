#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>  // Include the ArduinoJson library

const char *ssid = "Yasiru's Pradator";
const char *password = "unlimited";
const char *serverIP = "192.168.137.1:5000/api_endpoint";
const int serverPort = 5000;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Nothing to do here for this example

  // Send GET request
  sendGETRequest();
  // delay(1000);
}

void sendGETRequest() {
  HTTPClient http;

  // Specify the URL
  String url = "http://" + String(serverIP) + "?command=Robot=001";

  // Start the request
  http.begin(url);

  // Get the HTTP response code
  int httpCode = http.GET();

  // Check for a successful response
  if (httpCode > 0) {
    // Serial.printf("HTTP GET request successful, response code: %d\n", httpCode);
    String payload = http.getString();

    // Parse the JSON response
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);

    // Extract and print the "command" value
    const char *command = doc["command"];
    Serial.printf("Received command: %s\n", command);
  } else {
    Serial.printf("HTTP GET request failed, response code: %d\n", httpCode);
  }

  // Close the connection
  http.end();
}
