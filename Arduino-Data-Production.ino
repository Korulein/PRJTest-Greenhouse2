#include "DHT11.h"

const int LIGHTPIN = A2;   // Pin connected to light sensor (LDR)

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);

  // Initialize the light sensor (LDR) pin
  pinMode(LIGHTPIN, INPUT);
}

void loop() {
  // Read temperature and humidity from DHT11 sensor
  float temperature = DHT11.getTemperature();
  float humidity = DHT11.getHumidity();

  // Read the light level from the LDR sensor 
  int lightLevel = analogRead(LIGHTPIN);

  // Send the temperature, humidity, and light level over the serial port
  Serial.print("T:"); // Prefix for temperature
  Serial.print(temperature); // Temperature value
  Serial.print(", H:"); // Prefix for humidity
  Serial.print(humidity); // Humidity value
  Serial.print(", L:"); // Prefix for light level
  Serial.println(lightLevel); // Light level value

  // Delay before sending the next set of values
  delay(2000); // Send every 2 seconds
}
