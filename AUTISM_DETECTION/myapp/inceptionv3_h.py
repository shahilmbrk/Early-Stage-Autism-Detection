from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt

# Image size
img_width, img_height = 299, 299
num_classes = 5

train_data_dir = r"C:\Users\USER\Desktop\softwaresss\dataset\dataset"
val_data_dir = r"C:\Users\USER\Desktop\softwaresss\dataset\dataset"

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode="categorical"
)

val_generator = val_datagen.flow_from_directory(
    val_data_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode="categorical"
)

# Load base model
base_model = InceptionV3(weights="imagenet", include_top=False,
                         input_shape=(img_width, img_height, 3))

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(learning_rate=0.0001),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

# Train if model not exists
if not os.path.exists("inceptionv3.h5"):

    history = model.fit(
        train_generator,
        epochs=5,
        validation_data=val_generator
    )

    model.save("inceptionv3.h5")

    with open('iv3_history.pkl', 'wb') as f:
        pickle.dump(history.history, f)

    # Plot accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title("Model Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(["Train", "Validation"])
    plt.show()

else:
    model.load_weights("inceptionv3.h5")

# ---------- Prediction ----------

test_image_path = r"C:\Users\USER\Desktop\softwaresss\dataset\dataset\class1\image1.jpg"

img = image.load_img(test_image_path, target_size=(299, 299))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

pred = model.predict(x)
predicted_class = np.argmax(pred, axis=1)

print("Predicted class:", predicted_class[0])
