import pathlib
import numpy as np

examples_list = []

def _loadTypeData(typeExamplesPath) :
    for filename in pathlib.Path("trainingFiles/"+typeExamplesPath).glob('*'): # para todos los archivos en un directorio
        file = open(filename,'r')
        line = list(filter(lambda ch: ch not in "[]() ",file.readline())) # eliminar signos de puntuacion excepto ","
        line_string = "".join(line)
        list2 = [float(i) for i in line_string.split(",")] # crear una lista con todos los numeros que esten en el archivo en orden
        if len(list2) != 440 :
            print("Error in file: "+file.name)
        iteration = 23
        while iteration < 440: # para arreglar el bug en el grabador de gestos. La coordenada y del movimiento entre fotogramas se guardaba de forma absoluta
            list2[iteration] = list2[iteration] - list2[iteration-22]
            iteration = iteration + 22
        examples_list.append(list2)


def loadData(firstGestureCode,lastGestureCode) :
    examples_list.clear()
    for i in range(firstGestureCode,lastGestureCode+1):
         _loadTypeData(str(i))
    return np.array(examples_list)








