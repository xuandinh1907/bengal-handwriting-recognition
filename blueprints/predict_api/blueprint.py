from flask import Blueprint, jsonify, request
import tensorflow as tf
import numpy as np
import re
import os
import base64
import uuid
import pandas as pd

predict_api = Blueprint('predict', __name__)

model = tf.keras.models.load_model("models/Bengal_classifier.h5")
class_map = pd.read_csv('static/csv/class_map.csv')

def parse_image(imgData):

    # ImgData look like this
    # b'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMC
    # using re.search help us get like this b'/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMC . . .
    img_str = re.search(b"base64,(.*)", imgData).group(1)

    # Image after decode bytes look like this
    # b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\ . . .
    img_decode = base64.decodebytes(img_str)

    filename = "{}.jpg".format(uuid.uuid4().hex)
    with open('uploads/'+filename, "wb") as f:
        f.write(img_decode)
    
    return img_decode

def preprocess(image):

    # From b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\ . . .
    # We continue decode by decode_jpeg to get a tensor (includung numpy value)
    image = tf.image.decode_jpeg(image, channels=1)

    image = tf.image.resize(image, [64, 64])
    
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    image = tf.image.convert_image_dtype(image, tf.float32) / 255

    # Our training phase there is no normalization in range [-1,1] and
    # aslo no standardization so we exclude these 2 preprocessing methods
    # I have aslo dicovered that resize by OpenCV or Tensorflow  makes really small gap
    # So we use tensorflow because of convenience for reading image

    # image = (image*2) - 1  # normalize to [-1,1] range
    # image = tf.image.per_image_standardization(image)
    return image

@predict_api.route('/predict/', methods=['POST'])
def predict():
    data = request.get_json() # data form is a dictionary
    img_raw = data['data-uri'].encode()
    image = parse_image(img_raw)
    image = preprocess(image)
    image = tf.expand_dims(image, 0)

    pred = model.predict(image)
    root_label = np.argmax(pred[0], axis=1)[0]
    vowel_label = np.argmax(pred[1], axis=1)[0]
    consonant_label = np.argmax(pred[2], axis=1)[0]

    root_symbol = class_map[(class_map['component_type']=='grapheme_root') & 
                        (class_map['label']==root_label)]['component'].values[0]

    vowel_symbol = class_map[(class_map['component_type']=='vowel_diacritic') & 
                         (class_map['label']==vowel_label)]['component'].values[0]
    
    consonant_symbol = class_map[(class_map['component_type']=='consonant_diacritic') & 
                       (class_map['label']==consonant_label)]['component'].values[0]

    return jsonify({'root': str(root_symbol) , 'vowel': str(vowel_symbol) ,'consonant':str(consonant_symbol)})