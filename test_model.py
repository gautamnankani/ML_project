#!/usr/bin/env python3
# coding: utf-8

from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import Sequential
model = Sequential()
#SHYP1
model.add(Convolution2D(filters=32, 
                        kernel_size=(3,3), 
                        activation='relu',
                   input_shape=(64, 64, 3)
                       ))
#EHYP1
model.summary()
model.add(MaxPooling2D(pool_size=(2, 2)))
#SHYP2
model.add(Convolution2D(filters=32, 
                        kernel_size=(3,3), 
                        activation='relu',
                       ))
#EHYP2
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
#SHYP3
model.add(Dense(units=128, activation='relu'))
#EHYP3
model.add(Dense(units=1, activation='sigmoid'))
model.summary()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

from keras_preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)
training_set = train_datagen.flow_from_directory(
        '../dataset/training_set/',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')
test_set = test_datagen.flow_from_directory(
        '../dataset/test_set/',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')
history=model.fit(
        training_set,
        steps_per_epoch=100,
        epochs=2,
        validation_data=test_set,
        validation_steps=800)


from keras.preprocessing import image
test_image = image.load_img('../dataset/single_prediction/cat_or_dog_2.jpg', 
        target_size=(64,64))
test_image = image.img_to_array(test_image)

import numpy as np 
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)


r = training_set.class_indices
print(r)

if result[0][0] == 1.0:
    print('dog')
else:
    print('cat')





