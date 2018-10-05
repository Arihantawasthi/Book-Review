import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

# Registration of users
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check whether the user has provided username and password
        if username and password:
            usernames = db.execute("SELECT username FROM users")

            # Checking whether username already exists or not
            for user in usernames:
                if user.username == username:
                    return "Username Already Exists, please enter a different username"

            users = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
            db.commit()
            return "You are registered"

        else:
            return render_template("error.html")
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("log_username")
        password = request.form.get("log_password")

        users = db.execute("SELECT username, password FROM users")
        for user in users:
            if user.username == username and user.password == password:
                return render_template("welcome.html")

        return "username or password in correct"

    return render_template("login.html")
