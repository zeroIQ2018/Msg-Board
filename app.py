from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import datetime
import os
import urllib.request 
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

def checkifinternet():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.debug = True
app.config["DEBUG_MODE"] = True
app.config["SECRET_KEY"] = "Pringelsandcoke"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if checkifinternet() == True:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jhicjctonxlntk:1a28ed11d506db1432241de6ccae0c4aa53e6d8a6f8f34d98ebf5e8e04520acc@ec2-52-212-228-71.eu-west-1.compute.amazonaws.com:5432/d2tu9lis57lehf"
elif checkifinternet() == False:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000))
    username = db.Column(db.String(20))
    date_posted = db.Column(db.String(50))
    imageurl = db.Column(db.String(5000))


    def __init__(self, username, message, date_posted, imageurl):
        self.message = message
        self.username = username
        self.date_posted = date_posted
        self.imageurl = imageurl


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(2000), nullable=False, unique = True)
    password = db.Column(db.String(2000), nullable=False)




class Signinform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')


class Loginform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')





#MAIN ADDING MESSAGES AND OTHER STUFF
@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("home.html")

@app.route("/board", methods=["POST", "GET"])
def board():
    posts = Message.query.all()
    return render_template("board.html", posts=posts)

@app.route("/add_message", methods=["GET", "POST"])
@login_required
def add_message():
    message = Message(current_user.username , request.form["Username"], datetime.datetime.now(), request.form["imgurl"])
    db.session.add(message)
    db.session.commit()
    return redirect(url_for("board"))

@app.route("/options" ,methods=["GET", "POST"])
def options():
    return render_template("options.html")





#LOGIN AND SIGNUP STUFF
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = Signinform()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8") 
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('signup.html', form=form)

@app.route("/login" , methods=["GET", "POST"])
def login():
    form = Loginform()


    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('board'))


    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





#ADMIN STUFF
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    user = User.query.filter_by(username="admin0909").first()
    if current_user.username == "admin0909" and bcrypt.check_password_hash(user.password, "admin0909"):
        return render_template("admin.html")
    else:
        return redirect(url_for("board"))

@app.route("/delete", methods=["GET", "POST"])
def delete():
    user = User.query.filter_by(username="admin0909").first()
    if current_user.username == "admin0909" and bcrypt.check_password_hash(user.password, "admin0909"):
            db.session.query(Message).delete()
            db.session.commit()
            return redirect(url_for("board"))
    else:
        return redirect(url_for("board"))





@app.route("/deleteid", methods=["POST","GET"])
def deleteid():
    user = User.query.filter_by(username="admin0909").first()
    if current_user.username == "admin0909" and bcrypt.check_password_hash(user.password, "admin0909"):
        data = request.form.get('idform', 0)
        int(data)
        Message.query.filter(Message.id == data).delete()
        db.session.commit()
        return redirect(url_for("board"))
    else:
        return redirect(url_for("board"))


@app.route("/deleteaccount", methods=["POST","GET"])
def deleteaccount():
    user = User.query.filter_by(username="admin0909").first()
    if current_user.username == "admin0909" and bcrypt.check_password_hash(user.password, "admin0909"):
            account = request.form.get("accountid",0)
            int(account)
            User.query.filter(User.id == account).delete()
            db.session.commit()
            return redirect(url_for("board"))
    else:
        return redirect(url_for("board"))


if __name__ == "__main__":
    app.run(debug=True)