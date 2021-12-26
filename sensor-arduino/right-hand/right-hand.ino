#include <MPU6050_tockn.h>
#include <Wire.h>
#include <Math.h>
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(2, 3); //2 <-> Tx , 3 <-> Rx
//SoftwareSerial LeftHand(8, 9); //8 <-> Tx, 9 <-> Rx

MPU6050 mpu6050(Wire);

long  timer = 0;
float accX = 0.0;
float accY = 0.0;
float accZ = 0.0;
float accMag = 0.0;
char l = ' ';
String l_signal = "";
int leftHandAngles[3] = {0, 0, 0}; // index 0 -> x, index 1 -> y, index 2 -> z

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Bluetooth.begin(9600);
//  LeftHand.begin(9600);
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  while (Serial.available()) {
    l = Serial.read();
    if (l == '\n') break;
  }
}

long count = 0;
void loop() {
  mpu6050.update();

  if (millis() - timer > 10) {
    accX = accX / count;
    accY = accY / count;
    accZ = accZ / count;
    accMag = sqrt(pow(accX, 2) + pow(accY, 2) + pow(accZ, 2));
    
    String signalToSend = String((int)(accX*1000)) + " " + String((int)(accY*1000)) + " " + String((int)(accZ*1000)) + " " \
                        + String((int)mpu6050.getAngleX()) + " " + String((int)mpu6050.getAngleY()) + " " + String((int)mpu6050.getAngleZ()) + " " \
                        + String(leftHandAngles[0]) + " " + String(leftHandAngles[1]) + " " + String(leftHandAngles[2]) + "\n";
    Serial.print(signalToSend);
    Bluetooth.print(signalToSend);
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
  if (Serial.available()) {
    l = Serial.read();
    l_signal += l;
    if (l == '\n') {
      Serial.print(l_signal);
      parseLeftHandSignal();
      l_signal = "";
    }
  }
}

void parseLeftHandSignal() {
  int start = 0;
  int index = 0;
  for (int e=0; e<l_signal.length(); ++e) {
    if (l_signal[e] == ' ' || l_signal[e] == '\n') {
      leftHandAngles[index] = l_signal.substring(start, e).toInt();
      index++;
      start = e+1;
    }
  }
}
