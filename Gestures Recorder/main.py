import collections

import cv2
import mediapipe as mp
import threading
import keyboard
import time

LONGITUD_GRABACION = 20
recording = LONGITUD_GRABACION + 1
listaInterna = []
listaGlobal = []

print("[Advertencia] Si no se pone bien se sobreescriben los datos anteriores.\n Primer indice de archivo de grabacion a utilizar:")
lastFileIndex = int(input())
print("Codigo del gesto que se va a grabar: ")
gestureToRecord = int(input())
print("pulsar espacio para empezar a grabar. El archivo se guarda automaticamente al pasar el tiempo LONGITUD_GRABACION")



def pressListerner():
    while True:
        if keyboard.is_pressed(' '):
            global recording
            global vectors8
            vectors8 = []
            recording = 0
            time.sleep(1)
        time.sleep(0.05)


thread = threading.Thread(target=pressListerner)
thread.start()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 192)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 108)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands= 1)
mpDraw = mp.solutions.drawing_utils

prevx = 0
prevy = 0

while True:

    success, img = cap.read()
    if success:

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:  # si hay una mano en la pantalla
            if recording < LONGITUD_GRABACION:
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
                            listaInterna.append((x0 - prevx, y0 - prevy))
                            prevx = x0
                            prey = y0 #bug conocido, se corrige en el lector de datos del entrenador de la red neuronal
                        elif id == 1 or id == 4 or id == 5 or id == 8 or id == 9 or id == 12 or id == 13 or id == 16 or id == 17 or id == 20:
                            listaInterna.append((lm.x - x0, lm.y - y0))

                    mpDraw.draw_landmarks(img, handlandmarks)  # dibujar los puntos de la mano
                recording = recording + 1
                listaGlobal.append(listaInterna)
                listaInterna = []
            else:
                if recording == LONGITUD_GRABACION:
                    print("Succesfully recorded")
                    print(listaGlobal)
                    output = open('output_files/'+str(gestureToRecord) + '_' + str(lastFileIndex),'w')
                    output.write(str(listaGlobal))
                    output.close()
                    listaGlobal = []
                    recording = recording + 1
                    lastFileIndex = lastFileIndex + 1



        cv2.imshow("image", cv2.flip(img, 1))
        cv2.waitKey(1)
