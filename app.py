from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime




app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://vppilujfsfwfbe:82c4177c3e7c07709fa25801f62506bf1bfc8d42a585d48260c57ef4be64c2f8@ec2-52-211-232-23.eu-west-1.compute.amazonaws.com:5432/d9n2b1qv12ouoo"
app.debug = False
db = SQLAlchemy(app)





class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300))
    username = db.Column(db.String(300))
    date_posted = db.Column(db.String(300))
    imageurl = db.Column(db.String(300))


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


@app.route("/admin2", methods=["GET", "POST"])
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


@app.route("/deleteid", methods=["POST","GET"])
def deleteid():
    data = request.form.get('idform', 0)
    coloumn = Message.query.filter_by(id=data).one()
    print(coloumn)
    db.session.query(coloumn).delete()
    db.session.commit()
    return redirect(url_for("admin"))