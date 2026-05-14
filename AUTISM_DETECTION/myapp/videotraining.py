# import cv2
# import os
# import json
# import numpy as np
# from joblib import load
# from django.http import JsonResponse
# from django.core.files.storage import FileSystemStorage
#
# # ---------------------------------------------------------------------------
# # NOTE: Your Autism Video Training Dataset is located here:
# # DATASET PATH FOR TRAINING:  E:\Regional\AUTISM\Video\Hand Flapping Classifier Dataset
# # This path is ONLY for training your model, NOT for prediction.
# # ---------------------------------------------------------------------------
# from myapp.views import user_check, op_order
#
# video_path=r"E:\Regional\AUTISM\Video\Hand Flapping Classifier Dataset\\"
# def process_video(video_path):
#     oplist = []
#     opdict = {}
#
#     cap = cv2.VideoCapture(video_path)
#
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return "NA"
#
#     frame_count = 0
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         frame_count += 1
#
#         # Process every 100th frame
#         if frame_count % 100 == 0:
#             temp_path = "sample.png"
#             cv2.imwrite(temp_path, frame)
#
#             res = user_check(temp_path)
#             if res not in oplist:
#                 oplist.append(res)
#                 opdict[res] = 0
#
#             opdict[res] += 1
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     # Return most frequent prediction
#     sorted_keys = sorted(opdict, key=opdict.get, reverse=True)[0]
#     return sorted_keys
#
#
#
# def predict_autism_video(request):
#     model_path = r'E:\New folder\AUTISM_DETECTION\myapp\AutismDecisionTree.joblib'
#     loaded_model = load(model_path)
#
#     if request.method == "POST":
#
#         answers = json.loads(request.POST.get('answers'))
#         age = int(request.POST.get('age'))
#         sex = request.POST.get('sex')
#         jaundice = request.POST.get('jaundice')
#         family_asd = request.POST.get('family_asd')
#
#         # --------------------------
#         # SAVE USER UPLOADED VIDEO
#         # --------------------------
#         video = request.FILES['video']
#         fs = FileSystemStorage()
#
#         videopath = fs.save(video.name, video)  # saved inside media/
#         full_video_path = os.path.join(
#             r"E:\New folder\AUTISM_DETECTION\media",
#             videopath
#         )
#
#         print("Saved Video Path:", full_video_path)
#
#         vres = process_video(full_video_path)
#
#         # Convert categorical values
#         sex_num = 0 if sex == 'm' else 1
#         jaundice_num = 1 if jaundice.lower() == 'yes' else 0
#         family_asd_num = 1 if family_asd.lower() == 'yes' else 0
#
#         # Validate 50 answers
#         if len(answers) != 50:
#             return JsonResponse({'status': 'error', 'message': 'Exactly 50 answers are required'})
#
#         # Map answers
#         mapped_answers = [op_order[i][ans - 1] for i, ans in enumerate(answers)]
#
#         # 10 categories (5 questions each)
#         ascorelist = []
#         for i in range(10):
#             s = sum(mapped_answers[i * 5:(i * 5) + 5])
#             ascorelist.append(s)
#
#         extra_features = [age, sex_num, jaundice_num, family_asd_num]
#
#         final_features = ascorelist + extra_features
#
#         X = np.array(final_features).reshape(1, -1)
#         prediction = loaded_model.predict(X)[0]
#
#         result_text = "AUTISM YES" if prediction > 0 else "AUTISM NO"
#
#         return JsonResponse({
#             'status': 'ok',
#             'prediction': "Q&A Result is " + result_text + "\nVideo result is " + vres
#         })
#
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

# -----------------------------------------
#        LOAD .MP4 AND EXTRACT FRAMES
# -----------------------------------------
def load_video(path, max_frames=60, resize=(128, 128)):
    cap = cv2.VideoCapture(path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, resize)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)

        if len(frames) >= max_frames:
            break

    cap.release()

    # If fewer frames, pad with zeros
    while len(frames) < max_frames:
        frames.append(np.zeros_like(frames[0]))

    return np.array(frames)


# -----------------------------------------
#        LOAD DATASET
# -----------------------------------------
dataset_path = r"D:\Desktop\AUTISM\Video\Converted_Videos"

X = []
y = []

classes = os.listdir(dataset_path)
label_idx = 0

for cls in classes:
    cls_path = os.path.join(dataset_path, cls)

    print("Class:", cls)

    for sub in os.listdir(cls_path):
        sub_path = os.path.join(cls_path, sub)

        for file in os.listdir(sub_path):
            if file.endswith(".mp4"):
                video_path = os.path.join(sub_path, file)
                print("   Loading video:", file)

                frames = load_video(video_path)
                X.append(frames)
                y.append(label_idx)

    label_idx += 1

X = np.array(X)
y = np.array(y)

print("Loaded videos:", len(X))
print("X shape:", X.shape)  # (samples, 60, 128, 128, 3)

# -----------------------------------------
#     TRAIN-TEST SPLIT
# -----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------------------
#       CNN + LSTM MODEL
# -----------------------------------------
model = models.Sequential([
    layers.TimeDistributed(
        layers.Conv2D(32, (3,3), activation='relu'),
        input_shape=(60, 128, 128, 3)
    ),
    layers.TimeDistributed(layers.MaxPooling2D((2,2))),
    layers.TimeDistributed(layers.Conv2D(64, (3,3), activation='relu')),
    layers.TimeDistributed(layers.MaxPooling2D((2,2))),
    layers.TimeDistributed(layers.Flatten()),

    layers.LSTM(64),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
model.summary()

# -----------------------------------------
#       TRAIN
# -----------------------------------------
model.fit(X_train, y_train, epochs=10, batch_size=4)

# -----------------------------------------
#       SAVE MODEL
# -----------------------------------------
model.save("autism_video_lstm_model.h5")
print("Model Saved!")

# -----------------------------------------
#       EVALUATE
# -----------------------------------------
loss, acc = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", acc)
