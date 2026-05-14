# import tensorflow as tf
# import numpy as np
# from librosa import load, feature
#
# # Function to preprocess new data
# def preprocess_new_data(data_path, sr=22050, n_mfcc=13):
#     y, sr = load(data_path, sr=sr)
#     mfccs = feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
#     mfccs_scaled = mfccs.T[:65]  # Assuming same preprocessing as training data
#     # Flatten the MFCCs to match the shape expected by the model
#     flattened_mfccs = mfccs_scaled.flatten()
#     return np.expand_dims(flattened_mfccs, axis=0)  # Add batch dimension
#
# # Load the trained model
# model = tf.keras.models.load_model(r'E:\New folder\AUTISM_DETECTION\myapp\fake_audio_detector.h5')
#
# # Function to predict whether the audio is real or fake
# def predict_audio(data_path, threshold=0.5):
#     # Preprocess the new data
#     processed_data = preprocess_new_data(data_path)
#     # Predict using the loaded model
#     prediction = model.predict(processed_data)
#     # Determine the class based on the threshold
#     if prediction >= threshold:
#         class_label = 'Real'
#     else:
#         class_label = 'Fake'
#     # Return the prediction and confidence level
#     return class_label, prediction[0][0]


import tensorflow as tf
import numpy as np
from librosa import load, feature

# Load the trained model
model = tf.keras.models.load_model(r'C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\audio_detector2.h5')


def preprocess_new_data(data_path, sr=22050, n_mfcc=13):
    # Load audio file
    y, sr = load(data_path, sr=sr)

    # Extract MFCC
    mfccs = feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    # Ensure exactly 60 frames (model input requirement)
    mfccs = mfccs[:, :60]

    # Pad if shorter than 60
    if mfccs.shape[1] < 60:
        pad_width = 60 - mfccs.shape[1]
        mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')

    # Add channel dimension → (13,60,1)
    mfccs = np.expand_dims(mfccs, axis=-1)

    # Add batch dimension → (1,13,60,1)
    mfccs = np.expand_dims(mfccs, axis=0)

    return mfccs


def predict_audio(data_path, threshold=0.5):
    # Preprocess input
    processed_data = preprocess_new_data(data_path)

    # Model prediction
    prediction = model.predict(processed_data)[0][0]

    # Class assignment
    if prediction >= threshold:
        class_label = "Real"
    else:
        class_label = "Fake"

    return class_label, float(prediction)

