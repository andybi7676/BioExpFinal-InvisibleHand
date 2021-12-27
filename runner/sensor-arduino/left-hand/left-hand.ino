// 接線: 
// MPU6050 => VCC(紅) <-> 5V端
//            GND(黑) <-> GND
//            SCL(紫) <-> arduino板A5
//            SDA(藍) <-> arduino板A4

#include <MPU6050_tockn.h>
#include <Wire.h>
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(2, 3); // 2: Tx, 3: Rx

long timer = 0;
MPU6050 mpu6050(Wire);

void setup() {
    Serial.begin(9600);
    Bluetooth.begin(9600);
    Wire.begin();
    mpu6050.begin();
    mpu6050.calcGyroOffsets(true);
}

void loop() {
    mpu6050.update();
    if (millis() - timer > 10) {
//        String newSignal = String((int)mpu6050.getGyroAngleX()) + " " + String((int)mpu6050.getGyroAngleY()) + " " + String((int)mpu6050.getGyroAngleZ()) + " " \
//                         + String((int)mpu6050.getAngleX()) + " " + String((int)mpu6050.getAngleY()) + " " + String((int)mpu6050.getAngleZ()) + "\n";
        String newSignal = String((int)mpu6050.getAngleX()) + " " + String((int)mpu6050.getAngleY()) + " " + String((int)mpu6050.getAngleZ()) + "\n";
        Serial.print(newSignal);
        Bluetooth.print(newSignal);
        timer = millis();
    }
}
