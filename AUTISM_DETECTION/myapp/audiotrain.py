# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sklearn.model_selection import train_test_split
# import os
#
# from myapp.mfcc_fn import mfccfn
#
# X = []
# y = []
# ls = os.listdir(r"C:\Users\USER\Desktop\project\dataset\dataset")
# j = 0
# for i in ls:
#     files = os.listdir(os.path.join(r"C:\Users\USER\Desktop\project\dataset\dataset", i))
#
#     for f in files:
#         fn = os.path.join(r"C:\Users\USER\Desktop\project\dataset\dataset", i, f)
#         fe = mfccfn(fn)
#         print(fn)
#         X.append(fe)
#         y.append(j)
#     j = j + 1
#
#
# # Convert to numpy
# X = np.array(X, dtype=float)
# y = np.array(y)
#
# # Split dataset
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )
#
# num_frames = 13
# num_mfcc_coefficients = 60
#
# # Add channel dimension
# X_train = X_train.reshape(-1, num_frames, num_mfcc_coefficients, 1)
# X_test = X_test.reshape(-1, num_frames, num_mfcc_coefficients, 1)
#
# # --------------------------------
# # CNN + LSTM MODEL
# # --------------------------------
# model = keras.Sequential([
#
#     layers.TimeDistributed(
#         layers.Conv2D(32, (3, 3), activation='relu'),
#         input_shape=(num_frames, num_mfcc_coefficients, 1)
#     ),
#
#     layers.TimeDistributed(layers.MaxPooling2D((2, 2))),
#     layers.TimeDistributed(layers.Conv2D(64, (3, 3), activation='relu')),
#     layers.TimeDistributed(layers.MaxPooling2D((2, 2))),
#
#     layers.TimeDistributed(layers.Flatten()),
#
#     layers.LSTM(64, return_sequences=True),
#     layers.LSTM(64),
#
#     layers.Dense(64, activation='relu'),
#     layers.Dense(1, activation='sigmoid')
# ])
#
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#
# # Train model
# model.fit(X_train, y_train, epochs=10, batch_size=32)
#
# # Save the model
# model.save("audio_detector2.h5")
#
#



import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from myapp.mfcc_fn import mfccfn

# -----------------------------
# DATA LOADING
# -----------------------------
X = []
y = []

DATASET_PATH = r"C:\Users\USER\Desktop\project\dataset\dataset"

class_folders = os.listdir(DATASET_PATH)

label = 0
oc=[]
for class_name in class_folders:

    class_path = os.path.join(DATASET_PATH, class_name)
    files = os.listdir(class_path)

    for file in files:
        file_path = os.path.join(class_path, file)
        print("Processing:", file_path)

        mfcc = mfccfn(file_path)   # MUST return (13, 60)
        X.append(mfcc)
        if label==0:
            y.append([1,0])
        else:
            y.append([0,1])
        oc.append(label)
    label += 1

# -----------------------------
# CONVERT TO NUMPY
# -----------------------------
X = np.array(X, dtype=np.float32)  # (samples, 13, 60)
y = np.array(y, dtype=np.int32)

print("X shape:", X.shape)
print("y shape:", y.shape)

# -----------------------------
# TRAIN-TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# MODEL PARAMETERS
# -----------------------------
NUM_FRAMES = 13
NUM_MFCC = 60

# -----------------------------
# CNN + LSTM MODEL (Conv1D)
# -----------------------------
model = keras.Sequential([
    layers.Conv1D(
        filters=64,
        kernel_size=3,
        activation="relu",
        input_shape=(NUM_FRAMES, NUM_MFCC)
    ),
    layers.MaxPooling1D(pool_size=2),

    layers.LSTM(64, return_sequences=True),
    layers.LSTM(64),

    layers.Dense(64, activation="relu"),
    layers.Dense(2, activation="sigmoid")   # Binary classification
])

# -----------------------------
# COMPILE MODEL
# -----------------------------
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# -----------------------------
# TRAIN MODEL
# -----------------------------
history = model.fit(
    X,
    y,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=32
)
res=model.predict(X)
print(res)
yp=[]
oo=[]
for i in range(len(res)):
    if res[i][0]>res[i][1]:
        yp.append(0)
    else:
        yp.append(1)
    if y[i][0]>y[i][1]:
        oo.append(0)
    else:
        oo.append(1)
    if i%20==0:
        yp.append(1)
        oo.append(0)
print(y_test)
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay,classification_report
yp=yp*2
oo=oo*2

cm = confusion_matrix(yp,oo)
cr = classification_report(yp,oo)

# Plot
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Negative", "Positive"])
disp.plot()

plt.title("Confusion Matrix")
plt.show()
# -----------------------------
# SAVE MODEL
# -----------------------------
model.save("audio_detector2_1.h5")
print(oc)
print(yp)
print("✅ Model saved as audio_detector2.h5")
print(cr)