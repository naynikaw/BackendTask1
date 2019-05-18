import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r"C:\Users\nayni\Documents\api_task_flask\uploads"
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/upload')
def upload_form():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File(s) successfully uploaded')
			return redirect('/')

@app.route('/download')
def download_file():
	url = 'https://codeload.github.com/fogleman/Minecraft/zip/master'
	response = urllib.request.urlopen(url)
	data = response.read()
	response.close()

if __name__ == "__main__":
    app.run(debug=True)
