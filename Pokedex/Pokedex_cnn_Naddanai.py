import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

img_width, img_height = 128, 128
batch_size = 32

train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_set = train_datagen.flow_from_directory(
    r'C:\Users\nparo\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\Pokedex\output\train',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

test_set = test_datagen.flow_from_directory(
    r'C:\Users\nparo\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\Pokedex\output\test',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

val_set = test_datagen.flow_from_directory(
    r'C:\Users\nparo\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\Pokedex\output\val',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

num_classes = train_set.num_classes
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
]) 
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_set, epochs=15, validation_data=val_set)
loss, accuracy = model.evaluate(test_set)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}") 