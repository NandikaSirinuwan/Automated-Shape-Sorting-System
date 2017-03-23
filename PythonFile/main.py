#import packages
import numpy as np
import cv2
import serial as ser

import Settings

#make serial instance
prt = ser.Serial(
port='COM8',
baudrate=9600,
parity=ser.PARITY_NONE,
stopbits=ser.STOPBITS_ONE,
bytesize=ser.EIGHTBITS
)
##make setting instance
sett=Settings.Settings()

#track bars onChange event
def onThr1(x):
    sett.settingArray[0]=x
def onThr2(x):
    sett.settingArray[1]=x
def onBlur(x):
    sett.settingArray[2]=x
def onE(x):
    sett.settingArray[3]=x
def onY1(x):
    sett.settingArray[4]=x
def onY2(x):
    sett.settingArray[5]=x
def onX1(x):
    sett.settingArray[6]=x
def onX2(x):
    sett.settingArray[7]=x
def nothing(x):
    pass

#count given conners and make relevent serial out,draw letter and contours on output Mat
#if you want more polygon,you can uncomment and add more elif statements
def getPoly(conners):
        points= len(conners)
        print ('ByPython: '+str(points))
        if points==3:
            prt.write(str(3))
            cv2.putText(img,'Triangle',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
            cv2.drawContours(img,[conners],-1,(0,255,0),2)
            #cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif points==4:
            prt.write(str(4))
            cv2.putText(img,'Square',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
            cv2.drawContours(img,[conners],-1,(0,255,0),2)
            #cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        #elif points==5:
        #    prt.write(str(5))
        #    cv2.putText(img,'Pentagon',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
        #    cv2.drawContours(img,[conners],-1,(0,255,0),2 )
        elif points == 6:
            prt.write(str(6))
            cv2.putText(img,'Hexagon',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
            cv2.drawContours(img,[conners],-1,(0,255,0),2)
            #cv2.drawContours(img,[cnt],0,(255,255,0),-1)
        ##elif points==7:
        ##    #prt.write(str(7) + '\r\n')
        ##    cv2.putText(img,'Heptagon',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
        ##    cv2.drawContours(img,[conners],-1,(0,255,0),2)
        #elif points==8:
        #    #prt.write(str(8) + '\r\n')
        #    cv2.putText(img,'Octagon',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
        #    cv2.drawContours(img,[conners],-1,(0,255,0),2)
        elif points > 5:
            prt.write(str(0))
            cv2.putText(img,'Irregular Shape',(10,110), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
            cv2.drawContours(img,[conners],-1,(0,255,0),2)
            #cv2.drawContours(img,[cnt],0,(0,255,255),-1)


#load settings on the settings.txt file
def loadSettings():
    sett.readSettings()
    

def makeTrackBars():
    #make trackbar window
    cv2.namedWindow('TrackBars_Filtering')
    #trackbars for filtering
    cv2.createTrackbar('Threshold','TrackBars_Filtering',int(sett.settingArray[0]),255,onThr1)
    cv2.createTrackbar('ThresholdUp','TrackBars_Filtering',int(sett.settingArray[1]),255,onThr2)
    cv2.createTrackbar('BlurSize','TrackBars_Filtering',int(sett.settingArray[2]),50,onBlur)
    cv2.createTrackbar('Epsilon','TrackBars_Filtering',int(sett.settingArray[3]),10,onE)
    #trackbars for set image position
    cv2.namedWindow('TrackBars_Sizing')
    cv2.createTrackbar('Y1','TrackBars_Sizing',int(sett.settingArray[4]),480,onY1)
    cv2.createTrackbar('Y2','TrackBars_Sizing',int(sett.settingArray[5]),480,onY2)
    cv2.createTrackbar('X1','TrackBars_Sizing',int(sett.settingArray[6]),640,onX1)
    cv2.createTrackbar('X2','TrackBars_Sizing',int(sett.settingArray[7]),640,onX2)
    #find contours
    cv2.namedWindow('FindCnt')
    cv2.createTrackbar('ContourApproximationModes','FindCnt',0,4,nothing)
  #cv::CHAIN_APPROX_NONE = 1, 
  #cv::CHAIN_APPROX_SIMPLE = 2, 
  #cv::CHAIN_APPROX_TC89_L1 = 3, 
  #cv::CHAIN_APPROX_TC89_KCOS = 4 
    cv2.createTrackbar('RetrievalModes','FindCnt',0,4,nothing)
  #cv::RETR_EXTERNAL = 0, 
  #cv::RETR_LIST = 1, 
  #cv::RETR_CCOMP = 2, 
  #cv::RETR_TREE = 3, 
  #cv::RETR_FLOODFILL = 4 

  #====================================================
  #load settings and make trackbar windows
loadSettings()    
makeTrackBars()

#open the cam
cap=cv2.VideoCapture(1)
if not cap.isOpened()  :
    print("can't open the camera")

while(1):
    #try to read cam
    try:
        ret,frame=cap.read()
    except:
        print("unable to get image from amera")
    #resize captured frame to given size from TrackBars_Sizing track bars
    try:
        frame=frame[y1:y2,x1:x2]
    #flip as you want
        cv2.flip(frame,1)
    except:
        print "error while resizing (or flipping)"
    #make copy of Mat
    img = frame
    #read track bars for blur.If value is 0,it shuld be 1.because of while giving 0 as blur,it function occur an error.
    b=cv2.getTrackbarPos('BlurSize','TrackBars_Filtering')
    if b==0:
        b=1
    #read trackbars for frame resizing
    y1=cv2.getTrackbarPos('Y1','TrackBars_Sizing')
    y2=cv2.getTrackbarPos('Y2','TrackBars_Sizing')
    x1=cv2.getTrackbarPos('X1','TrackBars_Sizing')
    x2=cv2.getTrackbarPos('X2','TrackBars_Sizing')
    #make blur according to given track bar value
    frame = cv2.blur(frame,(b,b))
    #convert RGB to GRAY.this is essential for future process
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #read threshold values track bar
    th=cv2.getTrackbarPos('Threshold','TrackBars_Filtering')
    lmt=cv2.getTrackbarPos('ThresholdUp','TrackBars_Filtering')
    #make a binary threshold for givel range by track bars value
    ret,thresh = cv2.threshold(gray,th,lmt,cv2.THRESH_BINARY)
    #read contour approximation methode from track bar
    mode=cv2.getTrackbarPos('ContourApproximationModes','FindCnt')
    tpe=cv2.getTrackbarPos('RetrievalModes','FindCnt')+1
    #display thresholded Mat
    cv2.imshow("THR",thresh)
    #find countours from thresholded Mat
    _,contours,h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #read epsilon value for approxPolyDP function.read documantation for more info
    eps=cv2.getTrackbarPos('Epsilon','TrackBars_Filtering')
    #try to get a polygon from every contour previously detected
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,eps*0.01*cv2.arcLength(cnt,True),True)
        #get number of conners
        corners=len(approx)
        #if conners count is more than 2 and less than 9,call getPoly
        if(corners>2 and corners<9):
            getPoly(approx)
    #show RGB modified frame         
    cv2.imshow('img',img)
    #wait 40ms for 'q' key.if pressed,write current settings,destroy windows and exit from loop
    if cv2.waitKey(40) & 0xFF ==ord('q'):
        sett.writeSettings()
        cv2.destroyAllWindows()
        break
    