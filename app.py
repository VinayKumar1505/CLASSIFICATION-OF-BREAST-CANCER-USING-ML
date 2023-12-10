from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras"""
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# from tensorflow.applications.imagenet_utils import preprocess_input, decode_predictions
# from tensorflow.models import load_model
# from tensorflow.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model_path2 = 'model3.h5' # load .h5 Model

CTS = load_model(model_path2)

from tensorflow.keras.preprocessing.image import load_img, img_to_array

def model_predict2(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(224,224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
    
    
    if result == 0:
        return "BENIGN","after.html"        
    elif result == 1:
        return "MALIGNANT","after.html"
    
    
@app.route("/")
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/predict2',methods=['GET','POST'])
def predict2():
    print("Entered")
    
    print("Entered here")
    file = request.files['files'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
        
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    print("@@ Predicting class......")
    pred, output_page = model_predict2(file_path,CTS)
              
    return render_template(output_page, pred_output = pred, img_src=UPLOAD_FOLDER + file.filename)


   
if __name__ == '__main__':
    app.run(debug=False)