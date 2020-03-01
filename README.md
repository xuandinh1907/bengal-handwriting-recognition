# Documentation of quick tips to build a Flask app

## Project structure
Run this in the project folder
```
mkdir app app/templates app/static app/static/js app/static/css app/blueprints app/middlewares app/models app/static/images app/uploads
touch app/main.py app/templates/base.html app/static/js/index.js app/static/css/style.css
touch app/blueprints/__init__.py
```

Using Canvas or jquery (optional)
```
cp docs/index.js app/static/js/index.js
cp docs/jquery-3.4.1.min.js app/static/js/
cp docs/images/coderschool-logo.png app/static/images/
```

**app/main.py**
VSCode Extension needed: flask-snippets
Start with `fapp`, remove the route

## Create a new blueprint

Run this in the project folder. Change 'home_page' to make a new blueprint
```
export NEW_BLUEPRINT=predict_api
mkdir app/blueprints/$NEW_BLUEPRINT
touch app/blueprints/$NEW_BLUEPRINT/__init__.py app/blueprints/$NEW_BLUEPRINT/blueprint.py
echo "from .$NEW_BLUEPRINT import $NEW_BLUEPRINT" >> app/blueprints/__init__.py
echo "from .blueprint import $NEW_BLUEPRINT" > app/blueprints/$NEW_BLUEPRINT/__init__.py
printf \
"from flask import Blueprint, render_template, request\n\
\n\
$NEW_BLUEPRINT = Blueprint('$NEW_BLUEPRINT', __name__)\
\n\
@$NEW_BLUEPRINT.route('/route_name')\n\
def route_name():\n\
    return render_template('$NEW_BLUEPRINT.html') \n\
" > app/blueprints/$NEW_BLUEPRINT/blueprint.py
cp docs/sample_page.html app/templates/$NEW_BLUEPRINT.html
```

In **app/main.py**:
```
from blueprints import *

app.register_blueprint(home_page)
```

## HTML Template

**app/template/base.html**
Extension: Bootstrap 4, Font awesome 4, Font Awesome 5 Free & Pro snippets
```
b4-$
```
Add javascript and block content to the body
```
<head>
    ...
    <link href="static/css/style.css" rel="stylesheet">
</head>
<body>
    {% block content%} {% endblock %}

    <script src="static/js/jquery-3.4.1.min.js"></script>
    <script src="static/js/index.js"></script>
    <!-- AJAX optional -->
    <script type="text/javascript">
        $("#myButton").click(function(){
            $('#result').text('  Predicting...');
            var $SCRIPT_ROOT = {{request.script_root|tojson|safe}};
            var canvasObj = document.getElementById("canvas");
            var img = canvasObj.toDataURL('image/jpeg');
            $.ajax({
                type: "POST",
                url: $SCRIPT_ROOT + "/upload/",
                data: img,
                success: function(data){
                    $('#result').text('Predictions ' + data);
                }
            });
        });
    </script>
</body>
```


**Bengal Classifier Example**

*home_page.html*
```
<div class="container">
    <br><br>
    <img class="mb-4" src="static/images/coderschool-logo.png" alt="">
    <br><br>
    <div class="row">
        <div class="col-md-6">
            <div id="my-camera"></div>
            <br>
            <form id="form-capture-image">
                <a href="#" class="btn btn-lg btn-primary btn-capture-image">Predict Now</a>
            </form>
        </div>
        <div class="col-md-6">
            <div id="results">
                <div id="loading" class="hidden spinner-border text-warning" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
                <h3 id='class-result'>Predictions:</h3>
                <div id="results-prediction">
                    <p id="prediction"></p>
                </div>
            </div>
        </div>
    </div>
</div>
```

*index.js*
```
CAPTURE_IMG_WIDTH = 640
CAPTURE_IMG_HEIGHT = 480

jQuery.ajaxSetup({
  beforeSend: function() {
     $('#loading').removeClass('hidden');
  },
  complete: function(){
     $('#loading').addClass('hidden');
  },
  success: function() {
    $('#loading').addClass('hidden');
  }
});

// HTML5 WEBCAM
Webcam.set({
  width: CAPTURE_IMG_WIDTH,
  height: CAPTURE_IMG_HEIGHT,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach( '#my-camera' );

let form_capture = document.getElementById('form-capture-image')
$('.btn-capture-image').on('click', function(e) {
  e.preventDefault();

  Webcam.snap(function(data_uri) {
    // display results in page
    // readURL(data_uri, '#input-data-uri')
    let json_data = {'data-uri': data_uri }

    $.ajax({
      type: 'POST',
      url: '/predict/',
      processData: false,
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(json_data),
      success: function(data) {
        console.log(data)
        $('#class-result').text('Predictions: ' + data['root_label']);

        // $('.box-main').css('height', $('.box-results').height());
      }
    });
  });
});
```

*predict_api/blueprint.py*
```
from flask import Blueprint, jsonify, request
import tensorflow as tf
import numpy as np
import re
import os
import base64
import cv2

predict_api = Blueprint('predict', __name__)

model = tf.keras.models.load_model("models/Bengal_classifier.h5")

def preprocess(image):
    image_array = cv2.imread(image,0) / 255
    resized_by_cv_arr = cv2.resize(image_array,(64,64)) 
    final_arr = resized_by_cv_arr.reshape(-1, 64, 64, 1) 
    return final_arr

@predict_api.route('/predict/', methods=['POST'])
def predict():
    data = request.get_json()

    # Preprocess the upload image
    img_raw = data['data-uri']
    final_arr = preprocess(img_raw)

    pred = model.predict(final_arr)
    root_label = np.argmax(pred[0], axis=1)[0]
    vowel_label = np.argmax(pred[1], axis=1)[0]
    consonant_label = np.argmax(pred[2], axis=1)[0]

    return jsonify({'root_label': root_label, 'vowel_label': vowel_label,'consonant_label':consonant_label})
```