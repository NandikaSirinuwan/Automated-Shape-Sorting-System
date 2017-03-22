//LED pins for each shape
#define LED1 2 //for triangle
#define LED2 3 //for square
#define LED3 4 //for hexagon
#define LED4 5 //for other shapes

//declare pin functions on stepper driver of conveyor
#define stp 22
#define dir 24
#define MS1 26
#define MS2 28
#define EN  30
//declare pin functions on stepper driver of rotator
#define rstp 23
#define rdir 25
#define rMS1 27
#define rMS2 29
#define rEN  31

#define LDR A0 //LDR pin
#define LDR_THRESH 30 //if higher than this value, that means object is present
#define CONV_SPD 4000 //micro seconds for step signal to stepper driver
byte incomingByte;  //serial buffer
uint8_t LEDs[] = {LED1, LED2, LED3, LED4};


void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) {
    pinMode(LEDs[i], OUTPUT);
    offAllLEDs();
  }

  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);
  resetEDPins();
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  pinMode(rstp, OUTPUT);
  pinMode(rdir, OUTPUT);
  pinMode(rMS1, OUTPUT);
  pinMode(rMS2, OUTPUT);
  pinMode(rEN, OUTPUT);

  digitalWrite(rstp, LOW);
  digitalWrite(rdir, LOW);
  digitalWrite(rMS1, LOW);
  digitalWrite(rMS2, LOW);
  digitalWrite(rEN, LOW);

}
unsigned long cutTime = 0;
bool cut = false;
bool runAfterCut = false;
byte ledn;
int currentAngle = 0;

void loop() {
  int ldr_val = analogRead(LDR);
  if (ldr_val > LDR_THRESH) {
    if (cut == false) {
      cutTime = millis();
      cut = true;

    }

    if (Serial.available() > 0) {
      incomingByte = Serial.read();
      if (!runAfterCut) {
        switch (incomingByte) {
          case '3':
            ledn = 0;
            break;
          case '4':
            ledn = 1;
            break;
          case '6':
            ledn = 2;
            break;
          case '0':
            ledn = 3;
            break;
          default:
            break;
        }
      }
      if ((millis() - cutTime > 2000) && cut) {
        onCorrectLED(ledn);
        digitalWrite(13, HIGH);
      }
      if ((millis() - cutTime > 4000) && cut) {
        digitalWrite(13, LOW);
        rotateTo(ledn);
        offAllLEDs();
        runAfterCut = true;

      }
    }
  }
  else {
    digitalWrite(EN, LOW);
    digitalWrite(dir, HIGH);
    digitalWrite(MS1, HIGH);
    digitalWrite(MS2, HIGH);
    SmallStepMode();
    cutTime = 0;
    cut = false;
    runAfterCut = false;

  }

  if (runAfterCut) {
    runCmd();
  }

}//end main loop

//run the conveyor after detecting a shape
void runCmd() {
  offAllLEDs();
  digitalWrite(EN, LOW);
  digitalWrite(dir, HIGH); //Pull direction pin low to move "forward"
  digitalWrite(MS1, HIGH); //Pull MS1, and MS2 high to set logic to 1/8th microstep resolution
  digitalWrite(MS2, HIGH);
  SmallStepMode();
  cutTime = 0;
}

//light up the correct led given by parameter n
void onCorrectLED(byte n) {
  if (!runAfterCut) {
    digitalWrite(LEDs[n], HIGH);

    for (int i = 0; i < 4; i++) {
      if (i != n) {
        digitalWrite(LEDs[i], LOW);
      }
    }
  }
}

//turn off all LED
void offAllLEDs() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(LEDs[i], LOW);
  }
}

//reset all control pins of the stepper driver
void resetEDPins()
{
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(EN, HIGH);
}

// 1/8th microsteping step genaration function for conveyor
void SmallStepMode()
{

  digitalWrite(stp, HIGH); //Trigger one step forward
  delayMicroseconds(4000);
  digitalWrite(stp, LOW); //Pull step pin low so it can be triggered again
  delayMicroseconds(4000);
}

//rotate the rotationg plate according to given angle and direection
void rotate(bool dire, int ang) {
  if (dire) {
    digitalWrite(rdir, HIGH);
  }
  else {
    digitalWrite(rdir, LOW);
  }
  byte steps;
  if (ang == 90) {
    steps = 12;
  } else if (ang == 180)  {
    steps = 24;
  }

  for (int i = 0; i < steps; i++) {
    digitalWrite(rstp, HIGH); //Trigger one step forward
    delay(20);
    digitalWrite(rstp, LOW); //Pull step pin low so it can be triggered again
    delay(20);
  }
}
//select most suitable rotation according to given angle and present angle
void rotateTo(uint8_t shapeNum) {
  switch (shapeNum) {
    case 0:  //tra ROTATE TO 0
      switch (currentAngle) {
        case 0:
          //
          break;
        case  90:
          rotate(true, 90);
          break;
        case  180:
          rotate(true, 180);
          break;
        case  270:
          rotate(false, 90);
          break;
        default:
          break;
      }
      currentAngle = 0;
      break;
    case 1:  //squ ROTETE TO 90
      switch (currentAngle) {
        case  0:
          rotate(false, 90);
          break;
        case  90:
          //
          break;
        case  180:
          rotate(true, 90);
          break;
        case  270:
          rotate(true, 180);
          break;
        default:
          break;
      }
      currentAngle = 90;
      break;
    case 2:  //hex ROTATE TO 180
      switch (currentAngle) {
        case  0:
          rotate(true, 180);
          break;
        case  90:
          rotate(false, 90);
          break;
        case  180:
          //
          break;
        case  270:
          rotate(true, 90);
          break;
        default:
          break;
      }
      currentAngle = 180;
      break;
    case 3:  //irre ROTATE TO 270
      switch (currentAngle) {
        case  0:
          rotate(true, 90);
          break;
        case  90:
          rotate(true, 180);
          break;
        case  180:
          rotate(false, 90);
          break;
        case  270:
          //
          break;
        default:
          break;
      }
      currentAngle = 270;
      break;
    default:
      break;
  }
}



