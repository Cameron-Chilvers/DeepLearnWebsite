import subprocess
import cv2
from flask import Flask, Response, render_template, request, send_from_directory, flash, redirect
import json
from werkzeug.utils import secure_filename
import os
from yolov5.detect import run
import shutil
import time
#@from camera import VideoCamera

app = Flask(__name__)
app.config['SECRET_KEY'] = 'STINKY'
app.config["UPLOAD_FOLDER"] = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
YAMLPATH = os.path.join(os.getcwd(),'modelYaml.yaml')
PTPATH = os.path.join(os.getcwd(),'model.pt')

HOME_TEMP = "home.html"
PHOTO_TEMP = "photo.html"
UPLOAD_TEMP = "upload.html"
VIDEO_TEMP = "video.html"

def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def start_website():
    return render_template(HOME_TEMP)

@app.route("/upload-photo")
def upload_photo():
    return render_template(UPLOAD_TEMP, filename = None)

@app.route("/upload-photo", methods=["POST"])
def save_uploaded_photo():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], filename)
            
            saveDir = run(PTPATH, source=filename, data=YAMLPATH, line_thickness=1)
            shutil.move(os.path.join(saveDir, secure_filename(file.filename)), filename)
            filename = '\\uploads\\'+ secure_filename(file.filename)

            return render_template(UPLOAD_TEMP, filename = filename)
    return redirect('/upload-photo')
        

@app.route("/save-photo", methods=['POST'])
def save_taken_photo():
    photo_file = request.files.get('photo')

    if photo_file is not None:
        counter = 0
        while os.path.isfile(os.path.join(os.getcwd(), 'uploads', 'photo_{}.png'.format(counter))):
            counter += 1
        
        filename = 'photo_{}.png'.format(counter)
        file_path = os.path.join(os.getcwd(), 'uploads', filename)

        photo_file.save(file_path)

        saveDir = run(PTPATH, source=file_path, data=YAMLPATH, line_thickness=2)
        shutil.move(os.path.join(saveDir, filename), file_path)
        filename = os.path.join('uploads', filename)

        return str(filename)
    else:
        return "No photo uploaded"

@app.route('/take-photo')
def take_photo():
    return render_template(PHOTO_TEMP)

@app.route('/video-stream')
def video_stream():
    return render_template(VIDEO_TEMP)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/print-screen', methods=['POST'])
def print_to_screen():
    data = json.loads(request.form.get('data'))

    print(data)
    return 'success'

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(os.getcwd()+ '\\uploads\\',filename)