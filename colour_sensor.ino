unsigned int red_raw_value;
unsigned int green_raw_value;
unsigned int blue_raw_value;


int red_strength;
int green_strength;
int blue_strength;


int pin_s2 = 7;
int pin_s3 = 8;

int out_pin = 4;

unsigned int pulse_width;

void setup() {
  digitalWrite(pin_s2,LOW);
  digitalWrite(pin_s3,LOW);
  Serial.begin(115200);
}

void loop() {
  
  //get red value
  
 
 //get red value
  digitalWrite(pin_s2,LOW);
  digitalWrite(pin_s3,LOW);
  pulse_width = pulseIn(out_pin, LOW);    //Measure length of a LOW pulse at pin outPin
  
  red_strength = (pulse_width/400)-1;
  red_strength = (255-red_strength);
 
 //get green value
  digitalWrite(pin_s2,HIGH);
  digitalWrite(pin_s3,HIGH);
  pulse_width = pulseIn(out_pin, LOW);    //Measure length of a LOW pulse at pin outPin
  green_strength = (pulse_width/400)-1;
  green_strength = (255-green_strength);
 
 
  Serial.print(red_strength);
  Serial.print("  ");
  Serial.println(green_strength);
}
