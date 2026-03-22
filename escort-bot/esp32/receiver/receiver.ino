/*
 * ESP-NOW Receiver — Escort Bot
 * ===============================
 * ESP32-CAM #2: Mounted on robot chassis.
 * Receives drive commands via ESP-NOW, forwards to Pi 5 over Serial (UART).
 *
 * WIRING TO PI 5:
 *   ESP32-CAM GPIO 1 (U0TXD) → Pi 5 GPIO 15 (RXD)
 *   ESP32-CAM GPIO 3 (U0RXD) → Pi 5 GPIO 14 (TXD)  [optional, for Pi→ESP32]
 *   ESP32-CAM GND             → Pi 5 GND
 *
 *   *** 3.3V logic on both sides — no level shifter needed ***
 *
 * SERIAL PROTOCOL (to Pi 5):
 *   Sends CSV line at 20Hz: "forward,turn,turbo,estop\n"
 *   Examples:
 *     "1,0,0,0\n"   → forward, straight, normal speed
 *     "1,-1,1,0\n"  → forward+left, turbo
 *     "0,0,0,0\n"   → idle/stop
 *     "0,0,0,1\n"   → emergency stop
 *     "-1,1,0,0\n"  → reverse+right
 *
 * SAFETY:
 *   - If no packet received for 500ms, sends stop command automatically
 *   - Emergency stop (estop=1) locks motors until cleared
 *
 * SETUP:
 *   1. Flash get_mac.ino first to find THIS board's MAC address
 *   2. Put that MAC in controller.ino's RECEIVER_MAC
 *   3. Flash this sketch to receiver board
 *   4. Disconnect from programmer, wire to Pi 5 UART
 */

#include <esp_now.h>
#include <WiFi.h>

// Command packet — must match controller struct exactly
typedef struct {
  int8_t forward;  // -1 back, 0 stop, 1 forward
  int8_t turn;     // -1 left, 0 straight, 1 right
  uint8_t turbo;   // 0 normal, 1 turbo
  uint8_t estop;   // 0 normal, 1 emergency stop
} ControlPacket;

ControlPacket lastPacket;
volatile bool newData = false;
unsigned long lastReceived = 0;

// Timeout — if controller goes silent, stop the bot
#define TIMEOUT_MS 500

void onReceive(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  if (len == sizeof(ControlPacket)) {
    memcpy(&lastPacket, data, sizeof(ControlPacket));
    newData = true;
    lastReceived = millis();
  }
}

void sendToPi(int8_t fwd, int8_t turn, uint8_t turbo, uint8_t estop) {
  // CSV format: forward,turn,turbo,estop
  Serial.print(fwd);
  Serial.print(',');
  Serial.print(turn);
  Serial.print(',');
  Serial.print(turbo);
  Serial.print(',');
  Serial.println(estop);
}

void setup() {
  // Serial to Pi 5 — 115200 baud, 8N1
  // GPIO 1 (TX) and GPIO 3 (RX) are the default UART0 pins
  Serial.begin(115200);

  // Brief startup message (Pi can ignore or use for handshake)
  Serial.println("ESP-NOW-RX:BOOT");

  // Onboard LED
  pinMode(33, OUTPUT);
  digitalWrite(33, HIGH); // off

  // Init WiFi + ESP-NOW
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Print MAC so user can copy it for controller sketch
  // This goes to Serial (which is also the Pi connection)
  // Pi-side code should ignore lines starting with '#'
  Serial.print("# Receiver MAC: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println("# ESP-NOW init FAILED");
    return;
  }

  esp_now_register_recv_cb(onReceive);

  Serial.println("ESP-NOW-RX:READY");

  // Zero out packet
  memset(&lastPacket, 0, sizeof(lastPacket));
  lastReceived = millis();
}

void loop() {
  unsigned long now = millis();

  // New command from controller
  if (newData) {
    newData = false;
    sendToPi(lastPacket.forward, lastPacket.turn, lastPacket.turbo, lastPacket.estop);

    // Blink LED on receive
    digitalWrite(33, LOW);
    delay(5);
    digitalWrite(33, HIGH);
  }

  // Safety timeout — no signal from controller
  if (now - lastReceived > TIMEOUT_MS) {
    // Send stop every 200ms while timed out
    static unsigned long lastTimeout = 0;
    if (now - lastTimeout > 200) {
      lastTimeout = now;
      sendToPi(0, 0, 0, 0); // idle stop
      Serial.println("# TIMEOUT — no controller signal");
    }
  }

  // Check if Pi sent anything back (optional bidirectional)
  // Pi can send "ESTOP\n" or "OK\n" etc.
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    // Could relay Pi commands back to controller via ESP-NOW
    // For now, just acknowledge
    if (cmd == "PING") {
      Serial.println("PONG");
    }
  }
}
