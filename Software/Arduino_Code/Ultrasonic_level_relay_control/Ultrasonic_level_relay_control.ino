#include <Arduino.h>
#include <Ultrasonic.h>

// Define the pins
const int trigPin = 12;  // GPIO12 on LilyGO ESP32 Relay
const int echoPin = 14;  // GPIO14 on LilyGO ESP32 Relay
const int relayPin = 5; // GPIO32 on LilyGO ESP32 Relay

// Variables for duration, distance, and threshold values
long duration;
int distance;
const int lowerThreshold = 12; // Below this distance, turn on the relay
const int upperThreshold = 15; // Above this distance, turn off the relay

// Create an Ultrasonic object
Ultrasonic ultrasonic(trigPin, echoPin);

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Set relayPin as OUTPUT
  pinMode(relayPin, OUTPUT);

  // Some initial delay for stability
  delay(1000);
}

void loop() {
  // Measure the distance using the Ultrasonic sensor
  distance = ultrasonic.read();

  // Print the distance to the Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Control the relay based on the distance
  if (distance < lowerThreshold) {
    // If distance is below the lower threshold, turn on the relay
    digitalWrite(relayPin, HIGH);
  } else if (distance > upperThreshold) {
    // If distance is above the upper threshold, turn off the relay
    digitalWrite(relayPin, LOW);
  }

  // Wait for a short time before taking the next measurement
  delay(500);
}
