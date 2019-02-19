import os
import secret

from flask import Flask, render_template, request

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
    print("password without the decode is "+ password)
    password = bcrypt.generate_password_hash(password,10).decode('utf-8')
    db.execute("INSERT INTO users (email, password) VALUES (:email, :password)",
            {"email": email, "password": password})
    
    db.commit()
    data = db.execute(
         "SELECT email FROM users").fetchall()
    data = str(data)
    return(data)

@app.route("/check", methods=["POST", "GET"])
def check():
        email = request.form.get("login_email")
        check_email_in_db = db.execute("SELECT COUNT(*) FROM users WHERE email = :email", {"email": email}).fetchall()
        if check_email_in_db[0][0] == 1 :
            email = request.form.get("login_email")
            password = request.form.get("login_password")
            retrive_password_from_db = db.execute("SELECT password FROM users WHERE email = :email", {"email": email}).fetchall()
            retrive_password_from_db = retrive_password_from_db[0][0]
            if bcrypt.check_password_hash(retrive_password_from_db, password):
                return("this works")
            else:
                return("something is wrong")
        
            
            # if abc == password:
            #    return("all is good")
            # else:
            #     return ("Sorry you have entered an incorrect password")
            # rs = db.execute("SELECT password FROM users WHERE email = :email" , {"email": email, "password": password}).fetchall()
            # if rs[0][0] == 1 :
            #     return ("Thank you for logging-in")
            # else:
            #     
        
        else:
            return ("Sorry, you are not a registered user")
    
    
if __name__ == '__main__':
    app.run()

