from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class students(db.Model):
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    regNo = db.Column(db.String(100), primary_key=True)
    mobNo = db.Column(db.String(10))
    email = db.Column(db.String(100))
    gender = db.Column(db.String(10))


def __init__(self, firstName, lastName, regNo, mobNo, email, gender):
    self.firstName = firstName
    self.lastName = lastName
    self.regNo = regNo
    self.mobNo = mobNo
    self.email = email
    self.gender = gender

def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = "6Lc3F6sUAAAAALvoG1cKxkgU0ffUIkbpAamIzezJ"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['firstName'] or not request.form['lastName'] or not request.form['mobNo'] or not \
        request.form['email'] or not request.form['gender']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['firstName'], request.form['lastName'], request.form['regNo'],
                               request.form['mobNo'], request.form['email'], request.form['gender'])
            captcha_response = request.form['g-recaptcha-response']

            db.session.add(student)
            db.session.commit()

            if is_human(captcha_response):
                # Process request here
                status = "Detail submitted successfully."
            else:
                # Log invalid attempts
                status = "Sorry ! Bots are not allowed."

            flash(status)


            #flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
