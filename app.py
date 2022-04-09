from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from facerecognition import FaceRecognition
app = Flask(__name__)

facerecognition = FaceRecognition()

def gen(camera):
    while True:
        #get camera frame
        frame = camera.start()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(FaceRecognition()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')