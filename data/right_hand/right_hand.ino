#include <MPU6050_tockn.h>
#include <Wire.h>
#include <Math.h>
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(2, 3); //2 <-> Tx , 3 <-> Rx

MPU6050 mpu6050(Wire);

long timer = 0;
float accX = 0.0;
float accY = 0.0;
float accZ = 0.0;
float accMag = 0.0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Bluetooth.begin(9600);
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

long count = 0;
void loop() {
  mpu6050.update();

  if(millis() - timer > 10){
    accX = accX / count;
    accY = accY / count;
    accZ = accZ / count;
    accMag = sqrt(pow(accX, 2) + pow(accY, 2) + pow(accZ, 2));
    
//    Serial.println("=======================================================");
//    Serial.print("temp : ");Serial.println(mpu6050.getTemp());
//    Serial.print("accX : ");Serial.print(accX);
//    Serial.print("\taccY : ");Serial.print(accY);
//    Serial.print("\taccZ : ");Serial.println(accZ);
//    
//    Serial.print("angleX : ");Serial.print(mpu6050.getAngleX());
//    Serial.print("\tangleY : ");Serial.print(mpu6050.getAngleY());
//    Serial.print("\tangleZ : ");Serial.println(mpu6050.getAngleZ());
//    Serial.println("=======================================================\n");
    String signalToSend = String((int)(accX*100)) + " " + String((int)(accY*100)) + " " + String((int)(accZ*100)) + " " \
                        + String((int)mpu6050.getAngleX()) + " " + String((int)mpu6050.getAngleY()) + String((int)mpu6050.getAngleZ()) + "\n";
    Serial.print(signalToSend);
    Serial.println(accMag);
//    Bluetooth.print(signalToSend);
    timer = millis();
    accX = 0.0;
    accY = 0.0;
    accZ = 0.0;
    count = 0;
  }
  else {
    accX += mpu6050.getAccX();
    accY += mpu6050.getAccY();
    accZ += mpu6050.getAccZ();
    count++;
  }
}
