
import cv2
import os
import time

face_cascade = cv2.CascadeClassifier('cars.xml')
vc = cv2.VideoCapture('dashcam.mp4')
#vc = cv2.VideoCapture(0)
 
if vc.isOpened():
    rval , frame = vc.read()
else:
    rval = False
 
 
roi = [0,0,0,0]
lastdetected = 0
detections = 0
last_alert = 0   
total_alerts = 0
actual_alerts = 0   

while rval:
    rval, frame = vc.read()
    fheight, fwidth, fdepth = frame.shape 
 
    # car detection.
    cars = face_cascade.detectMultiScale(frame, 1.1, 2)
 
    ncars = 0
    for (x,y,w,h) in cars:
 
        if x < fwidth*0.6  and y < fheight*0.5 and w < 300 and h < 300:
 
                if ( abs(x-roi[0]) < 20 ):
                    x = roi[0]
 
                if ( abs(y-roi[1]) < 20 ):
                    y = roi[1]
 
                if ( abs(w-roi[2]) < 20 ):
                    w = roi[2]
 
                if ( abs(h-roi[3]) < 50 ):
                    h = roi[3]
 
                roi = [x,y,w,h]
                ncars = ncars + 1
                lastdetected = 0
                detections = detections + 1
                print "Bit :: Object detected"
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)


        if w*h > ( fwidth*fheight*0.1):
            total_alerts = total_alerts+1
            current_time = time.time()

            if current_time - last_alert > 3:
                last_alert = current_time
                actual_alerts = actual_alerts +1
                print "Bit :: alert dispatched"
                os.system('say "Break"');

 
    # show result
    cv2.imshow("Result",frame)
    cv2.waitKey(1);
vc.release()