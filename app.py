from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug import secure_filename
import os
import jwt
import datetime
from pymongo import MongoClient
from functools import wraps
from pymongo import MongoClient
import bcrypt

salt = bcrypt.gensalt(10)
client = MongoClient(
    "mongodb+srv://rahulbera21:rahul123@cluster0-9qlne.mongodb.net/test?retryWrites=true&w=majority"
)
db = client.flask_jwt_api_file_upload
users = db.users


app = Flask(__name__)
app.config["SECRET_KEY"] = "!@#$%^&*"

UPLOAD_FOLDER = "images/"
ALLOWED_EXTENSIONS = set(["jpeg", "png", "jpg"])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

limiter = Limiter(app, key_func=get_remote_address)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session["token"]

        if not token:
            return render_template("sucess.html", message="Token Missing")
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])

        except:
            return render_template("sucess.html", message="Token Expired")

        return f(*args, **kwargs)

    return decorated


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email})

        if user:
            return render_template("register.html", message="Email already Registered")

        else:
            password_hash = bcrypt.hashpw(password.encode("UTF-8"), salt)
            user = {"email": email, "password": password_hash}

            users.insert_one(user)

            return render_template("register.html", message="Registration Completed")

    return render_template("register.html")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=["GET", "POST"])
@limiter.limit("5 per minute")
@token_required
def upload():
    if request.method == "POST":
        file = request.files["file"]
        file.save(
            os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        )
        return render_template("sucess.html", message=file.filename)


@app.route("/token")
def token():
    return session["token"]


@app.route("/getauthtoken", methods=["GET", "POST"])
def getauthtoken():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode("UTF-8"), user["password"]):
            token = jwt.encode(
                {
                    "user": user["email"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
                },
                app.config["SECRET_KEY"],
            )
            session["token"] = token
            return render_template("token.html", token=token)
        else:
            return render_template("token.html", token="Invalid Credentials")

    return render_template("token.html")


if __name__ == "__main__":
    app.run(debug=False)
