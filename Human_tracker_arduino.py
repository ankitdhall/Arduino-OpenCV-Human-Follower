# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Created during Winter Semester 2015

OpenCV Human face tracker combined with arduino powered bot to
follow humans.

         @authors:
Yash Chandak    Ankit Dhall


TODO:
convert frame specific values to percentages
-------------------------------------------------------------------------------
"""

import numpy as np
import sys
import time

"""
PySerial library required for arduino connection
OpenCV library requierd for face tracking
"""

import serial
import cv2

"""
Arduino connected at port No. COM28,
Confirm and change this value accordingly from control panel

Baud Rate = 9600
"""

arduino = serial.Serial('COM28', 9600)
time.sleep(2) # waiting the initialization...
print("initialised")

#gets the direction for Arduino serial
def direction(bound, initArea=40000):
    """
    Direction control Index:

    '<' , '>' are the frame check bits for serial communication

    Numbers represent the direction to be moved as per their position on numpad
    1: Back Left
    2: Back
    3: Back right
    4: Left
    5: Stay still
    6: Right
    7: Front Left
    8: Forward
    9: Forward right
    """

    #anchor the centre position of the image
    center=(320, 240)
    #current rectangle center
    curr = (bound[0] + bound[2]/2, bound[1]+bound[3]/2)
    out=0
    flag=0
    fb = 0 #0-stay 1-fwd 2-bwd
    lr = 0 #0-stay 1-left 2-right

    #if the object is coming closer i.e. it's size is increasing then move bwd
    if bound[2]*bound[3] > (initArea+5000) or bound[1]<50 :
        fb = 2
    #if the object os moving away i.e. it's size is decreasing then move towards it
    elif bound[2]*bound[3] < (initArea-5000) or (bound[1]+bound[3])>430 : 
        fb = 1
    else :
        fb = 0
        
    #move right
    if curr[0] > (center[0] + 100):
        lr = 2
    #move left
    elif curr[0] < (center[0] - 100):
        lr = 1        
    else:
        lr = 0
    
    if lr == 0 and fb == 0:
        out = 5
        print "stay"
    elif lr == 0 and fb == 1:
        out =8
        print "fwd"
    elif lr == 0 and fb == 2:
        out = 2
        print "back"
    elif lr == 1 and fb == 0:
        out = 4
        print "left"
    elif lr == 1 and fb == 1:
        out = 7
        print "fwd left"
    elif lr == 1 and fb == 2:
        out = 1
        print "left back"
    elif lr == 2 and fb == 0:
        out = 6
        print "right"
    elif lr == 2 and fb == 1:
        out = 9
        print "fwd right"
    elif lr == 2 and fb == 2:
        out = 3
        print "bwd right"
    else :
        out = 5
        print "Stay Still"

    #Write the encoded direction value on the serial communication line
    print out
    arduino.write('<')
    arduino.write(str(out))
    arduino.write('>')
        
def detectAndDisplay(frame):
    #use OpenCV HAAR face detetcion algorithm to detect faces
    faces = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=3,
                                            minSize=(30, 30),maxSize=(500,500),
                                            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
     
    #if any face is detected then process else continue searching
    if(len(faces)!=0):
        #If number of faces in the image is more than 1
        #Then choose the one with maximum size
        max_area=-1
        i=0
        for (x,y,w,h) in faces:
            if w*h > max_area:
                max_area=w*h
                pos=i
            i=i+1
            
        RECT=faces[pos]
        #Mark the face being tracked on the image display
        cv2.rectangle(frame, (RECT[0], RECT[1]), (RECT[0]+RECT[2], RECT[1]+RECT[3]), (0, 255, 0), 2)
        #draw_str(frame, (RECT[0], RECT[3]+16), 'x: %.2f y: %.2f size: %.2f' % (RECT[2]-RECT[0])/2 % (RECT[3]-RECT[1])/2 % RECT[2]*RECT[3])

        #Put the text details about the ROI on imdisplay
        cv2.putText(frame, `RECT[0] + RECT[2]/2`+'  '+`RECT[1]+RECT[3]/2`+' '+`RECT[2]*RECT[3]`, (RECT[0],RECT[1]+RECT[3]),  cv2.FONT_HERSHEY_SIMPLEX , 1, (0,0,255));

        #compute direction for the arduino bot to be moved.
        direction(RECT)

    else:
        print 'Search...'
        arduino.write('<')
        arduino.write(str(5))
        arduino.write('>')
    
    cv2.imshow('frame',frame)


cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


cap = cv2.VideoCapture(1)
cap.grab()
ret, frame = cap.retrieve()
cv2.namedWindow('frame')

#Run the tracker in infinite loop
while(1):
    #grab the frames from web camera
    ret, frame = cap.retrieve()
    if ret ==0:
        print "frame not loaded"
    if ret==True:
        
        #Resize the frame for faster computation
        #cv2.resize(frame,(240,320))

        #Process the frame and pass data to arduino
        detectAndDisplay(frame)

        #cv2.imshow('input',frame)

        #press ESC to exit program
        ch = cv2.waitKey(1)
        if ch==27:
            break
    
#Free up memory on exit    
cap.release()
cv2.destroyAllWindows()
arduino.close()
