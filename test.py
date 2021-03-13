from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta
import numpy as np
from keras.preprocessing import image
import tensorflow as tf
from flask import Flask, render_template, request

# Set the allowed file format
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])
ALLOWED_MODEL_EXTENSIONS = set(['h5'])


def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS


def allowed_model_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_MODEL_EXTENSIONS


app = Flask(__name__)
# Set the expiration time of the static file cache
app.send_file_max_age_default = timedelta(seconds=1)


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])  # Add route
def upload():
    if request.method == 'POST':
        basepath = os.path.dirname(__file__)  # The path of the current file

        image_file = request.files['image']
        model_file = request.files['model']

        if request.files['model']:
            if not (allowed_model_file(model_file.filename)):
                return jsonify({"error": 1002,
                                "msg": "Please check the uploaded model type, only .h5"})
            upload_model_path = os.path.join(basepath, 'static/models', secure_filename(model_file.filename))
            model_file.save(upload_model_path)

        if not (image_file and allowed_image_file(image_file.filename)):
            return jsonify({"error": 1001,
                            "msg": "Please upload image and check the uploaded image type, only png、PNG、jpg、JPG、bmp、jpeg"})

        # Otherwise, you will be prompted that there is no such path
        upload_path = os.path.join(basepath, 'static/images', secure_filename(image_file.filename))
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')
        image_file.save(upload_path)

        # Use Opencv to convert the image format and name
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'X-Ray.jpg'), img)

        test_image = image.load_img(upload_path, target_size=[224, 224])
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255
        test_image = np.expand_dims(test_image, axis=0)

        # define the function blocks
        def covid():
            return "covid"

        def normal():
            return "normal"

        def pneumonia():
            return "pneumonia"

        result_sentence = "-----"
        result_sentence1 = "-----"
        result_sentence2 = "-----"
        result_sentence3 = "-----"
        result_sentence4 = "-----"
        result_sentence5 = "-----"
        if request.files['model']:
            model = tf.keras.models.load_model(upload_model_path)
            # tf.keras.experimental.load_from_saved_model
            result = model.predict(test_image)

            # Initialize max with first element of array.
            max = result[0][0]
            max_index = 0

            # Loop through the array
            for i in range(0, len(result[0])):
                # Compare elements of array with max
                if (result[0][i] > max):
                    max = result[0][i]
                    max_index = i
            print(max_index)

            # map the inputs to the function blocks
            options = {0: covid, 1: normal, 2: pneumonia}
            result_name = options[max_index]()
            result_sentence = "Selected Model:" + result_name + "         \n"

        if request.form.get("model-1"):
            model = tf.keras.models.load_model('model/COVID19-XRay-Dataset_model.h5')
            # tf.keras.experimental.load_from_saved_model
            result = model.predict(test_image)

            # Initialize max with first element of array.
            max = result[0][0]
            max_index = 0

            # Loop through the array
            for i in range(0, len(result[0])):
                # Compare elements of array with max
                if (result[0][i] > max):
                    max = result[0][i]
                    max_index = i
            print(max_index)

            # map the inputs to the function blocks
            options = {0: covid, 1: normal, 2: pneumonia}
            result_name = options[max_index]()
            result_sentence1 = "Model 1:" + result_name + "         \n"

        if request.form.get("model-2"):
            model = tf.keras.models.load_model('model/COVID-19 Radiography Database.h5')
            result = model.predict(test_image)

            max = result[0][0]
            max_index = 0

            for i in range(0, len(result[0])):
                if (result[0][i] > max):
                    max = result[0][i]
                    max_index = i
            print(max_index)

            options = {0: covid, 1: normal, 2: pneumonia}
            result_name = options[max_index]()
            result_sentence2 = "Model 2:" + result_name + "         \n"

        if request.form.get("model-3"):
            model = tf.keras.models.load_model('model/N-CLAHE-MEDICAL-IMAGES.h5')
            result = model.predict(test_image)

            max = result[0][0]
            max_index = 0

            for i in range(0, len(result[0])):
                if (result[0][i] > max):
                    max = result[0][i]
                    max_index = i
            print(max_index)

            options = {0: covid, 1: normal, 2: pneumonia}
            result_name = options[max_index]()
            result_sentence3 = "Model 3:" + result_name + "         \n"

        if request.form.get("model-4"):
            model = tf.keras.models.load_model('model/COVID-19 X rays + Chest X-Ray Images (Pneumonia).h5')
            result = model.predict(test_image)

            max = result[0][0]
            max_index = 0

            for i in range(0, len(result[0])):
                if (result[0][i] > max):
                    max = result[0][i]
                    max_index = i
            print(max_index)

            options = {0: covid, 1: normal, 2: pneumonia}
            result_name = options[max_index]()
            result_sentence4 = "Model 4:" + result_name + "         \n"

        if request.form.get("model-5"):
            model = tf.keras.models.load_model('model/Combo Dataset.h5')
            result = model.predict(test_image)

            max = result[0][0]
            max_index = 0

            for i in range(0, len(result[0])):
                if (result[0][i] > max):
                    max = result[0][i]
                    max_index = i
            print(max_index)

            options = {0: covid, 1: normal, 2: pneumonia}
            result_name = options[max_index]()
            result_sentence5 = "Model 5:" + result_name + "         \n"

        if (request.form.get("model-1") or request.form.get("model-2")) or ((request.form.get("model-3")
                or request.form.get("model-4")) or (request.form.get("model-5") or request.files['model'])):
            null = ""
        else:
            return jsonify({"error": 1003, "msg": "Please check the model"})

        return render_template('detector2.html', result1=result_sentence1, result2=result_sentence2,
                               result3=result_sentence3, result4=result_sentence4, result5=result_sentence5,
                               result=result_sentence, val1=time.time())

    return render_template('detector.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
