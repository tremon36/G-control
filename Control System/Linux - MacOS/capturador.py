import cv2
import mediapipe as mp
import numpy as np

def capturarManos(q):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 192)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 108)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    prevx = 0
    prevy = 0

    list_position = -1
    list = np.empty((22, 1))

    while True:
        success, img = cap.read()
        if success:

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:  # si hay una mano en la pantalla
                x0 = 0
                y0 = 0
                for handlandmarks in results.multi_hand_landmarks:  # para cada mano

                    for id, lm in enumerate(handlandmarks.landmark):  # para cada punto de esa mano
                        if id == 0:
                            x0 = lm.x
                            y0 = lm.y

                            if list_position == -1:
                                prevx = x0
                                prevy = y0
                                list_position = list_position + 1

                            list[list_position] = x0 - prevx
                            list[list_position + 1] = y0 - prevy
                            list_position = list_position + 2
                            prevx = x0
                            prevy = y0

                        elif id == 1 or id == 4 or id == 5 or id == 8 or id == 9 or id == 12 or id == 13 or id == 16 or id == 17 or id == 20:
                            list[list_position] = lm.x - x0
                            list[list_position+1] = lm.y - y0
                            list_position = list_position + 2

                    mpDraw.draw_landmarks(img, handlandmarks)  # dibujar los puntos de la mano
                    cv2.imshow("image", cv2.flip(img, 1))
                    cv2.waitKey(1)

                    q.put(list.copy())
                    list_position = 0
