/*
 * ESP-NOW Controller — Escort Bot
 * ================================
 * ESP32-CAM #1: Handheld controller with 5 buttons.
 * Sends drive commands to receiver via ESP-NOW (~5ms latency, ~200m range).
 *
 * WIRING (buttons connect pin to GND, using internal pullup):
 *   GPIO 13 → Forward button  → GND
 *   GPIO 15 → Backward button → GND
 *   GPIO 14 → Left button     → GND
 *   GPIO 2  → Right button    → GND
 *   GPIO 4  → Turbo button    → GND
 *
 * Boot notes:
 *   - GPIO 12 avoided (must be LOW at boot or enters wrong flash voltage)
 *   - GPIO 0 avoided (boot mode select)
 *   - GPIO 15 has internal pullup by default (safe for boot)
 *
 * SETUP:
 *   1. Flash this sketch via ESP32-CAM-MB programmer
 *   2. First flash get_mac.ino to find receiver's MAC address
 *   3. Replace RECEIVER_MAC below with actual MAC
 *   4. Re-flash this sketch
 */

#include <esp_now.h>
#include <WiFi.h>

// *** REPLACE WITH RECEIVER ESP32-CAM MAC ADDRESS ***
uint8_t RECEIVER_MAC[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// Button pins (active LOW — press connects to GND)
#define PIN_FWD   13
#define PIN_BACK  15
#define PIN_LEFT  14
#define PIN_RIGHT  2
#define PIN_TURBO  4

// Send rate (ms) — 50ms = 20Hz, fast enough for RC control
#define SEND_INTERVAL 50

// Command packet — must match receiver struct exactly
typedef struct {
  int8_t forward;  // -1 back, 0 stop, 1 forward
  int8_t turn;     // -1 left, 0 straight, 1 right
  uint8_t turbo;   // 0 normal, 1 turbo
  uint8_t estop;   // 0 normal, 1 emergency stop (no buttons = stop)
} ControlPacket;

ControlPacket packet;
esp_now_peer_info_t peerInfo;
unsigned long lastSend = 0;
bool peerAdded = false;

// Delivery callback — blink onboard LED on success
void onSent(const uint8_t *mac, esp_now_send_status_t status) {
  if (status == ESP_NOW_SEND_SUCCESS) {
    digitalWrite(33, LOW);  // ESP32-CAM onboard red LED (active LOW)
  } else {
    digitalWrite(33, HIGH);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("\n[CTRL] ESP-NOW Controller starting...");

  // Button pins — internal pullup, press = LOW
  pinMode(PIN_FWD, INPUT_PULLUP);
  pinMode(PIN_BACK, INPUT_PULLUP);
  pinMode(PIN_LEFT, INPUT_PULLUP);
  pinMode(PIN_RIGHT, INPUT_PULLUP);
  pinMode(PIN_TURBO, INPUT_PULLUP);

  // Onboard LED (GPIO 33, active LOW)
  pinMode(33, OUTPUT);
  digitalWrite(33, HIGH); // off

  // Init WiFi in station mode (required for ESP-NOW)
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  Serial.print("[CTRL] MAC: ");
  Serial.println(WiFi.macAddress());

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("[CTRL] ESP-NOW init FAILED");
    return;
  }
  esp_now_register_send_cb(onSent);

  // Register receiver as peer
  memcpy(peerInfo.peer_addr, RECEIVER_MAC, 6);
  peerInfo.channel = 0; // use current channel
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) == ESP_OK) {
    peerAdded = true;
    Serial.println("[CTRL] Peer added OK");
  } else {
    Serial.println("[CTRL] Failed to add peer");
  }

  Serial.println("[CTRL] Ready — press buttons to drive");
}

void loop() {
  if (!peerAdded) return;

  unsigned long now = millis();
  if (now - lastSend < SEND_INTERVAL) return;
  lastSend = now;

  // Read buttons (LOW = pressed due to INPUT_PULLUP)
  bool fwd   = !digitalRead(PIN_FWD);
  bool back  = !digitalRead(PIN_BACK);
  bool left  = !digitalRead(PIN_LEFT);
  bool right = !digitalRead(PIN_RIGHT);
  bool turbo = !digitalRead(PIN_TURBO);

  // Build packet
  packet.forward = 0;
  packet.turn = 0;
  packet.turbo = turbo ? 1 : 0;
  packet.estop = 0;

  if (fwd && !back)       packet.forward = 1;
  else if (back && !fwd)  packet.forward = -1;

  if (left && !right)     packet.turn = -1;
  else if (right && !left) packet.turn = 1;

  // No buttons at all = stop (not estop, just idle)
  // estop could be triggered by holding both fwd+back simultaneously
  if (fwd && back) {
    packet.forward = 0;
    packet.turn = 0;
    packet.estop = 1;
  }

  // Send
  esp_now_send(RECEIVER_MAC, (uint8_t *)&packet, sizeof(packet));
}
