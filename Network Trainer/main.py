import DataLoader
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import activations
from keras import optimizers
from keras import losses
from keras import metrics

training_inputs = DataLoader.loadData(1,9)
expected_outputs = np.r_[
    np.tile([[1,0,0,0,0,0,0,0,0]],(859,1)), #numero de ejemplos del primer gesto
    np.tile([[0,1,0,0,0,0,0,0,0]],(435,1)), #numero de ejemplos del segundo gesto ....
    np.tile([[0,0,1,0,0,0,0,0,0]],(424,1)),
    np.tile([[0,0,0,1,0,0,0,0,0]],(342,1)),
    np.tile([[0,0,0,0,1,0,0,0,0]],(278,1)),
    np.tile([[0,0,0,0,0,1,0,0,0]],(221,1)),
    np.tile([[0,0,0,0,0,0,1,0,0]],(204,1)),
    np.tile([[0,0,0,0,0,0,0,1,0]],(243,1)),
    np.tile([[0,0,0,0,0,0,0,0,1]],(1191,1)), # numero de ejmplos que no son nada (basura)
]
print(training_inputs.shape)
print(expected_outputs.shape)


model = keras.Sequential([
    keras.layers.Dense(440, input_dim=440,activation = activations.relu),
    keras.layers.Dense(220, activation=  activations.relu),
    keras.layers.Dense(110, activation=  activations.relu),
    keras.layers.Dense(55, activation=activations.relu),
    keras.layers.Dense(9, activation= activations.softmax)
])

model.compile(optimizer = "adam", loss = "categorical_crossentropy",
              metrics = ["accuracy"])

model.fit(training_inputs,expected_outputs,epochs = 12,shuffle = True)

test_loss, test_acc = model.evaluate(training_inputs,expected_outputs)

print("Tested Acc:",test_acc)

model.save("model/saved")

model2 = keras.models.load_model("model/saved")

training_inputs = DataLoader.loadData(8888,8888)
print(training_inputs.shape)
print(len(training_inputs)-1)

for i in range (0,len(training_inputs)-1):
    training_inputs2 = np.reshape(training_inputs[i],(1,440),order = 'C')
    result = model2.predict(training_inputs2)
    maximum = -1.0
    maximumIndex = -1

    for element in result :
        index = 1
        for element2 in element:
            if element2 > maximum:
                maximum = element2
                maximumIndex = index

            index = index + 1
            print("{:.2f}".format(element2))

        print()
        print("resultado: "+str(maximumIndex)+ "con: "+str(maximum))
        print()

print("===============================================================================")

training_inputs = DataLoader.loadData(11,18)
print(training_inputs.shape)
print(training_inputs.size)

for i in range (0,len(training_inputs)-1):
    training_inputs2 = np.reshape(training_inputs[i],(1,440),order = 'C')
    result = model2.predict(training_inputs2)
    maximum = -1.0
    maximumIndex = -1

    for element in result :
        index = 1
        for element2 in element:
            if element2 > maximum:
                maximum = element2
                maximumIndex = index

            index = index + 1
            print("{:.2f}".format(element2))

        print()
        print("resultado: "+str(maximumIndex) + " con: "+str(maximum))
        print()


