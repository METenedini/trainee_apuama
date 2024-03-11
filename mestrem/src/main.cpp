#include <esp_now.h>
#include <WiFi.h>

uint8_t broadcastAddress[] = {0xD4, 0xD4, 0xDA, 0x5E, 0x07, 0xA0};

typedef struct struct_message {
  char data[200]; 
} struct_message;

struct_message myData;

esp_now_peer_info_t peerInfo;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void setup() {

  Serial.begin(115200);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Transmitted packet
  esp_now_register_send_cb(OnDataSent);

  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  // Add peer
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() {
  // Set values to send
  String mensagem = "{\"TPS\":" + String(random(0, 100)) + ",\"MAP\":" +
                    String(random(0, 100)) + ",\"AirTemp\":" +
                    String(random(0, 100)) + ",\"EngineTemp\":" +
                    String(random(0, 100)) + ",\"ExhaustO2\":" +
                    String(random(0, 2)) + ",\"RPM\":" +
                    String(random(0, 14000)) + ",\"OilTemp\":" +
                    String(random(0, 100)) + ",\"PitLimit\":" +
                    String(random(0, 100)) + ",\"OilPressure\":" +
                    String(random(0, 100)) + ",\"FuelPressure\":" +
                    String(random(0, 100)) + ",\"WaterPressure\":" +
                    String(random(0, 100)) + ",\"Gear\":" +
                    String(random(0, 100)) + "} \n";

  // Copy the content of the string to the struct field
  mensagem.toCharArray(myData.data, sizeof(myData.data));

  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *)&myData, sizeof(myData));

  if (result == ESP_OK) {
    Serial.println("Sent with success");
  } else {
    Serial.println("Error sending the data");
  }
  delay(2000);
}
