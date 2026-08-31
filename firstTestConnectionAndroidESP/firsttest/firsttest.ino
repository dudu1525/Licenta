#include <WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --- WIFI CREDENTIALS (YOUR PHONE'S HOTSPOT) ---
const char* ssid = "pppaaa";
const char* password = "12345678";
//8sda
//9scl
unsigned long lastTextTime = 0;
// --- OLED SETUP ---
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// --- WEBSOCKET SETUP ---
WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("Disconnected from Phone!");
            break;
        case WStype_CONNECTED:
            Serial.println("Connected to Phone!");
            display.clearDisplay();
            display.setCursor(0,0); 
            display.print("Connected!");
            display.display();
            break;
        case WStype_TEXT:
            // WE RECEIVED TEXT FROM THE AI!
           { String aiText = (char*)payload;
            Serial.println(aiText);
            
            // Print it to the OLED
            display.clearDisplay();
            display.setCursor(0,0);
            display.print(aiText);
            display.display();
             lastTextTime = millis();
            break;}
    }
}

void setup() {
    Serial.begin(115200);

    // 1. Initialize OLED (Pins 8 and 9 on SuperMini C3)
    Wire.begin(8, 9); 
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
        Serial.println(F("OLED allocation failed"));
        for(;;);
    }
    display.clearDisplay();
    display.setTextSize(1); // Small font
    display.setTextColor(SSD1306_WHITE);
    display.setTextWrap(true); // Auto-wrap text to next line!
    display.setCursor(0,0);
    display.print("Connecting Wi-Fi...");
    display.display();

       WiFi.mode(WIFI_STA); // FORCE it into receiver mode
        WiFi.setSleep(false);
    WiFi.disconnect();   // Clear any stuck previous connections
    delay(100);          // Wait a tiny bit
    
    WiFi.begin(ssid, password);
    WiFi.setTxPower(WIFI_POWER_8_5dBm);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    display.clearDisplay();
    display.setCursor(0,0);
    display.print("Wi-Fi Connected!\nLooking for App...");
    display.display();

    // 3. Connect WebSocket to App
    // The phone hotspot router IP is ALWAYS the Gateway IP
    IPAddress gateway = WiFi.gatewayIP();
     Serial.print("Phone's IP Address is: ");
      Serial.println(gateway);
       delay(1000); 
    webSocket.begin(gateway.toString(), 9090, "/");
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(2000);
   // webSocket.enableHeartbeat(15000, 3000, 2);
}

void loop() {
    webSocket.loop(); // Keep the connection alive

        if (lastTextTime > 0 && millis() - lastTextTime > 3000) {
        display.clearDisplay();
        display.display();
        lastTextTime = 0; // Stop it from clearing constantly
         Serial.println("Screen cleared after 3 seconds of silence.");
    }
}