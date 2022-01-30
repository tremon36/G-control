
import cv2
import mediapipe as mp
import threading
import gesture1
import gesture2
import gesture3
import gesture4
import gesture5
import gesture6
import gesture7
import gesture8
import numpy as np
import tensorflow
from tensorflow import keras


class Traductor:
    data = np.empty((1,440))
    haveControl = True
    LONGITUD_GRABACION = 20
    model = keras.models.load_model("model/saved")
    inicio = True

    def shiftLeft(self):
        i = 0
        self.data[0][22] = 0
        self.data[0][23] = 0

        while i < 418:
            self.data[0][i] = self.data[0][i+22]
            i = i + 1


    def __init__(self):
        self.haveControl = True
        self.lastFramePositions = True

    def awake(self):
        self.haveControl = True

    def terminarPrograma(self):
        self.inicio = False

    def _getGesture(self, listaGlobal):
        probabilities = self.model.predict(listaGlobal)
        maxProb = -1
        indexOfMaxProb = -1
        currentIndex = 1
        for probability in probabilities[0]:
            if probability > maxProb:
                maxProb = probability
                indexOfMaxProb = currentIndex
            currentIndex = currentIndex + 1
        return indexOfMaxProb

    def run(self):

        self.inicio = True
        recording = 0

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 192)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 108)

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1)
        mpDraw = mp.solutions.drawing_utils

        prevx = 0
        prevy = 0
        position = 0

        while self.inicio:

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
                                if recording == 0:
                                    prevx = x0
                                    prevy = y0
                                if position == 440:
                                    self.shiftLeft()
                                    position = position - 22
                                self.data[0][position] = x0 - prevx
                                self.data[0][position+1] = y0 -prevy
                                position = position + 2
                                prevx = x0
                                prevy = y0
                            elif id == 1 or id == 4 or id == 5 or id == 8 or id == 9 or id == 12 or id == 13 or id == 16 or id == 17 or id == 20:
                                self.data[0][position] = lm.x - x0
                                self.data[0][position + 1] = lm.y - y0
                                position = position + 2

                        mpDraw.draw_landmarks(img, handlandmarks)  # dibujar los puntos de la mano
                    if recording < self.LONGITUD_GRABACION:
                        recording = recording + 1
                    if self.haveControl:
                        print("Traductor got control")
                        gesture = self._getGesture(self.data)
                        print("detected gesture: "+str(gesture))
                        if gesture == 1:
                            #  start new thread with the gesture control program
                            thread = threading.Thread(target=gesture1.run,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 2:
                            thread = threading.Thread(target=gesture2.run,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 3:
                            thread = threading.Thread(target=gesture3.run,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 4:
                            thread = threading.Thread(target=gesture4.run,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 5:
                            thread = threading.Thread(target=gesture5.run,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 6:
                            thread = threading.Thread(target=gesture6.run,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 7:
                            thread = threading.Thread(target=gesture7.playpause,args=[self])
                            self.haveControl = False
                            thread.start()
                        elif gesture == 8:
                            thread = threading.Thread(target=gesture8.close,args=[self])
                            self.haveControl = False
                            thread.start()

                cv2.imshow("image", cv2.flip(img, 1))
                cv2.waitKey(1)
