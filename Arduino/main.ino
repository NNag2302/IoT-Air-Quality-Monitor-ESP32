#include "config.h"
#include "sensor.h"

WiFiClient espClient;
PubSubClient client(espClient);

// ==========================
// Setup
// ==========================
void setup() {
  Serial.begin(9600);

  pinMode(mq2, INPUT);
  pinMode(mq4, INPUT);
  pinMode(mq135, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  mqttConnect();
}

// ==========================
// Main Loop
// ==========================
void loop() {
  client.loop();

  double mq2_value   = analogToVoltage(analogRead(mq2));
  double mq4_value   = analogToVoltage(analogRead(mq4));
  double mq135_value = analogToVoltage(analogRead(mq135));

  char output[15];

  dtostrf(mq2_value,   6, 3, output); client.publish("MQ2",   output);
  dtostrf(mq4_value,   6, 3, output); client.publish("MQ4",   output);
  dtostrf(mq135_value, 6, 3, output); client.publish("MQ135", output);

  Serial.println();
  Serial.print("MQ-2 Voltage: ");   Serial.println(mq2_value);
  Serial.print("MQ-4 Voltage: ");   Serial.println(mq4_value);
  Serial.print("MQ-135 Voltage: "); Serial.println(mq135_value);
  Serial.println();

  delay(3000);
}

// ==========================
// MQTT Connection Function
// ==========================
void mqttConnect() {
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  while (!client.connected()) {
    String client_id = "esp32-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("Connecting to MQTT broker as %s...\n", client_id.c_str());

    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT broker.");
    } else {
      Serial.print("Failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  client.publish(topic, "ESP32 connected with MQ sensors!");
  client.subscribe(topic);
}

// ==========================
// MQTT Callback
// ==========================
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);

  Serial.print("Message: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println("\n-----------------------");
}
