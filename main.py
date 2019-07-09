# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from smile_score_calculator import SmileScoreCalculator
from google.cloud import storage
from google.cloud.storage import Blob

client = storage.Client(project="smile-score")
BUCKET = client.get_bucket("smiles-in-cloud")


UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST', 'PUT'])
def upload_file():
    app.logger.info('Upload_file')
    app.logger.info(request.method)
    
    if request.method == 'POST':
        app.logger.info('POST')
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.info('file problem')
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print('allowed_file')
            app.logger.info('ddddddd')
            filename = secure_filename(file.filename)
            blob = Blob(filename, BUCKET)    
            blob.upload_from_file(file)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Smile Score Calculator</title>
    <h1>Upload image</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    uploaded_image_URI = "https://storage.googleapis.com/smiles-in-cloud/%s" % filename
    app.logger.info(uploaded_image_URI)

    ssc = SmileScoreCalculator(uploaded_image_URI)
    ssc.request_vision_api()
    caption = ssc.calculate_smile()

    return '''<!DOCTYPE html>
    <html>
    <body>
        <p>
        %s
        <img border="0" alt="uploaded image" src=%s width="100" height="150">
        </a>
        </p>
    </body>
    </html>
''' % (caption, uploaded_image_URI)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
