// 如果arduino插電腦，L298N接地然後12V要接arduino的5V
// 如果arduino沒接電腦，L298N接地然後12V接電池5V要接arduino的Vin
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(7, 8);
char prev_cmd=' ';
char cmd=' ';

//pins setting
//要插在有~的pin
const byte motorIn1 = 9;
const byte motorIn2 = 6;
const byte motorIn3 = 5;
const byte motorIn4 = 3;
const byte servo = 11; //10 11

// motor 參數
byte motorspeedR = 150;
byte motorspeedL = 150;
const byte offset_num = 50;

void Activate() {
  analogWrite(motorIn1, 150);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, 150);
  analogWrite(motorIn4, 0); 
}

void Back_Activate() {
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 150);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, 150); 
}

void Forward() {
  analogWrite(motorIn1, motorspeedL);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, motorspeedR);
  analogWrite(motorIn4, 0); 
}

void Backward() {
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, motorspeedL);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, motorspeedR);
}

void Left() {
  analogWrite(motorIn1, motorspeedL);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, motorspeedR+offset_num);
  analogWrite(motorIn4, 0);
}

void Right() {
  analogWrite(motorIn1, motorspeedL+offset_num);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, motorspeedR);
  analogWrite(motorIn4, 0);
}

void Stop() {
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, 0);
}

void Accelerate() {
  motorspeedL += 10;
  motorspeedR += 10;
  Serial.print("Left speed: ");
  Serial.println(motorspeedL);
  Serial.print("Right speed: ");
  Serial.println(motorspeedR);
  Forward();
}

void Decelerate() {
  motorspeedL -= 10;
  motorspeedR -= 10;
  Serial.print("Left speed: ");
  Serial.println(motorspeedL);
  Serial.print("Right speed: ");
  Serial.println(motorspeedR);
  Forward();
}

void setup() {
  pinMode(motorIn1,OUTPUT);   //left motors forward
  pinMode(motorIn2,OUTPUT);   //left motors reverse
  pinMode(motorIn3,OUTPUT);   //right motors forward
  pinMode(motorIn4,OUTPUT);   //right motors reverse
  //pinMode(9,OUTPUT);   //Led
  Serial.begin(9600);
  Serial.println("Hello!I'm ready!");
  Bluetooth.begin(9600);
  analogWrite(motorIn1, 0);
  analogWrite(motorIn2, 0);
  analogWrite(motorIn3, 0);
  analogWrite(motorIn4, 0);
}
 
void loop() {
  if(Bluetooth.available()){
    cmd = Bluetooth.read();
    Serial.println(cmd);
  }
  if (cmd != prev_cmd) {
    Control(cmd);
    prev_cmd = cmd;
  }
}

void Control(char c) {
  if(c == 'F'){            //move forward(all motors rotate in forward direction)
    Activate();
    delay(5);
    Forward();
    Serial.println("You are at Forward!");
  }
  else if(c == 'B'){      //move reverse (all motors rotate in reverse direction)
    Back_Activate();
    delay(5);
    Backward();
    Serial.println("You are at Backward!");
  }
  else if(c == 'L'){      //turn right (left side motors rotate in forward direction, right side motors doesn't rotate)
    Activate();
    delay(5);
    Left();
    Serial.println("You are at Left!");
  }
  else if(c == 'R'){      //turn left (right side motors rotate in forward direction, left side motors doesn't rotate)
    Activate();
    delay(5);
    Right();
    Serial.println("You are at Right!");
  }
  else if(c == 'A'){      //move reverse (all motors rotate in reverse direction)
    Accelerate();
  }
  else if(c == 'D'){      //move reverse (all motors rotate in reverse direction)
    Decelerate();
  }
  else if(c == 'S'){      //STOP (all motors stop)
    Stop();
    Serial.println("You are at Stop!");
  }
}
