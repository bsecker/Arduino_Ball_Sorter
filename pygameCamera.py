#Arduino PyGame Camera and Serial Communication Module.
 
#import necessary libraries
import sys
import pygame
import pygame.camera
from pygame.locals import *
import colorsys
import time
import serial
 
class ArduinoSerial:
    def __init__(self):
     """Main serial communication module that handles Writing to serial, Averaging and handling colour reading outputs"""
        self.ser = serial.Serial('/dev/ttyUSB3',9600)
        collect_readings = False
        self.colours = []
        self.max_readings = 50 #maximum number of readings to use
 
    def add(self, colour):
        """Add colour to colour list or average list and send serial writeout with most common colour if list is too large"""
        self.colours.append(colour)
        if len(self.colours) >= self.max_readings:
            _mode = max(set(self.colours), key=self.colours.count)
            print "most common value: ", _mode
            self.writeOut(_mode)
            collect_readings = False
            self.colours = []
 
         
    def writeOut(self, colour):
        """convert colour to appropriate integer and send command to arduino"""
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
 
def calibrate():
    """startup function to calibrate the colour sensing. This isn't always enabled - only used when the ambient light in the room changes significantly."""
    print 'Performing initial calibration sequence...'
    print 'press colour id when ball is placed before gate for each colour.'
    _hues = [[31,331],[31,43],[43,57],[151,211] #default hues
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
        print hsv[0]   
 
        screen.fill(ccolor, (0,0,50,50))
        pygame.display.flip()
         
        for event in pygame.event.get(): #event getting loop
            if event.type == pygame.QUIT:
                webcam.stop()
                terminate()
            elif event.type == KEYDOWN:
                #red
                if event.key == K_1:
                    _hues[0][0] = raw_input('REDMIN:')
                    _hues[0][1] = raw_input('REDMAX:')
 
                #orange
                if event.key == K_2:
                    _hues[1][0] = raw_input('ORANGEMIN:')
                    _hues[1][1] = raw_input('ORANGEMAX:')
 
                #yellow
                if event.key == K_3:
                    _hues[2][0] = raw_input('YELLOWMIN:')
                    _hues[2][1] = raw_input('YELLOWMAX:')
 
                #cyan
                if event.key == K_4:
                    _hues[3][0] = raw_input('CYANMIN:')
                    _hues[3][1] = raw_input('CYANMAX:')
 
                #done
                if event.key == K_d:
                    print 'done calibration'
 
 
    print 'original hues: [[31,331],[31,43],[43,57],[151,211]'
    print 'calibrated hues:',_hues
    return _hues
    #return [[31,331],[31,43],[43,57],[151,211]
 
def get_colour(hsv):
    """takes HSV input and returns one of the possible colours"""
    if hsv[1]<0.2 : # check saturation. Can't use value because of AGC
        detected = 'none'
 
    else:
        # print int(hsv[0]*360), int(hsv[1]*100), int(hsv[2]*100),ccolor
        # conver HSV to color words
        if int(hsv[0]*360) < hue_list[0][0]:                # red nominally 0 deg
            detected = 'red'
        elif int(hsv[0]*360) in range(hue_list[1][0],hue_list[1][1]):   # orange nominally 36 deg
            detected = 'orange'
        elif int(hsv[0]*360) in range(hue_list[2][0],hue_list[2][1]):  # Yellow .... 50 Deg
            detected = 'yellow'
        elif int(hsv[0]*360) in range(hue_list[3][0],hue_list[3][1]): # Cyan 208 deg
            detected = 'cyan'
        elif int(hsv[0]*360) > hue_list[0][1]:       # wraps around back to zero (red)
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
    pygame.camera.init() #initalise camera
     
    
    global arduino_serial, collect_readings, hue_list
    collect_readings = False
    arduino_serial = ArduinoSerial()
 
    hue_list = calibrate() #comment this line out to disable calibration
         
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
         
        #add colour to list
        if collect_readings == True:
            print detected
            arduino_serial.add(detected)
             
        #update PyGame screen
        screen.fill(ccolor, (0,0,50,50))
        pygame.display.flip()
         
        for event in pygame.event.get(): #event handling
            if event.type == pygame.QUIT:
                webcam.stop()
                terminate()
             
if __name__=="__main__":
    main()
 
