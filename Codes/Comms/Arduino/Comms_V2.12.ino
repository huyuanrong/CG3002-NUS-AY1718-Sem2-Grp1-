#include <Arduino_FreeRTOS.h>
#include <semphr.h>
#include <Wire.h>
#include <stdlib.h>

/*---Analog accelerometers pins---*/

#define pinX0 A0
#define pinY0 A1
#define pinZ0 A2

#define pinX1 A3
#define pinY1 A4
#define pinZ1 A5

const int MPU_addr = 0x68; // I2C address of the MPU-6050

//Function Headers
void establishHandshake();
void readSensors();
void processSensors();
void processPower();
void createMessage();
void mainTask(void *pv);

//Constants
const float Vref = 5;
const float zero_G = 1.65;
const float zero_G_Z = 1.7; // 0g value voltage for ADXL335
const float sensitivity = 0.33; //ADXL335 sensitivity is 330mV/g
const float scale = 102.3;  //ADXL335330 Sensitivity is 330mv/g
//330 * 1024/3.3/1000
const float digAccSens = 16384.0;
const float digGyroSens = 131.0;

/*--- Global Variables ---*/

int startFlag = 0;
int ackFlag = 0;

//Variables for reading & processing sensor values
float xLeft, yLeft, zLeft, xRight, yRight, zRight;
float xLeft_f, yLeft_f, zLeft_f, xRight_f, yRight_f, zRight_f; //For processing
int16_t dAccX, dAccY, dAccZ, Tmp, gyX, gyY, gyZ;
float dAccX_f, dAccY_f, dAccZ_f, gyX_f, gyY_f, gyZ_f; //For processing

//Variables for reading and processing power values
float voltageValue;
float currentValue;
float powerValue;
float energyValue;

const float RS = 0.095;          // Shunt resistor value (in ohms)
const int VOLTAGE_REF = 5;  // Reference voltage for analog read

unsigned long timePrev;
unsigned long timeCurr;
unsigned long timeDiff;

//Variables for creating message string
char xLeft_c[5], yLeft_c[5], zLeft_c[5]; //Left Analog Acc
char xRight_c[5], yRight_c[5], zRight_c[5]; //Right Analog Acc
char dAccX_c[5], dAccY_c[5], dAccZ_c[5]; //Digital Acc
char gyX_c[5], gyY_c[5], gyZ_c[5]; //Digital Gyro
char volt_c[5], current_c[5], power_c[5], energy_c[5]; //Power
char dataBuffer[3000];

//Checksum
int checksum = 0;
int checksum2;
char checksum_c[4];

/*Initial power up or reset state*/
void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial.println("S: Initializing...");

  //Set up Digital Accelerometer and Gyroscope
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  //Start Handshake
  establishHandshake();

  //Create task to be run
  xTaskCreate(mainTask, "main", 400, NULL, 2, NULL);
  //Start Scheduler
  vTaskStartScheduler();
  Serial.println("S: Initializing done...");
}

void establishHandshake() {
  while (startFlag == 0) {
    if (Serial1.available()) {
      if (Serial1.read() == 'H') {
        Serial.println("EH: Received handshake!");
        startFlag = 1;
        Serial1.write('A');
      }
    }
  }

  while (ackFlag == 0) {
    if (Serial1.available()) {
      if (Serial1.read() == 'A') {
        ackFlag = 1;
      }
    } else {
      Serial1.write('A');
    }
  }
  Serial.println("EH: Handshake established!");
}

void loop() {};

/*--- Auxillary functions ---*/

//Sensor functions

