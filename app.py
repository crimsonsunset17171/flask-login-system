import sqlite3
from flask import Flask
from extensions import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key_123"

bcrypt.init_app(app)

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 注册 Blueprint
from auth import auth as auth_blueprint
from main import main as main_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)