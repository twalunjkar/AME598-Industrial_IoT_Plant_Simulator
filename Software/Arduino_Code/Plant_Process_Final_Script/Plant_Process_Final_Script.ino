// Including All Required Libraries
#include <Ultrasonic.h>                                 // Library for ultrasonic sensor
#include <OneWire.h>                                    // Library for temperature sensor
#include <DallasTemperature.h>                          // Library for temperature sensor

// Board Pin Definitions
#define PUMP1_PIN 2                                     // Pin for controlling pump 1
#define PUMP2_PIN 4                                     // Pin for controlling pump 2
#define HEATER_PIN 6                                    // Pin for controlling heater
#define ULTRASONIC_TRIG_PIN 7                           // Ultrasonic sensor trigger pin
#define ULTRASONIC_ECHO_PIN 8                           // Ultrasonic sensor echo pin
#define TEMP_SENSOR_PIN 9                               // Temperature sensor pin

// Global Constants
#define MAX_LEVEL 30                                    // Maximum liquid level (in centimeters)
#define MIN_LEVEL 10                                    // Minimum liquid level (in centimeters)
#define TEMPERATURE_SETPOINT 25                         // Temperature setpoint in degrees Celsius

// PID parameters for Pump 1
double kp1 = 1.0;                                       // Proportional gain for Pump 1
double ki1 = 0.1;                                       // Integral gain for Pump 1
double kd1 = 0.01;                                      // Derivative gain for Pump 1

// PID parameters for Pump 2
double kp2 = 1.0;                                       // Proportional gain for Pump 2
double ki2 = 0.1;                                       // Integral gain for Pump 2
double kd2 = 0.01;                                      // Derivative gain for Pump 2

// Variables
double previousError1 = 0;
double integral1 = 0;
double previousError2 = 0;
double integral2 = 0;

// Objects
Ultrasonic ultrasonic(ULTRASONIC_TRIG_PIN, ULTRASONIC_ECHO_PIN);  // Ultrasonic sensor object
OneWire oneWire(TEMP_SENSOR_PIN);                                 // OneWire object for temperature sensor
DallasTemperature tempSensor(&oneWire);                           // Temperature sensor object

// ------------------------------------------------------------------------------------------------------------ // 

void setup() {

  pinMode(PUMP1_PIN, OUTPUT);                           // Initialize pins                           
  pinMode(PUMP2_PIN, OUTPUT);
  pinMode(HEATER_PIN, OUTPUT);

  Serial.begin(9600);                                   // Initiate Serial Communication

  tempSensor.begin();                                   // Initialize Temperature Sensor
}

// ------------------------------------------------------------------------------------------------------------ // 

void loop() {
  
  float level = getLiquidLevel();                       // Read ultrasonic sensor to get the liquid level

  float temperature = getTemperature();                 // Read temperature from the sensor

  controlPumps(level);                                  // Control pumps based on the liquid level

  controlHeater(temperature);                           // Control heater based on temperature setpoint

  Serial.print("Liquid Level: ");                       
  Serial.print(level);
  Serial.print(" cm, Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  delay(1000);                                          // Delay for 1 second
}

// ------------------------------------------------------------------------------------------------------------ // 

float getLiquidLevel() {
  return ultrasonic.read();                             // Measure distance using ultrasonic sensor
}

float getTemperature() {

  tempSensor.requestTemperatures();                     // Request temperature from the temperature sensor

  return tempSensor.getTempCByIndex(0);                 // Read and return the temperature in Celsius
}


void controlPumps(double output1, double output2) {

  analogWrite(PUMP1_PIN, output1);                      // Set output value at pin for pump
  analogWrite(PUMP2_PIN, output2);
}

void controlHeater(float temperature) {
  if (temperature < TEMPERATURE_SETPOINT) {
    digitalWrite(HEATER_PIN, HIGH);
  } else {
    digitalWrite(HEATER_PIN, LOW);
  }
}

double pidControl(double error, double kp, double ki, double kd, double &integral) {
  double proportional = kp * error;
  integral += ki * error;
  double derivative = kd * (error - previousError1);
  double output = proportional + integral + derivative;
  previousError1 = error;
  return output;
}