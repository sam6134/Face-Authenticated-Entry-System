import xlsxwriter as xlsxwriter
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, flash, request, send_file
from camera import camera_stream, person_name
from form import LoginForm
from datetime import datetime


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SECRET_KEY'] = '21a00ee024ebe902cf1848208f5c1a29'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Entry(db.Model):
    __searchable__ =['name']

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20),nullable=False)
    date_posted = db.Column(db.DateTime, nullable= False, default = datetime.now)
    def __repr__(self):
        return f"User('{self.name}')"



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('home.html')


@app.route('/detect')
def detect():
    return render_template('index.html')


@app.route('/welcome')
def welcome():
    name = person_name()
    if(name=="Unknown"):
        return render_template('welcome1.html')
    entry1 = Entry(name = name)
    db.session.add(entry1)
    db.session.commit()
    return render_template('welcome.html', name=name)

@app.route('/search')
def search():
    posts = Entry.query.filter_by(name=(request.args.get("query")).lower()).all()
    return render_template('query.html',posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@cavity.com" and form.password.data == "1234":
            posts = Entry.query.all()
            return render_template("query.html", posts=posts)
        else:
            flash("Login unsuccessful. Check email/password", 'danger')
    return render_template("login.html", title="Login", form=form)


def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/download', methods=['GET'])
def export_db():
    values = Entry.query.all()

    wb = xlsxwriter.Workbook('static/attendance.xlsx')
    ws = wb.add_worksheet()

    ws.write(0, 0, "Name")
    ws.write(0, 1, "Date")
    ws.write(0, 2, 'Time')

    row = 1
    for item in values:
        ws.write(row, 0, item.name)
        ws.write(row, 1, item.date_posted.strftime('%d %b'))
        ws.write(row, 2, item.date_posted.strftime('%-I:%M %p'))
        row += 1
    wb.close()

    return send_file('static/attendance.xlsx')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
