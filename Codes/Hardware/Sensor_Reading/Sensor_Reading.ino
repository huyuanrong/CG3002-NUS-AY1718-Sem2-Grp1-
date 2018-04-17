#include<Wire.h>
const int leftXPin = 0;                  // x-axis of the accelerometer
const int leftYPin = 1;                  // y-axis
const int leftZPin = 2;                  // z-axis (only on 3-axis models)
const int rightXPin = 3;
const int rightYPin = 4;
const int rightZPin = 5;

float Vref = 5;
float zero_G = 1.65;
float zero_G_Z = 1.7; // 0g value voltage for ADXL335
float sensitivity = 0.33; //ADXL335 sensitivity is 330mV/g
float scale = 102.3;  //ADXL335330 Sensitivity is 330mv/g
                       //330 * 1024/3.3/1000  

const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

void setup()
{
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(9600);
}

void loop()
{
  //Analog
  float leftX = analogRead(leftXPin);  //read from xpin
  float leftY = analogRead(leftYPin);  //read from ypin
  float leftZ = analogRead(leftZPin);  //read from zpin
  float rightX = analogRead(rightXPin);
  float rightY = analogRead(rightYPin);
  float rightZ = analogRead(rightZPin);
  
  //digital 
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  //printing of values
  Serial.print("Left X Value: ");
  Serial.println(((leftX*Vref/1023) - zero_G)/sensitivity);
  Serial.print("Left Y Value: ");
  Serial.println(((leftY*Vref/1023) - zero_G)/sensitivity);
  Serial.print("Left Z Value: ");
  Serial.println(((leftZ*Vref/1023) - zero_G_Z)/sensitivity);
  Serial.print("Right X Value: ");
  Serial.println(((rightX*Vref/1023) - zero_G)/sensitivity);
  Serial.print("Right Y Value: ");
  Serial.println(((rightY*Vref/1023) - zero_G)/sensitivity);
  Serial.print("Right Z Value: ");
  Serial.println(((rightZ*Vref/1023) - zero_G_Z)/sensitivity);
  
  Serial.print("AcX = "); Serial.print(AcX/16384.0);
  Serial.print(" | AcY = "); Serial.print(AcY/16384.0);
  Serial.print(" | AcZ = "); Serial.print(AcZ/16384.0);
  Serial.print(" | GyX = "); Serial.print(GyX/131.0);
  Serial.print(" | GyY = "); Serial.print(GyY/131.0);
  Serial.print(" | GyZ = "); Serial.println(GyZ/131.0);

  delay(1000);
}
