from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from werkzeug.utils import secure_filename
from facerecognition import FaceRecognition
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'static/upload/'
facerecognition = FaceRecognition()
app.secret_key = 'godisbitch'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/home')
def index():
    return render_template('index.html')
@app.route('/')
def default():
    return redirect('/home')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash("No File Found")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == "":
        flash("No Image Selected for uploading")
        return redirect(request.url)
    if file and allowed_filename(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        attendance = facerecognition.start(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', attendance=attendance)
    else:
        flash('not Valid Image File')
        return redirect(request.url)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')