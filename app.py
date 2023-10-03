from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import urllib.request 
from flask_bcrypt import Bcrypt, check_password_hash



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
app.config["SECRET_KEY"] = "FLASKMSGBOARD"


if os.getenv('DATABASE_URL') is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000))
    username = db.Column(db.String(200))
    date_posted = db.Column(db.String(50))
    imageurl = db.Column(db.String(5000))


    def __init__(self, username, message, date_posted, imageurl):
        self.message = message
        self.username = username
        self.date_posted = date_posted
        self.imageurl = imageurl


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(2000), nullable=False, unique = True)
    password = db.Column(db.String(2000), nullable=False)
    accountcreated = db.Column(db.String(50))
    def __init__(self, username, password, accountcreated):
        self.username = username
        self.password = password
        self.accountcreated = accountcreated











#MAIN ADDING MESSAGES AND OTHER STUFF

@app.route("/", methods=["POST", "GET"])
def board():
    posts = Message.query.all()
    if "username" not in session:
        return render_template("board.html", posts=posts, curuser="Not logged in")

    if request.method == 'POST' and "username" in session:
        message = Message(session['username'] , request.form["Username"], datetime.datetime.now(), request.form["imgurl"])
        db.session.add(message)
        db.session.commit()
    if "username" in session:
        return render_template("board.html", posts=posts, curuser=session['username'])


@app.route("/options" ,methods=["GET", "POST"])
def options():
    return render_template("options.html")




#LOGIN AND SIGNUP STUFF
@app.route("/signup", methods=["GET", "POST"])
def signup():
    test = User.query.all()
    if request.method == 'POST':
        new_user = User(request.form["RegUsername"] , bcrypt.generate_password_hash(request.form["RegPassword"]).decode("utf-8"), datetime.datetime.now() )
        if request.form["RegUsername"] in test:
            return redirect(url_for("usernamealreadyexists"))
        else:
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', )


@app.route("/login" , methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form["LogUsername"]).one()
        print(request.form["LogUsername"])
        print(u.password)
        if bool(User.query.filter_by(username=request.form["LogUsername"]).first()) == True and bool(check_password_hash(u.password, request.form["LogPassword"]) ) == True:
            session['username'] = request.form['LogUsername']
            
            # will do later
            return redirect(url_for('board'))
        else:
            return redirect(url_for('login'))






    return render_template("login.html")





@app.route('/logout', methods=['GET', 'POST'])
#only available if login do later fr fr
def logout():
    if "username" in session:
        session.pop("username", None)
    return redirect(url_for('board'))


#ERROR HANDELING

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def intserverror(error):
    return render_template('500.html'), 500


@app.route("/usernamealreadyexists")
def usernamealreadyexists():
    return render_template("error.html")



if __name__ == "__main__":
    app.run(debug=True)