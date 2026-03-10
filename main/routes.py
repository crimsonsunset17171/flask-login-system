from flask import render_template, redirect, session
from functools import wraps
from main import main

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

@main.route("/")
@login_required
def index():
    return render_template("index.html", username=session["username"])