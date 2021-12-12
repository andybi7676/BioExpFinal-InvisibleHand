#include <Kalman.h>
#include <Wire.h>
#include <Math.h>
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(2, 3); //2 <-> Tx , 3 <-> Rx

char c = ' ';
float fRad2Deg = 57.295779513f; //將弧度轉為角度的乘數
const int MPU = 0x68; //MPU-6050的I2C地址
const int nValCnt = 7; //一次讀取寄存器的數量

const int nCalibTimes = 1000; //校準時讀數的次數
int calibData[nValCnt]; //校準數據

unsigned long nLastTime = 0; //上一次讀數的時間
float fLastRoll = 0.0f; //上一次濾波得到的Roll角
float fLastPitch = 0.0f; //上一次濾波得到的Pitch角
Kalman kalmanRoll; //Roll角濾波器
Kalman kalmanPitch; //Pitch角濾波器

void setup() {
  Serial.begin(9600); //初始化串口，指定波特率
  Serial.println("ready");
  Bluetooth.begin(9600);
  Wire.begin(); //初始化Wire庫
  WriteMPUReg(0x6B, 0); //啟動MPU6050設備

  Calibration(); //執行校準
  nLastTime = micros(); //記錄當前時間
}

void loop() {
  if(Bluetooth.available())
  {
    c=Bluetooth.read();
    Serial.write(c);
  }
  int readouts[nValCnt];
  ReadAccGyr(readouts); //讀出測量值
  
  float realVals[7];
  Rectify(readouts, realVals); //根據校準的偏移量進行糾正

  //計算加速度向量的模長，均以g為單位
  float fNorm = sqrt(realVals[0] * realVals[0] + realVals[1] * realVals[1] + realVals[2] * realVals[2]);
  float fRoll = GetRoll(realVals, fNorm); //計算Roll角
  if (realVals[1] > 0) {
    fRoll = -fRoll;
  }
  float fPitch = GetPitch(realVals, fNorm); //計算Pitch角
  if (realVals[0] < 0) {
    fPitch = -fPitch;
  }

  //計算兩次測量的時間間隔dt，以秒為單位
  unsigned long nCurTime = micros();
  float dt = (double)(nCurTime - nLastTime) / 1000000.0;
  //對Roll角和Pitch角進行卡爾曼濾波
  float fNewRoll = kalmanRoll.getAngle(fRoll, realVals[4], dt);
  float fNewPitch = kalmanPitch.getAngle(fPitch, realVals[5], dt);
  //跟據濾波值計算角度速
  float fRollRate = (fNewRoll - fLastRoll) / dt;
  float fPitchRate = (fNewPitch - fLastPitch) / dt;
 
 //更新Roll角和Pitch角
  fLastRoll = fNewRoll;
  fLastPitch = fNewPitch;
  //更新本次測的時間
  nLastTime = nCurTime;

  //向串口打印輸出Roll角和Pitch角，運行時在Arduino的串口監視器中查看
  Serial.print("Roll:");
  Serial.print(fNewRoll); Serial.print("(");
  Serial.print(fRollRate); Serial.print("),\tPitch:");
  Serial.print(fNewPitch); Serial.print("(");
  Serial.print(fPitchRate); Serial.print(")\n");
  String sentString = String((int)fNewRoll) + " " + String((int)fNewPitch) + "\n";
  Serial.print(sentString);
  for (int i=0; i<sentString.length(); ++i) {
    char ch = sentString[i];
    Bluetooth.write(ch);
  }
//  Bluetooth.write();
//  Bluetooth.write(" \n");
////  Bluetooth.write();
////  Bluetooth.write('\n');
  delay(20);
}

//向MPU6050寫入一個字節的數據
//指定寄存器地址與一個字節的值
void WriteMPUReg(int nReg, unsigned char nVal) {
  Wire.beginTransmission(MPU);
  Wire.write(nReg);
  Wire.write(nVal);
  Wire.endTransmission(true);
}

//從MPU6050讀出一個字節的數據
//指定寄存器地址，返回讀出的值
unsigned char ReadMPUReg(int nReg) {
  Wire.beginTransmission(MPU);
  Wire.write(nReg);
  Wire.requestFrom(MPU, 1, true);
  Wire.endTransmission(true);
  return Wire.read();
}

//從MPU6050讀出加速度計三個分量、溫度和三個角速度計
//保存在指定的數組中
void ReadAccGyr(int *pVals) {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.requestFrom(MPU, nValCnt * 2, true);
  Wire.endTransmission(true);
  for (long i = 0; i < nValCnt; ++i) {
    pVals[i] = Wire.read() << 8 | Wire.read();
  }
}

//對大量讀數進行統計，校準平均偏移量
void Calibration()
{
  float valSums[7] = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0};
  //先求和
  for (int i = 0; i < nCalibTimes; ++i) {
    int mpuVals[nValCnt];
    ReadAccGyr(mpuVals);
    for (int j = 0; j < nValCnt; ++j) {
      valSums[j] += mpuVals[j];
    }
  }
  //再求平均
  for (int i = 0; i < nValCnt; ++i) {
    calibData[i] = int(valSums[i] / nCalibTimes);
  }
  calibData[2] += 16384; //設芯片Z軸豎直向下，設定靜態工作點。
}

//算得Roll角。算法見文檔。
float GetRoll(float *pRealVals, float fNorm) {
  float fNormXZ = sqrt(pRealVals[0] * pRealVals[0] + pRealVals[2] * pRealVals[2]);
  float fCos = fNormXZ / fNorm;
  return acos(fCos) * fRad2Deg;
}

//算得Pitch角。算法見文檔。
float GetPitch(float *pRealVals, float fNorm) {
  float fNormYZ = sqrt(pRealVals[1] * pRealVals[1] + pRealVals[2] * pRealVals[2]);
  float fCos = fNormYZ / fNorm;
  return acos(fCos) * fRad2Deg;
}

//對讀數進行糾正，消除偏移，並轉換為物理量。公式見文檔。
void Rectify(int *pReadout, float *pRealVals) {
  for (int i = 0; i < 3; ++i) {
    pRealVals[i] = (float)(pReadout[i] - calibData[i]) / 16384.0f;
  }
  pRealVals[3] = pReadout[3] / 340.0f + 36.53;
  for (int i = 4; i < 7; ++i) {
    pRealVals[i] = (float)(pReadout[i] - calibData[i]) / 131.0f;
  }
}
