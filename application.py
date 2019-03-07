import os
import secret
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


engine = create_engine(secret.user_database_url)
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'secret.secret_key'
login = LoginManager(app)


bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search_page", methods=["POST"])
def search_page():
    email = request.form.get("login_email")
    check_email_in_db = db.execute(
        "SELECT COUNT(*) FROM users WHERE email = :email", {"email": email}).fetchall()
    if check_email_in_db[0][0] == 1:
        email = request.form.get("login_email")
        password = request.form.get("login_password")
        retrive_password_from_db = db.execute(
            "SELECT password FROM users WHERE email = :email", {"email": email}).fetchall()
        retrive_password_from_db = retrive_password_from_db[0][0]
        if bcrypt.check_password_hash(retrive_password_from_db, password):
            return render_template("search_page.html")
        else:
            flash('Invalid Password; Please try again')
            return redirect(url_for('index'))
    else:
        flash('You are not a registered User. Request you to sign-up first')
        return redirect(url_for('index'))


@app.route("/search_result")
def search_result():
    return render_template("search_result.html")


@app.route("/hello", methods=["POST", "GET"])
def hello():
    email = request.form.get("email")
    check_email_in_db = db.execute(
        "SELECT COUNT(*) FROM users WHERE email = :email", {"email": email}).fetchall()
    if check_email_in_db[0][0] == 1:
        return("Sorry, this username has already been taken, please revisit the home page and try with a new email address")
    else:
        password = request.form.get("password")
        password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {
                   "email": email, "password": password})
        db.commit()
        return("Thank you for sigining up")

  
    

if __name__ == '__main__':
    app.run()
