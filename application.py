import os
import secret

from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



engine = create_engine(secret.database_url)
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.static_folder = 'static'
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST", "GET"])
def hello():
    email = request.form.get("email")
    password = request.form.get("password")
    password = bcrypt.generate_password_hash(password)
    db.execute("INSERT INTO users (email, password) VALUES (:email, :password)",
            {"email": email, "password": password})
    
    db.commit()
    data = db.execute(
         "SELECT password FROM users").fetchall()
    data = str(data)
    return(data)
    
    
if __name__ == '__main__':
    app.run()

