import os
from flask import render_template, Flask, flash, request, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\flask\microblog'
ALLOWED_EXTENTIONS = {'txt','pdf','png','jpg','gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/')

@app.route('/index')
def index():
    user = {'username': 'Miguel', 'password': 'mypassword'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Microblog', user=user, posts=posts)

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('upload_file.html', title='Last opp ny fil')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

path = 'UPLOAD_FOLDER'
@app.route('/get_files', methods=['GET', 'POST'])
def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            return (os.listdir(path))
    files=[]
    for file in get_files(path):
        files.append(file)
        print(files)      
        
    