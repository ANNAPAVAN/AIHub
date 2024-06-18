import numpy as np
import cv2 # type: ignore
import tensorflow as tf # type: ignore
import os


# Load your trained model
model = tf.keras.models.load_model('projects/model_controllers/mask/vgg16_mask_detector.h5')

UPLOAD_FOLDER = 'projects/static/images'

def mask_predict(filename):

    img_path = os.path.join(UPLOAD_FOLDER, filename)

    # Load the image using OpenCV
    img = cv2.imread(img_path)
    
    # Resize the image to (224, 224)
    img = cv2.resize(img, (224, 224))
    
    # Convert to numpy array and normalize
    img_array = np.array(img)
    img_array = img_array / 255.0
    
    # Expand dimensions to create a batch of size 1
    img_batch = np.expand_dims(img_array, axis=0)
    
    # Make prediction
    y_pred = model.predict(img_batch)
    
    # Threshold predictions
    predictions = (y_pred >= 0.5).astype(int)
    
    # Convert predictions to 'mask' or 'nomask'
    result = 'nomask' if predictions[0][0] == 1 else 'mask'
    
    return result