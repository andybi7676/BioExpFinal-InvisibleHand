// 如果arduino插電腦，L298N接地然後12V要接arduino的5V
// 如果arduino沒接電腦，L298N接地然後12V接電池5V要接arduino的Vin
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(7, 8); //7 <-> Tx , 8 <-> Rx
template <typename T>
Print& operator<<(Print& printer, T value)
{
    printer.print(value);
    return printer;
}

char c=' ';
String newState = "";
long timer = 0;

struct State {
  int accel;
  int dir;
  int act;
  bool left;
  bool right;
};

State curState = { -5, 0, 0, false, false };

//pins setting
//要插在有~的pin
const byte motorIn1 = 5;
const byte motorIn2 = 3;
const byte motorIn3 = 9;
const byte motorIn4 = 6;
const byte led_left = 13;
const byte led_right = 12;

// motor 參數
byte offset_speed_L = 0;
byte offset_speed_R = 0;
const byte offset_num = 10;
const byte accel_num = 1;
const byte maxspeed = 250;
const byte minspeed = 20;
byte motorspeedR = minspeed;
byte motorspeedL = minspeed;

void parseStringToCurState(String newState) {
  int start = 0;
  int index = 0;
  for (int e=0; e<newState.length(); ++e) {
    if (newState[e] == ' ' || newState[e] == '\n') {
      switch (index) {
        case 0:
          curState.accel = newState.substring(start, e).toInt();
          break;
        case 1:
          curState.dir = newState.substring(start, e).toInt();
          break;
        case 2:
          curState.act = newState.substring(start, e).toInt();
          break;
        case 3:
          curState.left = newState.substring(start, e)=="T" ? true : false;
          break;
        case 4:
          curState.right = newState.substring(start, e)=="T" ? true : false;
          break;
        default:
          break;
      }
      start = e+1;
      index++;
    }
  }
  Serial << "State Changed: ("    << curState.accel << ", " \
         << curState.dir  << ", " << curState.act   << ", " \
         << curState.left << ", " << curState.right << ")\n";
}

void Activate() {
  analogWrite(motorIn1, 100);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, 100);
  analogWrite(motorIn4, 0); 
}

void Back_Activate() {
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 100);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, 100); 
}

void Forward() {
  if (motorspeedL + offset_speed_L >= maxspeed) {
    analogWrite(motorIn1, maxspeed);
  }
  else if (motorspeedL + offset_speed_L <= minspeed) {
    analogWrite(motorIn1, minspeed);
  }
  else {
    analogWrite(motorIn1, motorspeedL + offset_speed_L);
  }
  analogWrite(motorIn2, 0);
  
  if (motorspeedR + offset_speed_R >= maxspeed) {
    analogWrite(motorIn3, maxspeed);
  }
  else if (motorspeedR + offset_speed_R <= minspeed) {
    analogWrite(motorIn3, minspeed);
  }
  else {
    analogWrite(motorIn3, motorspeedR + offset_speed_R);
  }
  analogWrite(motorIn4, 0); 
}

void Backward() {
  analogWrite(motorIn1, 0);
  if (motorspeedL + offset_speed_L >= maxspeed) {
    analogWrite(motorIn2, maxspeed);
  }
  else if (motorspeedL + offset_speed_L <= minspeed) {
    analogWrite(motorIn2, minspeed);
  }
  else {
    analogWrite(motorIn2, motorspeedL + offset_speed_L);
  }
  
  analogWrite(motorIn3, 0);
  if (motorspeedR + offset_speed_R >= maxspeed) {
    analogWrite(motorIn4, maxspeed);
  }
  else if (motorspeedR + offset_speed_R <= minspeed) {
    analogWrite(motorIn4, minspeed);
  }
  else {
    analogWrite(motorIn4, motorspeedR + offset_speed_R);
  }
}

void Stop() {
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, 0);
}

void Drive(){
  if (curState.act == 1 || curState.act == -1){
    // control motorspeedL
    if (curState.accel >= 0){
      if (motorspeedL + curState.accel * accel_num <= maxspeed){
        motorspeedL += curState.accel * accel_num;
      }
      else{
        motorspeedL = maxspeed;
      }
    }
    else {
      if (motorspeedL + curState.accel * accel_num >= minspeed){
        motorspeedL += curState.accel * accel_num;
      }
      else{
        motorspeedL = minspeed;
      }
    }

    // control motorspeedR
    if (curState.accel >= 0){
      if (motorspeedR + curState.accel * accel_num <= maxspeed){
        motorspeedR += curState.accel * accel_num;
      }
      else{
        motorspeedR = maxspeed;
      }
    }
    else {
      if (motorspeedR + curState.accel * accel_num >= minspeed){
        motorspeedR += curState.accel * accel_num;
      }
      else{
        motorspeedR = minspeed;
      }
    }

    // control offset speed
    if (curState.dir >= 0){
      offset_speed_R = 0;
      offset_speed_L = offset_num * curState.dir;
    }
    else{
      offset_speed_L = 0;
      offset_speed_R = offset_num * curState.dir * -1;
    }

    if (curState.act == 1){
      if (motorspeedL < 35 || motorspeedR < 35) {
        Activate();
        delay(1);
      }
      Forward();
    }
    else{
      if (motorspeedL < 35 || motorspeedR < 35) {
        Back_Activate();
        delay(1);
      }
      Backward();
    }
  }
  else {
    curState.accel = -5;
    curState.dir = 0;
    curState.act = 0;
    curState.left = false;
    curState.right = false;
    motorspeedL = minspeed;
    motorspeedR = minspeed;
    Forward();
  }

  // print current speed
  Serial.print("Left speed: ");
  Serial.println(motorspeedL);
  Serial.print("Right speed: ");
  Serial.println(motorspeedR);
  Serial.print("Left offset speed: ");
  Serial.println(offset_speed_L);
  Serial.print("Right offset speed: ");
  Serial.println(offset_speed_R);

  // control LED
  if (curState.left) {
    digitalWrite(led_left,HIGH);
  }
  else{
    digitalWrite(led_left,LOW);
  }

  if (curState.right) {
    digitalWrite(led_right,HIGH);
  }
  else{
    digitalWrite(led_right,LOW);
  }
  
}

void setup() {
  pinMode(motorIn1,OUTPUT);   //left motors forward
  pinMode(motorIn2,OUTPUT);   //left motors reverse
  pinMode(motorIn3,OUTPUT);   //right motors forward
  pinMode(motorIn4,OUTPUT);   //right motors reverse
  pinMode(led_right,OUTPUT);   //Led right
  pinMode(led_left,OUTPUT);   //Led left
  Serial.begin(9600);
  Serial.println("Hello!I'm ready!");
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, 0);
  Bluetooth.begin(9600); //AT mode: should be set to 38400
}
 
void loop() {
  if(Bluetooth.available())
  {
    c=Bluetooth.read();
    newState += c;
    if (c == '\n') {
      parseStringToCurState(newState);
      newState = "";
      
    }
    // Serial.write(c);
  }
  if(millis() - timer > 10){
    Drive();
    timer = millis();
  }
  
}