import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# --- Set parameters manually ---
image_dir =  r'C:\Users\USER\Desktop\softwaresss\dataset\dataset'
output_graph = 'maincode/output_graph.h5'
output_labels = 'maincode2/output_labels.txt'
how_many_training_steps = 20
learning_rate = 0.0001
train_batch_size = 32
final_tensor_name = 'final_result'


flip_left_right = True
test_image_path = r"C:\Users\USER\Desktop\softwaresss\dataset\dataset\Autistic\qc_d99eda5986734e47bb582d1967ee5788.gif"


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







def predict_image(model, label_path, image_path):
    image_data = tf.io.read_file(image_path)

    # Automatically detect image type
    image = tf.image.decode_image(image_data, channels=3)
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
# pathh=r'C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\media\.png'
if os.path.exists(test_image_path):
    predict_image(model, output_labels, test_image_path)
else:
    print(" No test image provided or file not found.")

    #D:\AI\DATA_SET\Covid19-dataset\train\Covid\07.jpg
    #D:\AI\DATA_SET\Covid19-dataset\train\Normal\06.jpeg
    #D:\AI\DATA_SET\Covid19-dataset\train\Viral Pneumonia\012.jpeg








