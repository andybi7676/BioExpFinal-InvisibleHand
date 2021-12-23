#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(2, 3); //2 <-> Tx , 3 <-> Rx
template <typename T>
Print& operator<<(Print& printer, T value)
{
    printer.print(value);
    return printer;
}

char c=' ';
String newState = "";

struct State {
  int accel;
  int dir;
  bool act;
  bool left;
  bool right;
};

State curState = { -5, 0, false, false, false };

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
          curState.act = newState.substring(start, e)=="T" ? true : false;
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

void setup() 
{
  Serial.begin(9600);
  Serial.println("ready");
  Bluetooth.begin(9600); //AT mode: should be set to 38400
}

void loop() 
{
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
  if(Serial.available())
  {
    c=Serial.read();
    Bluetooth.write(c);
  }
}
