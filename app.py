from flask import Flask, render_template, request, send_from_directory, flash, redirect
import json
from werkzeug.utils import secure_filename
import os
from yolov5.detect import run
import shutil
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'STINKY'
app.config["UPLOAD_FOLDER"] = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
YAMLPATH = r'D:\UNi\UTS\DEEPLEARN\DeepLearnWebsite\modelYaml.yaml'
PTPATH = r'D:\UNi\UTS\DEEPLEARN\DeepLearnWebsite\best.pt'

WEBSITE_TEMP = "website.html"
CHOICES_TEMP = "choices.html"

def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def start_website():
    return render_template(CHOICES_TEMP, filename = None)

@app.route("/", methods=["POST"])
def save_photo():
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
            
            saveDir = run(PTPATH, source=filename, data=YAMLPATH)
            shutil.move(os.path.join(saveDir, secure_filename(file.filename)), filename)
            filename = '\\uploads\\'+ secure_filename(file.filename)

            return render_template(CHOICES_TEMP, filename = filename)
    return redirect('/')
        

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

        saveDir = run(PTPATH, source=file_path, data=YAMLPATH)
        shutil.move(os.path.join(saveDir, filename), file_path)
        filename = os.path.join('uploads', filename)

        return str(filename)
    else:
        return "No photo uploaded"

@app.route('/video-stream')
def video_stream():
    return render_template(WEBSITE_TEMP)

@app.route('/print-screen', methods=['POST'])
def print_to_screen():
    data = json.loads(request.form.get('data'))

    print(data)
    return 'success'

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(os.getcwd()+ '\\uploads\\',filename)