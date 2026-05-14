# # coding: utf-8
#
# # In[ ]:
# import os
#
# import tensorflow as tf
#
# import keras
# # from keras.engine.saving import load_model
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
# from keras.layers import Dense, Activation, Dropout, Flatten
#
# from keras.preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator
#
# import numpy as np
#
# #------------------------------
# # sess = tf.Session()
# # keras.backend.set_session(sess)
# #------------------------------
# #variables
# num_classes =3
# batch_size = 40
# epochs = 7
# #------------------------------
#
# import os, cv2, keras
# import numpy as np
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Flatten
# from keras.layers import Conv2D, MaxPooling2D
# # from keras.engine.saving import load_model
#
# from tensorflow.keras.models import load_model
#
# # manipulate with numpy,load with panda
# import numpy as np
# # import pandas as pd
#
# # data visualization
# import cv2
# import matplotlib
# import matplotlib.pyplot as plt
# # import seaborn as sns
#
# # get_ipython().run_line_magic('matplotlib', 'inline')
#
#
# # Data Import
# def read_dataset(path):
#     data_list = []
#     label_list = []
#     my_list = os.listdir(r'C:\Users\USER\Desktop\softwaresss\dataset\dataset')
#     i=-1
#     for pa in my_list:
#         i=i+1
#         print(pa,"==================")
#         for root, dirs, files in os.walk(r'C:\Users\USER\Desktop\softwaresss\dataset\dataset\\' + pa):
#
#          for f in files:
#             file_path = os.path.join(r'C:\Users\USER\Desktop\softwaresss\dataset\dataset\\'+pa, f)
#             img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#             res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
#             data_list.append(res)
#             # label = dirPath.split('/')[-1]
#             label = i
#             label_list.append(label)
#             # label_list.remove("./training")
#     return (np.asarray(data_list, dtype=np.float32), np.asarray(label_list))
#
# def read_dataset1(path):
#     data_list = []
#     label_list = []
#
#     file_path = os.path.join(path)
#     img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#     res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
#     data_list.append(res)
#     # label = dirPath.split('/')[-1]
#
#             # label_list.remove("./training")
#     return (np.asarray(data_list, dtype=np.float32))
#
# from sklearn.model_selection import train_test_split
# # load dataset
# x_dataset, y_dataset = read_dataset(r"C:\Users\USER\Desktop\softwaresss\dataset\dataset")
# X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=0.2, random_state=0)
#
# y_train1=[]
# for i in y_train:
#     emotion = keras.utils.to_categorical(i, num_classes)
#     print(i,emotion)
#     y_train1.append(emotion)
#
# y_train=y_train1
# x_train = np.array(X_train, 'float32')
# y_train = np.array(y_train, 'float32')
# x_test = np.array(X_test, 'float32')
# y_test = np.array(y_test, 'float32')
#
# x_train /= 255  # normalize inputs between [0, 1]
# x_test /= 255
# print("x_train.shape",x_train.shape)
# x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
# x_train = x_train.astype('float32')
# x_test = x_test.reshape(x_test.shape[0], 48, 48, 1)
# x_test = x_test.astype('float32')
#
# print(x_train.shape[0], 'train samples')
# print(x_test.shape[0], 'test samples')
# # ------------------------------
# # construct CNN structure
#
# model = Sequential()
#
# # 1st convolution layer
# model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48, 48, 1)))
# model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))
#
# # 2nd convolution layer
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))
#
# # 3rd convolution layer
# model.add(Conv2D(128, (3, 3), activation='relu'))
# model.add(Conv2D(128, (3, 3), activation='relu'))
# model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))
#
# model.add(Flatten())
#
# # fully connected neural networks
# model.add(Dense(1024, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(1024, activation='relu'))
# model.add(Dropout(0.2))
#
# model.add(Dense(num_classes, activation='softmax'))
# # ------------------------------
# # batch process
#
# print(x_train.shape)
#
# gen = ImageDataGenerator()
# train_generator = gen.flow(x_train, y_train, batch_size=batch_size)
#
# # ------------------------------
#
# model.compile(loss='categorical_crossentropy'
#               , optimizer=keras.optimizers.Adam()
#               , metrics=['accuracy']
#               )
#
# # ------------------------------
#
# if not os.path.exists("model1.h5"):
#
#     model.fit_generator(train_generator, steps_per_epoch=batch_size, epochs=epochs)
#     model.save("model13.h5")  # train for randomly selected one
# else:
#     model = load_model("model13.h5")  # load weights
# from sklearn.metrics import confusion_matrix
# yp=model.predict_classes(x_test,verbose=0)
# cf=confusion_matrix(y_test,yp)
# print(cf)
# ===============================
# Autism Image Classification CNN
# ===============================

import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# ------------------------------
# Variables
# ------------------------------
num_classes = 3
batch_size = 40
epochs = 30

# ------------------------------
# Dataset Loader (SAFE VERSION)
# ------------------------------
def read_dataset(path):
    data_list = []
    label_list = []

    folders = os.listdir(path)

    for i, folder in enumerate(folders):
        folder_path = os.path.join(path, folder)
        print(folder, "==================")

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                print("Skipping corrupted file:", file_path)
                continue

            img = cv2.resize(img, (48, 48))
            data_list.append(img)
            label_list.append(i)

    return np.array(data_list, dtype=np.float32), np.array(label_list)


# ------------------------------
# Load Dataset
# ------------------------------
dataset_path = r"C:\Users\USER\Desktop\softwaresss\dataset\dataset"

x_dataset, y_dataset = read_dataset(dataset_path)

X_train, X_test, y_train, y_test = train_test_split(
    x_dataset, y_dataset, test_size=0.2, random_state=0
)

# ------------------------------
# Preprocessing
# ------------------------------
x_train = X_train / 255.0
x_test = X_test / 255.0

x_train = x_train.reshape(-1, 48, 48, 1)
x_test = x_test.reshape(-1, 48, 48, 1)

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print("Train shape:", x_train.shape)
print("Test shape:", x_test.shape)

# ------------------------------
# CNN Model
# ------------------------------
model = Sequential()

# 1st Convolution Layer
model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48, 48, 1)))
model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))

# 2nd Convolution Layer
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

# 3rd Convolution Layer
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

model.add(Flatten())

# Fully Connected Layers
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(num_classes, activation='softmax'))

# ------------------------------
# Compile Model
# ------------------------------
model.compile(
    loss='categorical_crossentropy',
    optimizer=keras.optimizers.Adam(),
    metrics=['accuracy']
)

# ------------------------------
# Training
# ------------------------------
model_path = "model16.h5"

if not os.path.exists(model_path):

    gen = ImageDataGenerator()
    train_generator = gen.flow(x_train, y_train, batch_size=batch_size)

    model.fit(
        train_generator,
        steps_per_epoch=len(x_train) // batch_size,
        epochs=epochs
    )

    model.save(model_path)
    print("Model Saved!")

else:
    model = load_model(model_path)
    print("Model Loaded!")

# ------------------------------
# Evaluation
# ------------------------------
y_pred = np.argmax(model.predict(x_test), axis=1)
y_true = np.argmax(y_test, axis=1)

cf = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cf)
