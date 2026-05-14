import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import os

from myapp.mfcc_fn import mfccfn

X=[]
y=[]
ls=os.listdir(r"E:\Regional\AUTISM\dataset")
j=0
for i in ls:
    files=os.listdir(os.path.join(r"E:\Regional\AUTISM\dataset",i))

    for f in files:
        fn=os.path.join(r"E:\Regional\AUTISM\dataset",i,f)
        fe=mfccfn(fn)
        print(fn)
        X.append([fe])
        y.append(j)
    j=j+1


# Load and preprocess your MFCC data
# X should be your MFCC data with shape (num_samples, num_frames, num_mfcc_coefficients)
# y should be labels (1 for real, 0 for fake)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
num_frames=13
num_mfcc_coefficients=60
# Define the CNN-RNN hybrid model
model = keras.Sequential()

# CNN layers
model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(num_frames, num_mfcc_coefficients, 1)))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Flatten())

# RNN layers
model.add(layers.LSTM(64, return_sequences=True))
model.add(layers.LSTM(64))

# Fully connected layers
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Reshape the data for CNN
X_train=np.array(X_train)
X_test=np.array(X_test)
X_train = X_train.reshape(X_train.shape[0], num_frames, num_mfcc_coefficients, 1)
X_test = X_test.reshape(X_test.shape[0], num_frames, num_mfcc_coefficients, 1)
y_train=np.array(y_train)
# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)


y_test=np.array(y_test)
# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}, Test Accuracy: {test_accuracy}")
