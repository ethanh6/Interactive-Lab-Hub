import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
import alsaaudio
import random
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

class Quote_generator:
    
    def __init__(self, state):
        '''
        state = 0: nothing
        state = 1: thumbup
        state = 2: high5
        state = 3: i love you
        state = 4: quite coyote
        '''
        self.QUOTES = ["Continuous improvement is \n better than delayed perfection.",
            "Hope, but never expect.\n Look forward, but never wait.",
            "Work hard and don't allow anyone to \n make you feel bad for your success.",
            "Prove them wrong!\n",
            "Do all things with kindness!\n",
            "If you can't stop thinking about it,\n don't stop working for it.",
            "Never try to fit in.\n You were born to stand out!"]
        self.state = state 
        self.quote = self.QUOTES[random.randint(0, len(self.QUOTES)-1)]

    def get_state(self):
        return self.state

    def get_quote(self):
        return self.quote

    def update_gesture(self, thumbup, high5, iloveu, coyote):
        if thumbup and self.state != 1:
            self.state = 1
            self.quote = self.QUOTES[random.randint(0, len(self.QUOTES)-1)]

        elif high5 and self.state != 2:
            self.state = 2
            self.quote = self.QUOTES[random.randint(0, len(self.QUOTES)-1)]

        elif iloveu and self.state != 3:
            self.state = 3
            self.quote = self.QUOTES[random.randint(0, len(self.QUOTES)-1)]

        elif coyote and self.state != 4:
            self.state = 4
            self.quote = self.QUOTES[random.randint(0, len(self.QUOTES)-1)]

quote_generator = Quote_generator(state=0)

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
        thumb_up_condition = is_thumb_up(thumbX, thumbY, pointerX, pointerY, middleX, middleY,
                                        ringX, ringY, pinkyX, pinkyY)
        # i love you condition
        i_love_you_condition = is_I_love_you(thumbX, thumbY, pointerX, pointerY, middleX, middleY,
                                        ringX, ringY, pinkyX, pinkyY)
        # high five condition
        high_five_condition = is_high_five(thumbX, thumbY, pointerX, pointerY, middleX, middleY,
                                        ringX, ringY, pinkyX, pinkyY)
        
        # state machine
        quote_generator.update_gesture(thumb_up_condition, high_five_condition, i_love_you_condition, coyote_condition)
        quote = quote_generator.get_quote()
        state = quote_generator.get_state()

        dy = 20
        x, y = 150, 150
        q0, q1 = quote.split("\n")
        FONT_SIZE = 1.5

        if state == 0:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            counter = 0
            print("Hello")
            cv2.putText(img, 'Hello!', (100, 100), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
        
        if coyote_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            counter = 0
            # print("quite coyotea")
            cv2.putText(img, 'quiet coyote!', (100, 100), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)

        elif thumb_up_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            counter = 0
            # print("thumb up")
            cv2.putText(img, 'Thumb up!', (x, y), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
            cv2.putText(img, q0, (x, y+dy), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
            cv2.putText(img, q1, (x, y+2*dy), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)

        elif i_love_you_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            counter = 0
            # print("I love you")
            cv2.putText(img, 'I love you too!', (x, y), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
            cv2.putText(img, q0, (x-10, y+dy), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
            cv2.putText(img, q1, (x-10, y+2*dy), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)

        elif high_five_condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            counter = 0
            # print("High Five!")
            cv2.putText(img, 'High five!', (x, y), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
            cv2.putText(img, q0, (x, y+dy), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)
            cv2.putText(img, q1, (x, y+2*dy), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 0), 3)

        else:
            vol = np.interp(length0, [50, 300], [minVol, maxVol])
            volBar = np.interp(length0, [50, 300], [400, 150])
            volPer = np.interp(length0, [50, 300], [0, 100])
            m.setvolume(int(vol))

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
