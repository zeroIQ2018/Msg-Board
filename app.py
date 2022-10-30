from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


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



@app.route("/add_message", methods=["POST"])
def add_message():
    message = Message(request.form["Content"], request.form["Username"])
    db.session.add(message)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/", methods=['POST', 'GET'])
def index():
    posts = Message.query.all()
    return render_template("index.html", posts=posts)


@app.route("/admin" )
def admin():
    return render_template("admin.html")


@app.route("/delete", methods=["POST"])
def delete():
    db.session.query(Message).delete()
    db.session.commit()
    return redirect(url_for("admin"))

