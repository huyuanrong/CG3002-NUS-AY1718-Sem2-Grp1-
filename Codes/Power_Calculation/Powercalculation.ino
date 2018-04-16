// Global Variables
float voltageValue;
float currentValue;                  
float powerValue;
float energyValue;

const float RS = 0.095;          // Shunt resistor value (in ohms)
const int VOLTAGE_REF = 5;  // Reference voltage for analog read

unsigned long timePrev;
unsigned long timeCurr;
unsigned long timeDiff;

void setup()
{
    Serial.begin(9600);
}

void loop(){
    timePrev = micros();
    voltageValue = analogRead(A15);
    currentValue = analogRead(A14);
    
    currentValue = (currentValue * VOLTAGE_REF) / 1023.0;        
    voltageValue = ((voltageValue * VOLTAGE_REF) / 1023.0 )* 2.0);
    
    powerValue = voltageValue * currentValue;

    timeCurr = micros();
    timeDiff = timeCurr - timePrev;
    energyValue += powerValue * (timeDiff / 1000000 / 3600);
    
    Serial.print("Voltage: ");
    Serial.print(voltageValue);
    Serial.println (" V");
    Serial.print("Current: ");
    Serial.print(currentValue, 5);
    Serial.println(" A");
    Serial.print("Power: ");
    Serial.print(powerValue);
    Serial.println(" W");
    Serial.print("Energy: ");
    Serial.print(energyValue);
    Serial.println( "J");
}
