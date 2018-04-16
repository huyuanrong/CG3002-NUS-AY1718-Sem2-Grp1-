// Constants
const int SENSOR_PIN = 13;  // Input pin for measuring Vout
const float RS = 0.095;          // Shunt resistor value (in ohms)
const int VOLTAGE_REF = 5;  // Reference voltage for analog read

// Global Variables
float sensorValue;   // Variable to store value from analog read
float sensorValue_1;
float current;       // Calculated current value

void setup() {

  // Initialize serial monitor
  Serial.begin(9600);

}

void loop() {
  float avg;
  for (int i = 0; i<10; i++){
    // Read a value from the INA169 board
    sensorValue = analogRead(SENSOR_PIN);
  
    // Remap the ADC value into a voltage number (5V reference)
    sensorValue_1 = (sensorValue * VOLTAGE_REF) / 1023;
    avg += sensorValue_1;
    delay(10);
  }

  avg = avg/10.0;
  // Follow the equation given by the INA169 datasheet to
  // determine the current flowing through RS. Assume RL = 10k
  // Is = (Vout x 1k) / (RS x RL)
  current = avg / (10 * RS);
  // Output value (in amps) to the serial monitor to 3 decimal
  // places
  Serial.print(current, 5);
  Serial.println(" A");
//  Serial.print (sensorValue_1, 5);
//  Serial.println(" V");

  // Delay program for a few milliseconds
  delay(500);

}
