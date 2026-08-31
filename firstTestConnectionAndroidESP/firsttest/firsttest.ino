#include <WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <driver/i2s.h>

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

#define I2S_WS 3
#define I2S_SCK 4
#define I2S_SD 5
#define I2S_PORT I2S_NUM_0


// --- WEBSOCKET SETUP ---
WebSocketsClient webSocket;

void setupI2S() {///////////////////////////////////////////////
    const i2s_config_t i2s_config = {
        .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = 16000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_STAND_I2S),
        .intr_alloc_flags = 0,
        .dma_buf_count = 8,
        .dma_buf_len = 64,
        .use_apll = false
    };
    i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);

    const i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_SCK,
        .ws_io_num = I2S_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = I2S_SD
    };
    i2s_set_pin(I2S_PORT, &pin_config);
}

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

        setupI2S();////////////////////////////////////////////////////////////////



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

       // RECORD AUDIO AND SEND TO PHONE////////////////////////////////////////////////////////
    if (webSocket.isConnected()) {
        int16_t audioBuffer[512]; // Create a bucket for audio
        size_t bytesRead = 0;
        
        // Fill the bucket from the Mic
        esp_err_t result = i2s_read(I2S_PORT, &audioBuffer, sizeof(audioBuffer), &bytesRead, portMAX_DELAY);
        
        // If bucket is full, throw it to the phone!
        if (result == ESP_OK && bytesRead > 0) {
            webSocket.sendBIN((uint8_t*)audioBuffer, bytesRead);
        }
    }


}