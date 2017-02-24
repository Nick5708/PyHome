#include <ESP8266WiFi.h>

const char* ssid = "PIM77";
const char* password = "19771016";

const uint16_t port = 80;
const char* host = "194.87.237.49"; // ip or dns

String data;


void setup() {
    Serial.begin(115200);
    delay(10);
    Serial.println();
    Serial.print("Wait for WiFi... ");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    delay(500);
    
}


void loop() {
    Serial.print("connecting to ");
    Serial.println(host);
    WiFiClient client;

    if (!client.connect(host, port)) {
        Serial.println("connection failed");
        Serial.println("wait 5 sec...");
        delay(5000);
        return;
    }
    data = String(analogRead(A0) * 10);
    client.print("GET /data" + data + " HTTP/1.1 \r\n");
    client.print("Host: 0.0.0.0 \r\n");
    client.print("User-Agent: ESP8266/1.0 \r\n");
    client.print("\r\n");
    
    Serial.println("wait ...");
    delay(random(40000,60000));
    client.stop();
}

