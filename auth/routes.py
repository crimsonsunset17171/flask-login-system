from flask import render_template, request, redirect, session, flash
from extensions import bcrypt
from auth import auth
import sqlite3


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("注册成功，请登录！", "success")
            return redirect("/login")
        except:
            flash("用户名已存在！", "error")
            return redirect("/register")
        finally:
            conn.close()
    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user["password"], password):
            session["username"] = username
            return redirect("/")
        flash("用户名或密码错误！", "error")
        return redirect("/login")
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

@auth.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (session["username"],)).fetchone()
        if not bcrypt.check_password_hash(user["password"], old_password):
            flash("原密码错误！", "error")
            return redirect("/change_password")
        if new_password != confirm_password:
            flash("两次输入的新密码不一致！", "error")
            return redirect("/change_password")
        new_hashed = bcrypt.generate_password_hash(new_password).decode("utf-8")
        conn.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed, session["username"]))
        conn.commit()
        conn.close()
        flash("密码修改成功！", "success")
        return redirect("/")
    return render_template("change_password.html")