void readSensors() {
  //Serial.println("RS: Reading sensor values...");
  xLeft = analogRead(pinX0);
  yLeft = analogRead(pinY0);
  zLeft = analogRead(pinZ0);

  xRight = analogRead(pinX1);
  yRight = analogRead(pinY1);
  zRight = analogRead(pinZ1);

  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers

  dAccX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  dAccY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  dAccZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  gyX = Wire.read() << 8 | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  gyY = Wire.read() << 8 | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  gyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

void processSensors() {
  //Serial.println("PS: Processing sensor values...");
  //For quicker reference
  //sensitivity = 0.33 | zero_G = 1.65 | zero_G_Z = 1.7 | digAccSens = 16384.0 | digGyroSens = 131.0
  xLeft_f = ((xLeft * Vref / 1023) - zero_G) / sensitivity;
  yLeft_f = ((yLeft * Vref / 1023) - zero_G) / sensitivity;
  zLeft_f = ((zLeft * Vref / 1023) - zero_G_Z) / sensitivity;

  xRight_f = ((xRight * Vref / 1023) - zero_G) / sensitivity;
  yRight_f = ((yRight * Vref / 1023) - zero_G) / sensitivity;
  zRight_f = ((zRight * Vref / 1023) - zero_G_Z) / sensitivity;

  dAccX_f = dAccX / digAccSens;
  dAccY_f = dAccY / digAccSens;
  dAccZ_f = dAccZ / digAccSens;

  gyX_f = gyX / digGyroSens;
  gyY_f = gyY / digGyroSens;
  gyZ_f = gyZ / digGyroSens;

//    Serial.print("Left X: ");
//    Serial.print(xLeft_f);
//    Serial.print("|Left Y: ");
//    Serial.print(yLeft_f);
//    Serial.print("|Left Z: ");
//    Serial.println(zLeft_f);
//  
//    Serial.print("Right X: ");
//    Serial.print(xRight_f);
//    Serial.print("|Right Y: ");
//    Serial.print(yRight_f);
//    Serial.print("|Right Z: ");
//    Serial.println(zRight_f);
//  
//    Serial.print("Digtal X: ");
//    Serial.print(dAccX_f);
//    Serial.print("|Digital Y: ");
//    Serial.print(dAccY_f);
//    Serial.print("|Digital Z: ");
//    Serial.println(dAccZ_f);
//  
//    Serial.print("Gyro X: ");
//    Serial.print(gyX_f);
//    Serial.print("|Gyro Y: ");
//    Serial.print(gyY_f);
//    Serial.print("|Gyro Z: ");
//    Serial.println(gyZ_f);
}

//Power function

void processPower() {
  Serial.println("PP: Processing power values...");
  voltageValue = analogRead(A15);
  currentValue = analogRead(A14);

  currentValue = (currentValue * VOLTAGE_REF) / 1023.0;
  voltageValue = ((voltageValue * VOLTAGE_REF) / 1023.0 ) * 2.0;

  powerValue = voltageValue * currentValue;

  timeCurr = micros();
  timeDiff = timeCurr - timePrev;
  energyValue += powerValue * timeDiff / 1000000.0 / 3600.0;

//    Serial.print("Voltage: ");
//    Serial.print(voltageValue);
//    Serial.println (" V");
//    Serial.print("Current: ");
//    Serial.print(currentValue, 5);
//    Serial.println(" A");
//    Serial.print("Power: ");
//    Serial.print(powerValue);
//    Serial.println(" W");
//    Serial.print("Energy: ");
//    Serial.print(energyValue);
//    Serial.println( "J");
}

//Format message

void createMessage() {
  Serial.println("CM: Creating string...");

  //Concat sensor values to dataBuffer

  //Left Analog Acc
  dtostrf(xLeft_f, 3, 2, xLeft_c);
  strcat(dataBuffer, xLeft_c);
  strcat(dataBuffer, ",");
  (dtostrf(yLeft_f, 3, 2, yLeft_c));
  strcat(dataBuffer, yLeft_c);
  strcat(dataBuffer, ",");
  (dtostrf(zLeft_f, 3, 2, zLeft_c));
  strcat(dataBuffer, zLeft_c);
  strcat(dataBuffer, ",");

  //Right Analog Acc
  (dtostrf(xRight_f, 3, 2, xRight_c));
  strcat(dataBuffer, xRight_c);
  strcat(dataBuffer, ",");
  (dtostrf(yRight_f, 3, 2, yRight_c));
  strcat(dataBuffer, yRight_c);
  strcat(dataBuffer, ",");
  (dtostrf(zRight_f, 3, 2, zRight_c));
  strcat(dataBuffer, zRight_c);
  strcat(dataBuffer, ",");

  //Digital Acc
  (dtostrf(dAccX_f, 3, 2, dAccX_c));
  strcat(dataBuffer, dAccX_c);
  strcat(dataBuffer, ",");
  (dtostrf(dAccY_f, 3, 2, dAccY_c));
  strcat(dataBuffer, dAccY_c);
  strcat(dataBuffer, ",");
  (dtostrf(dAccZ_f, 3, 2, dAccZ_c));
  strcat(dataBuffer, dAccZ_c);
  strcat(dataBuffer, ",");

  //Digital Gyro
  (dtostrf(gyX_f, 3, 2, gyX_c));
  strcat(dataBuffer, gyX_c);
  strcat(dataBuffer, ",");
  (dtostrf(gyY_f, 3, 2, gyY_c));
  strcat(dataBuffer, gyY_c);
  strcat(dataBuffer, ",");
  (dtostrf(gyZ_f, 3, 2, gyZ_c));
  strcat(dataBuffer, gyZ_c);
  strcat(dataBuffer, ",");

  //Concat power readings to dataBuffer
  dtostrf(voltageValue, 4, 3, volt_c);
  strcat(dataBuffer, volt_c);
  strcat(dataBuffer, ",");
  dtostrf(currentValue, 4, 3, current_c);
  strcat(dataBuffer, current_c);
  strcat(dataBuffer, ",");
  dtostrf(powerValue, 4, 3, power_c);
  strcat(dataBuffer, power_c);
  strcat(dataBuffer, ",");
  dtostrf(energyValue, 4, 3, energy_c);
  strcat(dataBuffer, energy_c); 
}

/* --- Tasks --- */

void mainTask(void *pv) {
  //Serial.println("MT: In Main task");
  int readByte = 0;
  unsigned int frameNum = 1;
  char frameNum_c[4];
  unsigned int len;
  TickType_t xLastWakeTime;

  xLastWakeTime = xTaskGetTickCount();

  while (1) {
    if (Serial1.available()) {
      readByte = Serial1.read();
    }
    if (readByte == 'D') {
      //xLastWakeTime = xTaskGetTickCount();

      //Clear the dataBuffer
      strcpy(dataBuffer, "");

      //Add frame number
      itoa(frameNum, frameNum_c, 10);
      strcpy(dataBuffer, frameNum_c);
      strcat(dataBuffer, ",");
      //Read power readings
      processPower();
      //Read sensors
      readSensors();
      
      timePrev = micros();
      //Process sensors
      processSensors();
      //Create the message string to send to Pi3
      createMessage();

      //Append the checksum
      len = strlen(dataBuffer);
      for (int j = 0; j < len; j++) {
        checksum ^= dataBuffer[j];
      }
      checksum2 = (int)checksum;
      itoa(checksum2, checksum_c, 10);
      strcat(dataBuffer, ",");
      strcat(dataBuffer, checksum_c);

      len = strlen(dataBuffer);
      dataBuffer[len + 1] = '\n';
      int k = 0;

      //Send the message string
      while (k < len + 2) {
        Serial1.write(dataBuffer[k]);
        k++;
      }
      //Serial.print(dataBuffer);

      frameNum++;
      readByte = 0;
      checksum = 0;
    }
  }
}

