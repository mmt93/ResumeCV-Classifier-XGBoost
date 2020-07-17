from flask import Flask
from main import transform_file
from evaluate_resume import points_results

import os
import urllib.request

from werkzeug.utils import secure_filename
from predict_model import prepare_file
from flask_socketio import SocketIO,emit
from time import sleep
from threading import Thread, Event

from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/api'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

doc_type = set(['txt', 'pdf', 'doc', 'docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in doc_type

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file_class = prepare_file(filename)
			final_points, final_req = points_results(filename, file_class)
			flash(('We have seen you are looking for {} job positions.<br>Your resume has covered {:.2f}%'.format(file_class.upper(),final_points)))
			flash(final_req)
			return redirect('/')
		else:
			return redirect(request.url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
