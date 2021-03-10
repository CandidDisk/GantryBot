#include <Stepper.h>
#include <math.h>
//Open source library for simple, low overhead serial menu
#define SERIALMENU_MINIMAL_FOOTPRINT true
#define SERIALMENU_DISABLE_HEARTBEAT_ON_IDLE true
#include <SerialMenu.hpp>
SerialMenu& menu = SerialMenu::get();
//Open source library for handling output to serial
#include <PrintEx.h>
//Open source library for handing higher level stepper function
#include <SpeedyStepper.h>

SpeedyStepper stepperX;
SpeedyStepper stepperY;

PrintEx printEx = Serial;

void setup() {

  Serial.begin(9400);
  int outputs[] = {13, 12, 11, 10, 9, 8, 6, 5, 4, 3, 2};

  for (int i : outputs) {
    pinMode(i, OUTPUT);
  }
  pinMode(A1, OUTPUT);

  pinMode(A3, INPUT);
  pinMode(A0, INPUT);

  pinMode(A4, INPUT);
  pinMode(A5, INPUT);

  printEx.printf("\nTurning Servo X motor on...\n");
  motorEnable(13, 4);
  printEx.printf("\nTurning Servo Y motor on...\n");
  motorEnable(2, 12);

  printEx.printf("\nTurning Servo X Input B on...\n");
  motorEnable(11, A1);
  printEx.printf("\nTurning Servo Y Input B on...\n");
  motorEnable(3, 5);

  
  int analogVal;

  stepperX.connectToPins(11, A1);
  stepperX.setCurrentPositionInMillimeters(0);
  stepperX.setSpeedInMillimetersPerSecond(10000.0);
  stepperX.setStepsPerMillimeter(26.66667);
  stepperX.setAccelerationInMillimetersPerSecondPerSecond(500.0);


  stepperY.connectToPins(3, 5);
  stepperY.setCurrentPositionInMillimeters(0);
  stepperY.setSpeedInMillimetersPerSecond(2000.0);
  stepperY.setStepsPerMillimeter(2.67);
  stepperX.setAccelerationInMillimetersPerSecondPerSecond(500.0);

  printEx.printf("\nSetup complete\n");

}

bool menuDisplayed = false;
int xPointCount = 0;
int yPointCount = 0;

int xIntervDist = 0;
int yIntervDist = 0;

void motorEnable(int hi, int lo) {
  digitalWrite(hi, HIGH);
  digitalWrite(lo, LOW);
}

//int motor MUST be 1 or 2
void stepResolv(int motor, float total, int pointCount) {
  float intervDist = total / (pointCount + 1);
  int roundUp = round(intervDist + 0.5);
  int roundDown = round(intervDist - 0.5);
  int tempInput = 0;

  int pointCountUp = (total / roundUp) - 1;
  int pointCountDown = (total / roundDown) - 1;

  int intervDistFinal;
  int pointCountFinal;
  if (intervDist == roundUp || intervDist == roundDown) {
    intervDistFinal = intervDist;
    pointCountFinal = pointCount;
    printEx.printf("\nInterval distance valid: %u\nNumber of points valid: %u", intervDistFinal,pointCountFinal);
  } else {
    char receivedChar;
    printEx.printf("\nInterval distance invalid: %.2f\nNumber of points invalid: %u", intervDist, pointCount);
    printEx.printf("\nNearest number of points: 1=%u, 2=%u\n", pointCountUp, pointCountDown);
    
    
    while ( true ) {
      
      while (Serial.available() == 0){
      
      }
      
      tempInput = Serial.parseInt();
      
      if ( tempInput == 1){
        intervDistFinal = roundUp;
        pointCountFinal = pointCountUp;
        printEx.printf("\nNew interval distance set: %u\nNumber of points: %u\n", intervDistFinal, pointCountFinal);
        break;
      } else if ( tempInput == 2 ){
          intervDistFinal = roundDown;
          pointCountFinal = pointCountDown;
          printEx.printf("\nNew interval distance set: %u\nNumber of points: %u\n", intervDistFinal, pointCountFinal);
          break;
        } else if ( tempInput != 0 ) {
            printEx.printf("\n%u is not a valid input!\n", tempInput);
            printEx.printf("\nNearest number of points: 1=%u, 2=%u\n", roundUp, roundDown);
          }
      } 

  };
  if (motor == 1){
    xIntervDist = intervDistFinal;
    xPointCount = pointCountFinal;
    printEx.printf("\nServo X  interval distance: %u\nNumber of points: %u\n", xIntervDist, xPointCount);
  } else if(motor == 2) {
      yIntervDist = intervDistFinal;
      yPointCount = pointCountFinal;
      printEx.printf("\nServo Y  interval distance: %u\nNumber of points: %u\n", yIntervDist, yPointCount);
    } else {
        printEx.printf("Motor select invalid! Please restart process from menu");
      }

  menuDisplayed = false;
}

