from flask import Flask, render_template, request, send_from_directory, url_for, flash, redirect
import json
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'STINKY'
app.config["UPLOAD_FOLDER"] = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            filename = '\\uploads\\'+ filename

            print(filename)
            return render_template(CHOICES_TEMP, filename = filename)
    return redirect('/')
        
    
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