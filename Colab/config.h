#ifndef CONFIG_H
#define CONFIG_H

#include <WiFi.h>
#include <PubSubClient.h>

// ==========================
// WiFi credentials
// ==========================
const char *ssid = "YOUR_WIFI_SSID";         // <-- Replace safely
const char *password = "YOUR_WIFI_PASSWORD"; // <-- Replace safely

// ==========================
// MQTT settings
// ==========================
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "esp32/test";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

// ==========================
// Sensor Pin Definitions
// ==========================
const int mq2 = 32;
const int mq4 = 34;
const int mq135 = 35;

#endif
