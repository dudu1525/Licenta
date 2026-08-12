#include <driver/i2s_std.h>
#include <math.h>

#define I2S_BCLK 4
#define I2S_WS   5
#define I2S_DIN  6

#define LED_PIN 8

i2s_chan_handle_t rx_handle;

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);   // LED OFF

  Serial.println("INMP441 RMS TEST");

  i2s_chan_config_t chan_cfg =
      I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);

  i2s_new_channel(&chan_cfg, NULL, &rx_handle);

  i2s_std_config_t std_cfg = {
    .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),

    .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(
      I2S_DATA_BIT_WIDTH_32BIT,
      I2S_SLOT_MODE_MONO
    ),

    .gpio_cfg = {
      .mclk = I2S_GPIO_UNUSED,
      .bclk = (gpio_num_t)I2S_BCLK,
      .ws   = (gpio_num_t)I2S_WS,
      .dout = I2S_GPIO_UNUSED,
      .din  = (gpio_num_t)I2S_DIN
    }
  };

  // L/R connected to GND = LEFT
  std_cfg.slot_cfg.slot_mask = I2S_STD_SLOT_LEFT;

  i2s_channel_init_std_mode(rx_handle, &std_cfg);
  i2s_channel_enable(rx_handle);

  Serial.println("Microphone ready!");
}

void loop() {

  int32_t samples[512];
  size_t bytes_read = 0;

  i2s_channel_read(
    rx_handle,
    samples,
    sizeof(samples),
    &bytes_read,
    100
  );

  int count = bytes_read / sizeof(int32_t);

  // Calculate DC offset
  double mean = 0;

  for (int i = 0; i < count; i++) {
    double sample = samples[i] >> 8;
    mean += sample;
  }

  mean /= count;

  // Calculate RMS of actual AC audio signal
  double sumSquares = 0;

  for (int i = 0; i < count; i++) {
    double sample = (samples[i] >> 8) - mean;
    sumSquares += sample * sample;
  }

  double rms = sqrt(sumSquares / count);

  Serial.print("RMS: ");
  Serial.println(rms);

  delay(100);
}