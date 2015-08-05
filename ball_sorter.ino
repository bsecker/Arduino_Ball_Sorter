
/*
  
Sorting Mechanism:
  -Goes from 0 (minimum) to 160 (maximum) as a nice way of doing things. 
  (Roughly equates to 180° of movement)
  
  0 - red
  1 - green
  2 - blue / yellow
  3 - white
  4 - none
*/
#include <Servo.h>

#define sort_servo_pin 11
#define input_servo_pin 9

Servo input_servo;
Servo sort_servo;

int input_servo_pos = 0;
int input_servo_rest_pos = 175;
int input_servo_open_pos = 135;
int input_servo_open_time = 250;

int sort_servo_pos = 0;
int sort_servo_rest_pos = 0;

String colour;

int current_colour = 0;

void setup() {
  input_servo.attach(input_servo_pin); // attaches the servo on pin 9 to the servo object 
  input_servo.write(input_servo_rest_pos); // move servo to rest position
  
  sort_servo.attach(sort_servo_pin); //attaches the servo on pin 10 to the servo object 
  sort_servo.write(sort_servo_rest_pos); //move servo to rest position
  
  Serial.begin(9600);
  delay(500); //for sanity
}

void loop() {
    if(Serial.available()){
       s_sort(Serial.read()-'0');
    }
  }

void loop_array_test(){
  //loops through a set array of positions
  int results[] = {0,3,1,4,2,0,2,0,3};
  int i;
  for(i = 0; i<5; i++){
    delay(2000);
    i_pass();
    //colour = sens_read();
    Serial.println(results[i]);
    s_sort(results[i]);
    
  }
}

//Colour Sensor Functions
//------------------------------------------
int sens_read(){
   //return sensor reading
  return 2;
}

//Input Mechanism Functions 
void i_pass() {
 //open servo and allow a single ball to pass through 
 input_servo.write(input_servo_open_pos);
 delay(input_servo_open_time);
 input_servo.write(input_servo_rest_pos);
}

void i_pass_all() {
  //open servo and allow all balls to pass through (debug!) 
  input_servo.write(input_servo_open_pos);
  delay(2000); //delay two seconds to let all balls through
  input_servo.write(input_servo_rest_pos);
}

//sorting mechanism functions
//----------------------------------------------
void s_sort(int colour){
  //take input (colour) and rotate to send balls to appropriate output. Return if true.:
  if(colour==0){
    sort_servo.write(0);
  }
  else if(colour==1){
    sort_servo.write(40);
  }
  else if(colour==2){
   sort_servo.write(80);
  }
  else if(colour==3){
   sort_servo.write(120);
  }
  else {
   //unknown colour
    sort_servo.write(160); 
  }
 
  
  delay(500);
}
