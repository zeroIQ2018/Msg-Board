from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

import datetime
import urllib.request 
import os


def checkifinternet():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.debug = True



if checkifinternet() == True:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://vppilujfsfwfbe:82c4177c3e7c07709fa25801f62506bf1bfc8d42a585d48260c57ef4be64c2f8@ec2-52-211-232-23.eu-west-1.compute.amazonaws.com:5432/d9n2b1qv12ouoo"
elif checkifinternet() == False:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000))
    username = db.Column(db.String(20))
    date_posted = db.Column(db.String(50))
    imageurl = db.Column(db.String(500))


    def __init__(self, username, message, date_posted, imageurl):
        self.message = message
        self.username = username
        self.date_posted = date_posted
        self.imageurl= imageurl
        
  






@app.route("/", methods=['POST', 'GET'])
def index():
    posts = Message.query.all()
    return render_template("index.html", posts=posts)


@app.route("/admin2")
def fakeadmin():
    return render_template("fakeadmin.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")




@app.route("/delete", methods=["POST"])
def delete():
    db.session.query(Message).delete()
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/deleteid", methods=["POST","GET"])
def deleteid():
    data = request.form.get('idform', 0)
    int(data)
    Message.query.filter(Message.id == data).delete()
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/add_message", methods=["POST"])
def add_message():
    message = Message(request.form["Content"], request.form["Username"], datetime.datetime.now(), request.form["imgurl"])
    db.session.add(message)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/options")
def options():
    return render_template("options.html")