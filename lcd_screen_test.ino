#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library

// The control pins for the LCD can be assigned to any digital or
// analog pins...but we'll use the analog pins as this allows us to
// double up the pins with the touch screen (see the TFT paint example).
#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0

#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin

// Assign human-readable names to some common 16-bit color values:
#define	BLACK   0x0000
#define	RED     0xF800
#define	GREEN   0x07E0
#define CYAN    0x07FF
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
#define ORANGE  0xFD20

//Initalize TFTLCD screen
Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

//define count of each colour (old)
int red_count = 0;
int orange_count = 0;
int yellow_count = 0;
int blue_count = 0;
int unknown_count = 0;

//init colours and counts of each colour.
String colour_strings[] = {"RED","ORANGE","YELLOW","BLUE","UNKNOWN"};
int colours[] = {RED, ORANGE, YELLOW, CYAN, GREEN};
int colour_counts[] = {0,0,0,0,0};

//define LCD drawing variables
int tft_num_width = 200;
int tft_bezel_width = 10;

void setup(){
 //initialize Serial and LCD screen
 Serial.begin(9600);
 tft.reset();
 uint16_t identifier = tft.readID();
 tft.begin(identifier);
 tft.reset();
 tft.fillScreen(BLACK);
 
 tft.setTextColor(WHITE,BLACK);    
 tft.setTextSize(4);
 show_colours(); 
 
  
}

void loop(){
 //Wait for serial input before doing anything
 if(Serial.available()){
   count_colour(Serial.read()-'0');
   show_colours(); 
 }
  
 
}

void count_colour(int colour){
 //add 1 to appropriate colour
 //if any number is used, the colour is unrecognised (4)
  if(colour<=3){
    colour_counts[colour]++; 
  }
  else{
    colour_counts[4]++; 
  }
}

void show_colours(){
 //iterate through colours and print each to the screen a little lower than the last.
  for(int i = 0; i <= 5; i++){
    tft.setCursor(tft_bezel_width, i*40+10);
    tft.setTextColor(colours[i], BLACK);
    tft.print(colour_strings[i]);
    tft.setCursor(tft_num_width, i*40+10);
    tft.print(String(colour_counts[i]));
  } 
}

