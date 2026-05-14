import os
import cv2

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
# --- Set parameters manually ---
image_dir = r'C:\Users\USER\Desktop\softwaresss\dataset\dataset'
output_graph = 'autismm/output_graph.h5'
output_labels = 'autismm/output_labels.txt'
how_many_training_steps = 1
learning_rate = 0.0001
train_batch_size = 32
final_tensor_name = 'final_result'
flip_left_right = True
test_image_path = r''

# --- Create model ---
def create_inception_graph(num_classes):
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3), pooling='avg')

    for layer in base_model.layers[-50:]:
        layer.trainable = True

    x = base_model.output
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax', name=final_tensor_name)(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model


# ---  Prepare data generators ---
def prepare_data_generators():
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        brightness_range=[0.8, 1.2],
        horizontal_flip=flip_left_right
    )

    val_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        image_dir,
        target_size=(224, 224),
        batch_size=train_batch_size,
        class_mode='categorical'
    )

    validation_generator = val_datagen.flow_from_directory(
        image_dir,
        target_size=(224, 224),
        batch_size=train_batch_size,
        class_mode='categorical'
    )

    return train_generator, validation_generator

# --- Predict a single image ---
def predict_image(model, label_path, image_path):
    print(label_path,image_path)
    image_data = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image_data, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)

    predictions = model.predict(image)

    label_lines = [line.strip() for line in open(label_path)]
    top_class_id = np.argmax(predictions[0])
    top_class_label = label_lines[top_class_id]
    confidence = float(predictions[0][top_class_id])

    print(f"\n Prediction on image: {image_path}")
    print(f"  Predicted: {top_class_label}, Confidence: {confidence:.4f}")
    return top_class_label

from tensorflow.keras.layers import Input, Reshape, Conv2DTranspose, Conv2D, LeakyReLU, Flatten, Dense, BatchNormalization
from tensorflow.keras.models import Sequential

augment_with_gan = True
num_generated_images = 50  # per class
latent_dim = 100

def build_generator(latent_dim=100):
    model = Sequential()
    model.add(Dense(128 * 7 * 7, input_dim=latent_dim))
    model.add(LeakyReLU(0.2))
    model.add(Reshape((7, 7, 128)))
    model.add(Conv2DTranspose(128, kernel_size=4, strides=2, padding='same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    model.add(Conv2DTranspose(64, kernel_size=4, strides=2, padding='same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))
    model.add(Conv2DTranspose(3, kernel_size=7, activation='tanh', padding='same'))
    return model

def generate_and_save_images(generator, class_folder, num_images, latent_dim=100):
    os.makedirs(class_folder, exist_ok=True)
    for i in range(num_images):
        noise = np.random.normal(0, 1, (1, latent_dim))
        generated_image = generator.predict(noise)
        image = (generated_image[0] * 127.5 + 127.5).astype(np.uint8)
        image = cv2.resize(image, (224, 224))
        cv2.imwrite(os.path.join(class_folder, f"gan_gen_{i:04d}.jpg"), image)

if augment_with_gan:
    print("Training GAN to generate synthetic images...")
    generator = build_generator()
    generator.compile(optimizer='adam', loss='binary_crossentropy')

    for class_name in os.listdir(image_dir):
        class_path = os.path.join(image_dir, class_name)
        if os.path.isdir(class_path):
            print(f"Generating GAN images for class: {class_name}")
            generate_and_save_images(generator, class_path, num_generated_images)


# ---  Main Flow ---
print(" Loading dataset...")
num_classes = len(os.listdir(image_dir))

print(" Creating model...")
model = create_inception_graph(num_classes)

print(" Preparing data...")
train_generator, validation_generator = prepare_data_generators()

model.compile(optimizer=Adam(learning_rate=learning_rate),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)

print(" Training...")
model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=how_many_training_steps,
    validation_data=validation_generator,
    validation_steps=len(validation_generator),
    callbacks=[early_stop, reduce_lr]
)

#  Save model and labels
os.makedirs(os.path.dirname(output_graph), exist_ok=True)
os.makedirs(os.path.dirname(output_labels), exist_ok=True)

print(f" Saving model to {output_graph}")
model.save(output_graph)

print(f" Saving labels to {output_labels}")
with open(output_labels, 'w') as f:
    for class_label in train_generator.class_indices:
        f.write(f"{class_label}\n")

print(" Training complete!")

#  Prediction
pathh=r'D:\AI\DATA_SET\adhd data set\train\non-adhd-frames\frame_0000 (2).jpg'
if os.path.exists(test_image_path):
    predict_image(model, output_labels, pathh)
else:
    print(" No test image provided or file not found.")

    import os
    import cv2


    def extract_frames(input_video_path, output_folder_path):
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        video_capture = cv2.VideoCapture(0)
        frame_count = 0
        adhd_count = 0
        non_adhd_count = 0
        max_frames = 100

        while True:
            success, frame = video_capture.read()
            if not success:
                break
            if frame_count >= max_frames:
                break

            image_filename = os.path.join(output_folder_path, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(image_filename, frame)

            if os.path.exists(image_filename):
                print(f"Predicting frame {frame_count}")

            prediction = predict_image(model, output_labels, image_filename)

            if "non-adhd" in prediction:
                non_adhd_count += 1
            elif "adhd" in prediction:
                adhd_count += 1
            else:
                print("No test image provided or file not found.")

            frame_count += 1
        total = adhd_count + non_adhd_count
        video_capture.release()
        cv2.destroyAllWindows()

        print(f"Extracted {frame_count} frames to {output_folder_path}")
        print("*************************************")
        print(f"Total ADHD frames: {adhd_count}")
        print("*************************************")
        print(f"Total Non-ADHD frames: {non_adhd_count}")
        print("*************************************")
        print(f"Total frames: {total}")
        print("*************************************")
        adhd_percentage = (adhd_count / total) * 100
        print("*************************************")
        print(f"percentage of adhd_count: {adhd_percentage}")
        non_adhd_percentage = (non_adhd_count / total) * 100
        print("*************************************")
        print(f"percentage of non adhd_count: {non_adhd_percentage}")
        print("*************************************")





input_video = 0#r"D:\AI\DATA_SET\adhd data set\test\test.mp4"
output_directory = "ll"

extract_frames(input_video, output_directory)


