#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 12 // Pin D12 on Arduino Nano 33 BLE
#define RELAY_PIN 18    // Pin D18 for LILYGO relay
#define LED_PIN 13

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

const int lowerTemp = 20; // Below this temp, turn on the relay
const int upperTemp = 25; // Above this temp, turn off the relay

void setup() {
  Serial.begin(9600);
  sensors.begin();
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  sensors.requestTemperatures(); // Send the command to get temperatures

  float temperatureC = sensors.getTempCByIndex(0); // Index 0 since there's only one sensor

  if (temperatureC != DEVICE_DISCONNECTED_C) {
    Serial.print("Temperature: ");
    Serial.print(temperatureC);
    Serial.println(" °C");

    if (temperatureC < lowerTemp) {
      digitalWrite(RELAY_PIN, HIGH); // Turn on relay when temperature is below 20°C
      digitalWrite(LED_PIN, LOW);    // Optional: Turn on LED for indication
    } else if (temperatureC >= upperTemp) {
      digitalWrite(RELAY_PIN, LOW); // Turn off relay when temperature is above 25°C
      digitalWrite(LED_PIN, HIGH);  // Optional: Turn off LED for indication
    } else {
      // Optional: Add code here for the temperature range between 20°C and 25°C
    }
  } else {
    Serial.println("Error reading temperature!");
  }

  delay(1000); // Delay for a second before reading again
}