void execPoints(){

  int posX = 0;
  int posY = 0;

  int xPoint = xPointCount;
  int yPoint = yPointCount;

  bool xFinish = false;
  bool yFinish = false;
  
  stepperX.setSpeedInMillimetersPerSecond(10000);
  stepperY.setSpeedInMillimetersPerSecond(10000);

  stepperX.moveToPositionInMillimeters(0);
  stepperY.moveToPositionInMillimeters(0);

  bool foo = true;


  for (int i = 0; i < yPointCount; i++){
    Serial.println(posY);
    posY += yIntervDist;
    for (int i = 0; i < xPointCount; i++){
      Serial.println(posX);
      posX += xIntervDist;
      stepperX.moveToPositionInMillimeters(posX*100);
    }
    stepperX.moveToPositionInMillimeters(0);
    posX = 0;
    stepperY.moveToPositionInMillimeters(posY*100);
  }

  delay(1000);
  stepperY.moveToPositionInMillimeters(0);
  Serial.println("break");
  stepperX.moveToPositionInMillimeters(0);
  delay(100);
  stepperY.moveToPositionInMillimeters(0);
  delay(100);

  printEx.printf("\nTurning Servo X motor off...\n");
  motorEnable(4, 13);
  delay(100);
  
  printEx.printf("\nTurning Servo Y motor off...\n");
  motorEnable(12, 2);
  delay(100);
}

void funcCheck(){
  int delayTime = 1500;


  printEx.printf("\nTurning Servo X motor off...\n");
  motorEnable(4, 13);
  delay(delayTime);
  
  printEx.printf("\nTurning Servo X motor on...\n");
  motorEnable(13, 4);
  delay(delayTime);
  
  printEx.printf("\nTurning Servo Y motor off...\n");
  motorEnable(12, 2);
  delay(delayTime);
  
  printEx.printf("\nTurning Servo Y motor on...\n");
  motorEnable(2, 12);
  delay(delayTime);

  printEx.printf("\nServo X motor 10 CM");
  stepperX.moveToPositionInMillimeters(1000);
  delay(delayTime);

  printEx.printf("\nServo Y motor 10 CM");
  stepperY.moveToPositionInMillimeters(1000);
  delay(delayTime);

  printEx.printf("\nServo X motor 20 CM");
  stepperX.moveToPositionInMillimeters(2000);
  delay(delayTime);

  printEx.printf("\nServo Y motor 20 CM");
  stepperY.moveToPositionInMillimeters(2000);
  delay(delayTime);

  printEx.printf("\nServo X motor return to 0");
  stepperX.moveToPositionInMillimeters(0);
  delay(delayTime);

  printEx.printf("\nServo Y motor return to 0");

  stepperY.moveToPositionInMillimeters(0);
  stepperX.setSpeedInMillimetersPerSecond(0.0);
  stepperY.setSpeedInMillimetersPerSecond(0.0);
  delay(delayTime);
}


//Menu setup start
const char PROGMEM menuStep[] = "1: Configure amount of points";
const char PROGMEM menuFuncCheck[] = "2: Run function check";
const char PROGMEM menuExecPoint[] = "3: Run points";

float totalDist = 0;
int initPoints = 0;
int tempStoreMenu = 0;


const SerialMenuEntry mainMenu[] = {
    {menuStep, true, '1', [](){ 
      tempStoreMenu =  menu.getNumber<int>("Select motor : 1=x 2=y");
      totalDist = menu.getNumber<float>("Input total distance: ");
      initPoints = menu.getNumber<int>("Input expected number of points: ");
      stepResolv(tempStoreMenu, totalDist, initPoints);
      }},
    {menuFuncCheck, true, '2', [](){ 
      funcCheck();
      }},
    {menuExecPoint, true, '3', [](){
      execPoints();
      }}
  };
constexpr uint8_t mainMenuSize = GET_MENU_SIZE(mainMenu);
//Menu setup end

void loop() {
  if (!menuDisplayed){
      menuDisplayed = true;
      while(!Serial){};
      printEx.printf("\n\n\n\n\n");
      printEx.printf("GanRob Servomotor\n");
      menu.load(mainMenu, mainMenuSize);
      menu.show();
      printEx.printf("\n");
    }
  menu.run(1);
}
