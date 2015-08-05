#Arduino PyGame Camera and Serial Communication Module.

import sys
import pygame
import pygame.camera
from pygame.locals import *
import colorsys
import time
import serial

class ArduinoSerial:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB3',9600)
        
    def writeOut(self, colour):
        _col = ""
        if colour == "none":
            _col = "0"
        elif colour == "red":
            _col = "1"
        elif colour == "orange":
            _col = "2"
        elif colour == "yellow":
            _col = "3"
        elif colour == "cyan":
            _col = "4"
        self.ser.write(_col)

def get_colour(hsv):
    """takes HSV input and returns one of the possible colours"""
    if hsv[1]<0.2 : # check saturation. Can't use value because of AGC
        detected = 'none'

        #00 - none, 01 - red, 10 - green 11 - blue 
    else:
        # print int(hsv[0]*360), int(hsv[1]*100), int(hsv[2]*100),ccolor
        # conver HSV to color words
        if int(hsv[0]*360) < 31:                # red nominally 0 deg
            detected = 'red'
        elif int(hsv[0]*360) in range(31,43):   # orange nomnally 36 deg
            detected = 'orange'
        elif int(hsv[0]*360) in range(43,57):  # Yellow .... 50 Deg
            detected = 'yellow'
        elif int(hsv[0]*360) in range(151,211): # Cyan 208 deg
            detected = 'cyan'
        elif int(hsv[0]*360) > 331:       # wraps around back to zero (red)
            detected = 'red'
        else:
            detected = 'none'
    return detected

def terminate():
    """flush serial buffer and close everything down nicely"""
    arduino_serial.ser.close()
    pygame.quit()
    sys.exit()
    

def main():
    pygame.camera.init()
    
    global arduino_serial
    arduino_serial = ArduinoSerial()
    
    screen = pygame.display.set_mode((320,240),0)
    cam_list = pygame.camera.list_cameras()
    
    if not cam_list:
        print 'Error: No camera found. quitting'
        terminate()
        
    webcam = pygame.camera.Camera(cam_list[0],(352,288))
    
    try:
        webcam.start()
    except SystemError:
        pygame.quit()
        sys.exit()

    detected = 'none'
    last_detected = ''

    while True:
        # reduce noise, average 5 frames
        av = []
        for i in range(0,1):
            av.append(webcam.get_image())
            
        avg = pygame.transform.average_surfaces(av)
        screen.blit(avg, (0,0))     # display average
        # find the average colour inside the target rectangle
        crect = pygame.draw.rect(screen, (255,255,255), (145, 105, 50,50), 3)
        ccolor = pygame.transform.average_color(avg,crect)
        hsv = colorsys.rgb_to_hsv(ccolor[0]/255.0, ccolor[1]/255.0, ccolor[2]/255.0 )
        
        detected = get_colour(hsv)
        
              
        if detected != last_detected:
            print detected
            arduino_serial.writeOut(detected)
            last_detected = detected
            

        screen.fill(ccolor, (0,0,50,50))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                webcam.stop()
                terminate()
            

if __name__=="__main__":
    main()



                              


                              
