from flask import Flask, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from celery_worker import task1
import os
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'mp4', 'flv', 'avi', 'm4v', 'jpg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/')
# def hello_world():  # put application's code here
#     task_obj = task1.apply_async(args=[str(uuid.uuid4())])
#     return str(task_obj)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route('/convert', methods=['GET', 'POST'])
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
            id = task1.apply_async(args=[filename])
            return f'start convert file with id {id}'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



if __name__ == '__main__':
    app.run()
