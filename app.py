from email import message
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.debug = True
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50))
    username = db.Column(db.String(50))

    def __init__(self, username, message):
        self.message = message
        self.username = username

    def __repr__(self):
        return "<Message %r>" % self.username




@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/add_message", methods=["POST"])
def add_message():
    message = Message(request.form["Content"], request.form["Username"])
    db.session.add(message)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()