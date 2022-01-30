import math
import time
import pyautogui


def run(elTraductor):
    pyautogui.FAILSAFE = False
    while checkCondition(elTraductor.data) :
        X1 = -(elTraductor.data[0][418] + elTraductor.data[0][426] - elTraductor.data[0][404])
        Y1 = elTraductor.data[0][419] + elTraductor.data[0][427] - elTraductor.data[0][405]
        X2 = -(elTraductor.data[0][396] + elTraductor.data[0][404] - elTraductor.data[0][382])
        Y2 = elTraductor.data[0][397] + elTraductor.data[0][405] - elTraductor.data[0][383]
        X3 = -(elTraductor.data[0][374] + elTraductor.data[0][382] - elTraductor.data[0][360])
        Y3 = elTraductor.data[0][375] + elTraductor.data[0][383] - elTraductor.data[0][361]

        media_x = (X1 + X2 + X3) / 3
        media_Y = (Y1 + Y2 + Y3) / 3

        thumb = [elTraductor.data[0][422],elTraductor.data[0][423]]
        index = [elTraductor.data[0][426],elTraductor.data[0][427]]
        indexBase = [elTraductor.data[0][424]], elTraductor.data[0][425]



        distNorm = distanciaPuntos(index,indexBase)
        distThumToIndexBase = distanciaPuntos(indexBase,thumb)




        print("distancia pulgar : "+ str(distThumToIndexBase/ distNorm))

        if (distThumToIndexBase/distNorm) < 0.25 :
            pyautogui.click()


        if abs(media_x) > 0.001 and abs( media_Y) > 0.001:

            #print("X: "+ str(media_x)+" , X2: "+str(media_Y))
            pyautogui.move( media_x * 30000 , media_Y* 20000)

        elif abs( media_x) > 0.0005 and abs( media_Y) > 0.0005:

            pyautogui.move( media_x * 8500,media_Y* 5500)
            #print("2222222222")

        elif abs(media_x) > 0.00025 and abs(media_Y) > 0.00025:

            pyautogui.move(media_x * 5000, media_Y * 2000)
            #print("3333333333")

        else :

            pyautogui.move( media_x * 400,media_Y * 150)
            #print("4444444444")

    elTraductor.awake()


def checkCondition(lastFramePositions):

    index = [lastFramePositions[0][426], lastFramePositions[0][427]]
    indexBase = [lastFramePositions[0][424]], lastFramePositions[0][425]
    middle = [lastFramePositions[0][430], lastFramePositions[0][431]]
    ring = [lastFramePositions[0][434], lastFramePositions[0][435]]
    pinky = [lastFramePositions[0][438], lastFramePositions[0][439]]
    thumbBase = [lastFramePositions[0][420], lastFramePositions[0][421]]

    distMiddleTo1 = distanciaPuntos(middle, thumbBase)
    distRingTo1 = distanciaPuntos(ring, thumbBase)
    distpinkyTo1 = distanciaPuntos(pinky, thumbBase)
    distNorm = distanciaPuntos(index, indexBase)


     try:
        return distMiddleTo1/distNorm < 0.8 and distRingTo1/distNorm < 0.9 and distpinkyTo1/distNorm < 0.8
    except ZeroDivisionError:
        return True

def distanciaPuntos(punto1, punto2):
    return math.sqrt(pow(punto1[0] - punto2[0], 2) + pow(punto1[1] - punto2[1], 2))
