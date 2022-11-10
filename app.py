from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.debug = False
db = SQLAlchemy(app)





class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50))
    username = db.Column(db.String(50))
    date_posted = db.Column(db.String(50))
    imageurl = db.Column(db.String(50))


    def __init__(self, username, message, date_posted, imageurl):
        self.message = message
        self.username = username
        self.date_posted = date_posted
        self.imageurl= imageurl




@app.route("/add_message", methods=["POST"])
def add_message():
    message = Message(request.form["Content"], request.form["Username"], datetime.datetime.now(), request.form["imgurl"])
    db.session.add(message)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/", methods=['POST', 'GET'])
def index():
    posts = Message.query.all()
    return render_template("index.html", posts=posts)


@app.route("/admin2" )
def admin():
    return render_template("admin.html")


@app.route("/admin")
def fakeadmin():
    return render_template("fakeadmin.html")


@app.route("/delete", methods=["POST"])
def delete():
    db.session.query(Message).delete()
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/deleteid", methods=["POST"])
def deleteid():
    id = request.form["id"]
    row_to_delete = db.session.query(Message).filter(Message.id==id).one()
    db.session.query(row_to_delete).delete()
    return redirect(url_for("admin"))