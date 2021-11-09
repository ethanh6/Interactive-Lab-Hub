import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
import alsaaudio
m = alsaaudio.Mixer()
################################
wCam, hCam = 640, 480
################################
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
 
detector = htm.handDetector(detectionCon=0.7)
minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0


def is_thumb_up(thumbX, thumbY, pointerX, pointerY, middleX, middleY, ringX, ringY, pinkyX, pinkyY):
    a0 = math.hypot(thumbX-pointerX, thumbY-pointerY)
    a1 = math.hypot(pointerX-middleX, pointerY-middleY)
    a2 = math.hypot(middleX-ringX, middleY-ringY)
    a3 = math.hypot(ringX-pinkyX, ringY-pinkyY)
    return a0>100 and a1<50 and a2<50 and a3<50
            
def is_I_love_you(thumbX, thumbY, pointerX, pointerY, middleX, middleY, ringX, ringY, pinkyX, pinkyY):
    a0 = math.hypot(thumbX-pointerX, thumbY-pointerY)
    a1 = math.hypot(pointerX-middleX, pointerY-middleY)
    a2 = math.hypot(middleX-ringX, middleY-ringY)
    a3 = math.hypot(ringX-pinkyX, ringY-pinkyY)
    return a0>100 and a1>100 and a2<30 and a3>70

def is_high_five(thumbX, thumbY, pointerX, pointerY, middleX, middleY, ringX, ringY, pinkyX, pinkyY):
    a0 = math.hypot(thumbX-pointerX, thumbY-pointerY)
    a1 = math.hypot(pointerX-middleX, pointerY-middleY)
    a2 = math.hypot(middleX-ringX, middleY-ringY)
    a3 = math.hypot(ringX-pinkyX, ringY-pinkyY)
    return a0>70 and a1>70 and a2>70 and a3>70

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
 
        thumbX, thumbY = lmList[4][1], lmList[4][2] #thumb
        pointerX, pointerY = lmList[8][1], lmList[8][2] #pointer

        middleX, middleY = lmList[12][1], lmList[12][2]
        ringX, ringY = lmList[16][1], lmList[16][2]
        pinkyX, pinkyY = lmList[20][1], lmList[20][2]
        
        cx, cy = (thumbX + pointerX) // 2, (thumbY + pointerY) // 2
 
        cv2.circle(img, (thumbX, thumbY), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (pointerX, pointerY), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (middleX, middleY), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (ringX, ringY), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (pinkyX, pinkyY), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (thumbX, thumbY), (pointerX, pointerY), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # coyote condition
        len_calc = lambda x1,y1,x2,y2: math.hypot(x2 - x1, y2 - y1)
        length0 = len_calc(thumbX,thumbY,pointerX,pointerY)
        length1 = len_calc(pointerX,pointerY,middleX,middleY)
        length2 = len_calc(middleX, middleY, ringX, ringY)
        length3 = len_calc(ringX, ringY, pinkyX, pinkyY)
        length4 = len_calc(thumbX,thumbY, ringX, ringY)

        coyote_condition = length0>100 and length1>100 and length2<100 and length3>100 and length4<100

        # thumb up condition
        thumb_up_condition = is_thumb_up(thumbX, thumbY,
                                        pointerX, pointerY,
                                        middleX, middleY,
                                        ringX, ringY,
                                        pinkyX, pinkyY)
        # i love you condition
        i_love_you_condition = is_I_love_you(thumbX, thumbY,
                                        pointerX, pointerY,
                                        middleX, middleY,
                                        ringX, ringY,
                                        pinkyX, pinkyY)
        # high five condition
        high_five_condition = is_high_five(thumbX, thumbY,
                                        pointerX, pointerY,
                                        middleX, middleY,
                                        ringX, ringY,
                                        pinkyX, pinkyY)

        if coyote_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            print("quite coyotea")
            cv2.putText(img, 'quiet coyote!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        elif thumb_up_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            print("thumb up")
            cv2.putText(img, 'thumb up', (102, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        elif i_love_you_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            print("I love you")
            cv2.putText(img, 'I love you too!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        elif high_five_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            print("High Five!")
            cv2.putText(img, 'High five!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        else:
            vol = np.interp(length0, [50, 300], [minVol, maxVol])
            volBar = np.interp(length0, [50, 300], [400, 150])
            volPer = np.interp(length0, [50, 300], [0, 100])
            m.setvolume(int(vol))

        # print(int(length), vol)

 
        if length0 < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
 
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
 
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
 
    cv2.imshow("Img", img)
    cv2.waitKey(1)
