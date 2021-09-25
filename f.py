import os
from flask import Flask, flash, request, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'dataset/cat2dog/testB/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
            os.system("python3 main.py --dataset cat2dog --light True --phase test --smoothing False && "
                      "mv results/*/*.jpg static/cat.jpg && mv dataset/cat2dog/testB/* static/dog.jpg; "
                      "rm dataset/cat2dog/testB/*")
            return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <html><head><title>Test task #1</title></head><body>
    <h1>Upload, dog</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>''' + ('''<hr /><img src='static/dog.jpg'  width='256' height='256' />
    <img alt='The cat will be here.' src='static/cat.jpg'  width='256' height='256' />
    </body></html>
    ''' if os.path.isfile('static/cat.jpg') and os.path.isfile('static/dog.jpg') else '</body></html>')
