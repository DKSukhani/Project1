import os

from flask import Flask, render_template, request

from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    "postgres://sqlxamuciiofie:86b317ef4be1dc74d800442ecdfe1447933e12298c36a5333d6a3fdfddc27b9d@ec2-54-83-50-174.compute-1.amazonaws.com:5432/d33ltdp29n43i3")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST", "GET"])
def hello():
    email = request.form.get("email")
    password = request.form.get("password")
    db.execute("INSERT INTO users (email, password) VALUES (:email, :password)",
            {"email": email, "password": password})
    
    
    # ("INSERT INTO users (email, password) VALUES (:email, crypt(':password', gen_salt('bf'))", {"email": email, "password": password})




    db.commit()
    data = db.execute(
         "SELECT email FROM users").fetchall()
    data = str(data)
    return(data)
    
    
if __name__ == '__main__':
    app.run()

