/*
 * Get MAC Address — Flash to each ESP32-CAM first
 * =================================================
 * Prints the WiFi MAC address over Serial at 115200 baud.
 * You need the RECEIVER's MAC to put in controller.ino.
 *
 * Steps:
 *   1. Clip ESP32-CAM into ESP32-CAM-MB programmer
 *   2. Select board: "AI Thinker ESP32-CAM" in Arduino IDE
 *   3. Flash this sketch
 *   4. Open Serial Monitor at 115200
 *   5. Copy the MAC address (e.g., 24:6F:28:AB:CD:EF)
 *   6. Convert to hex array for controller.ino:
 *      24:6F:28:AB:CD:EF → {0x24, 0x6F, 0x28, 0xAB, 0xCD, 0xEF}
 */

#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  Serial.println("\n=============================");
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  Serial.println("=============================");
  Serial.println("Copy this MAC and put it in controller.ino as RECEIVER_MAC");
  Serial.println("Format: {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF}");
}

void loop() {
  // Blink onboard LED so you know it's running
  pinMode(33, OUTPUT);
  digitalWrite(33, LOW);
  delay(500);
  digitalWrite(33, HIGH);
  delay(500);
}
