import tensorflow as tf # type: ignore
import numpy as np # type: ignore
import cv2 # type: ignore
import os
from werkzeug.utils import secure_filename # type: ignore

# Load your trained model
model = tf.keras.models.load_model('projects/model_controllers/catdog/vgg16_cats_vs_dogs.h5')

# Define your upload folder
UPLOAD_FOLDER = 'projects/static/images'

# Function to process images (resize, preprocess, etc.)
def process_image(image):
    image = cv2.resize(image, (256, 256))  # Resize image as required
    image = tf.cast(image, tf.float32) / 255.0  # Normalize image
    return np.expand_dims(image, axis=0)  # Add batch dimension

# Function to get prediction label
def get_prediction_label(prediction_prob):
    if prediction_prob >= 0.5:
        return "dog"
    else:
        return "cat"

# Function to handle image upload
def upload_image(file):
    if file:
        filename = secure_filename(file.filename)
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(img_path)
        return filename  # Return filename if upload is successful
    return None  # Return None if no file or other error

# Function to predict on uploaded image
def predict_image(filename):
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(img_path)
    img_input = process_image(img)
    prediction = model.predict(img_input)[0][0]  # Get scalar prediction value
    prediction_label = get_prediction_label(prediction)
    return prediction_label  # Return prediction label

