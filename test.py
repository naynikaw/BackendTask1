import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = r"C:\Users\nayni\Documents\api_task_flask\uploads"
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp.db'
db = SQLAlchemy(app)

class Details(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))

    def __init__(self, password, age, gender):
        self.password = password
        self.age = age
        self.gender = gender

    def __repr__(self):
        return '<Details %r>' % self.password
    db.create_all()

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

	    def details_init_func(row):
                d = Details(row['username'])
                d.id = row['username']
                return d
        request.save_entry_to_database(
            field_name='file', session=db.session,
            tables=[Details],
            initializers=[details_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return

@app.route("/export", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(db.session, [Details], "xls")

@app.route("/handson_view", methods=['GET'])
def handson_table():
    return excel.make_response_from_tables(
        db.session, [Details], 'handsontable.html')

@app.route('/download')
def download_file():
	url = 'https://codeload.github.com/fogleman/Minecraft/zip/master'
	response = urllib.request.urlopen(url)
	data = response.read()
	response.close()



if __name__ == "__main__":
    app.run(debug=True)
