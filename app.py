import os
from os.path import join, dirname, realpath
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import random
import string
from PIL import Image
import PIL.ImageOps

import run

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'temp_data/temp_images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET"])
def index():
    return 'INDEX'

@app.route('/upload_image',  methods=["POST"])
def upload_image():
    print("start")
    image = request.files['imagefile'] # getting image file from POST request
    # check to make sure its an actual image
    filename = secure_filename(randomString(8) + '.jpg') # assigning secure filename ('never trust user input')
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # save image to UPLOAD_FOLDER path
    
    # run model
    run.run_prediction([app.config['UPLOAD_FOLDER'] + "/" + filename])

    filename_png = filename[:-3] + 'png' # basnet outputs files as png, but image input is jpg so we're just replacing the extension here

    # invert image
    pre_inverted_image = Image.open("temp_data/temp_results/" + filename_png)
    inverted_image = PIL.ImageOps.invert(pre_inverted_image)

    # save inverted image
    inverted_image.save('temp_data/temp_results/' + filename[:-3] + "_inverted.png")

    return send_file('temp_data/temp_results/' + filename[:-3] + "_inverted.png", mimetype='image/gif') # return image

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == '__main__':
    app.run(debug=True)
