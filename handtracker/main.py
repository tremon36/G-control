import collections

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 192)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 108)
cap.set(cv2.CAP_PROP_FPS, 10)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

previousTime = 0
currentTime = 0
vectors8 = [(0, 0)]


iteration = 0
prevx = 0
prevy = 0

while True:

    success, img = cap.read()
    if success:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handlandmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmarks.landmark):
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        if iteration < 10:
                            vectors8.append((x, y))
                            iteration = iteration + 1
                        else:
                            list1 = collections.deque(vectors8)
                            list1.rotate(-1)
                            vectors8 = list(list1)
                            vectors8[len(vectors8)-1] = (x,y)

                        i=1
                        while i < len(vectors8):
                            cv2.line(img, vectors8[i - 1], vectors8[i], (0, 255, 0), thickness=3)
                            i = i + 1
                        print(vectors8)
                        prevx = x
                        prevy = y

                mpDraw.draw_landmarks(img, handlandmarks)

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("image", img)
        cv2.waitKey(1)
