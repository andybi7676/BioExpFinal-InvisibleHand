// 藍芽模組在右手的 arduino 上，所以左手必須將 angle 值送往右手端 
// 注意!!只有 upload code 的時候才用 usb 接到電腦，其他時刻要用右手的 arduino 供電 (避免 Serial 接發受到干擾)
// 接線: 
// MPU6050 => VCC(紅) <-> 麵包板5V端
//            GND(黑) <-> 麵包板GND
//            SCL(紫) <-> arduino板A5
//            SDA(藍) <-> arduino板A4
// Arduino => 5V  用右手 Arduino 供電 (已有接到麵包板正端)
//            GND 也是接到麵包板的接地端 (已接到麵包板負端)
//            Tx(9) 接到右手 Arduino 的 Rx(8)
//            Rx(8) 接到右手 Arduino 的 Tx(9)
#include <MPU6050_tockn.h>
#include <Wire.h>
#include <SoftwareSerial.h>
//SoftwareSerial LeftHand(8, 9); // 8: Rx, 9: Tx

long timer = 0;
MPU6050 mpu6050(Wire);

void setup() {
    Serial.begin(9600);
//    LeftHand.begin(9600);
    Wire.begin();
    mpu6050.begin();
    mpu6050.calcGyroOffsets(true);
}

void loop() {
    mpu6050.update();
    if (millis() - timer > 100) {
        String newSignal = String((int)mpu6050.getAngleX()) + " " + String((int)mpu6050.getAngleY()) + " " + String((int)mpu6050.getAngleZ()) + "\n";
        Serial.print(newSignal);
        timer = millis();
    }
}
