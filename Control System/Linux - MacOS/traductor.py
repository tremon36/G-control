import threading
import gesture1
import gesture2
import gesture3
import gesture4
import gesture6
import gesture7
import gesture8
import gesture5
import capturador
import numpy as np
from tensorflow import keras
from multiprocessing import Process, Queue

class Traductor:
    inicio = True
    q = None
    p = None
    data = None
    haveControl = None
    LONGITUD_GRABACION = 20
    model = None
    recording = None

    def reset(self):
        self.__init__()

    def shiftLeft(self):
        i = 0
        self.data[0][22] = 0
        self.data[0][23] = 0

        while i < 418:
            self.data[0][i] = self.data[0][i + 22]
            i = i + 1

    def terminarPrograma(self):
        self.inicio = False
        self.p.kill()

    def __init__(self):
        self.haveControl = True
        self.lastFramePositions = True
        self.inicio = True
        self.q = Queue()
        self.p = Process(target=capturador.capturarManos, args=(self.q,))
        self.p.start()
        self.data = np.empty((1, 440))
        self.model = keras.models.load_model("model/saved")
        self.recording = 0

    def awake(self):
        self.haveControl = True
        self.data = np.empty((1, 440))
        self.recording = 0

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
        if maxProb > 0.7:
            if indexOfMaxProb == 8: # Caso especial para el 8, tiene que estar muy seguro de que es el 8 porque cierra la ventana
                print(str(maxProb))
                if maxProb > 0.9:
                    return indexOfMaxProb
                else:
                    return 9
            else:
                return indexOfMaxProb
        else:
            return 9

    def run(self):

        position = 0
        self.inicio = True

        while self.inicio:

            lastPositions = self.q.get()  # Extraer nuevas posiciones de la mano del proceso que graba los gestos
            if self.recording == 0:  # Rellenar el primer espacio de la grabacion con coordenada 0 (el otro proceso no hace eso)
                lastPositions[0] = 0
                lastPositions[1] = 0
            if position == 440:  # Si lista llena, realizar ciclo para liberar la ultima posicion
                self.shiftLeft()
                position = position - 22
            for i in range(0,len(lastPositions)):  # Añadir a los datos la lista de elementos pasados por el otro proceso y ajustar flags
                self.data[0][position + i] = lastPositions[i]
            position = position + 22
            self.recording = self.recording + 1

            if self.haveControl:

                print("Traductor got control")
                gesture = self._getGesture(self.data)
                print("detected gesture: " + str(gesture))

                if gesture == 1:
                    #  start new thread with the gesture control program
                    thread = threading.Thread(target=gesture1.run, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 2:
                    thread = threading.Thread(target=gesture2.run, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 3:
                    thread = threading.Thread(target=gesture3.run, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 4:
                    thread = threading.Thread(target=gesture4.run, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 7:
                    thread = threading.Thread(target=gesture7.playpause, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 8:
                    thread = threading.Thread(target=gesture8.close, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 5:
                    thread = threading.Thread(target=gesture5.run, args=[self])
                    self.haveControl = False
                    thread.start()
                if gesture == 6:
                    thread = threading.Thread(target=gesture6.run, args=[self])
                    self.haveControl = False
                    thread.start()

