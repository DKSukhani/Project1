import os
import secret
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


engine = create_engine(secret.user_database_url)
engine2 = create_engine(secret.books_database_url)
db = scoped_session(sessionmaker(bind=engine))
db2 = scoped_session(sessionmaker(bind=engine2))

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'secret.secret_key'
login = LoginManager(app)


bcrypt = Bcrypt(app)
user_signed_in = 0

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search_page", methods=["POST", "GET"])
def search_pg():
    return render_template("search_page.html")
    # global user_signed_in
    # if 'sign-up_form' in request.form:
    #     email = request.form.get("email")
    #     check_email_in_db = db.execute(
    #         "SELECT COUNT(*) FROM users WHERE email = :email", {"email": email}).fetchall()
    #     if check_email_in_db[0][0] == 1:
    #         flash("Sorry, this username has already been taken, please revisit the home page and try with a new email address")
    #         return redirect(url_for('index'))
    #     else:
    #         password = request.form.get("password")
    #         password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
    #         db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {
    #                 "email": email, "password": password})
    #         db.commit()
    #         user_signed_in = 1
    #         return render_template("search_page.html")
    # elif 'login_form' in request.form:
    #     email = request.form.get("login_email")
    #     check_email_in_db = db.execute(
    #         "SELECT COUNT(*) FROM users WHERE email = :email", {"email": email}).fetchall()
    #     if check_email_in_db[0][0] == 1:
    #         email = request.form.get("login_email")
    #         password = request.form.get("login_password")
    #         retrive_password_from_db = db.execute(
    #             "SELECT password FROM users WHERE email = :email", {"email": email}).fetchall()
    #         retrive_password_from_db = retrive_password_from_db[0][0]
    #         if bcrypt.check_password_hash(retrive_password_from_db, password):
    #             user_signed_in = 1
    #             return render_template("search_page.html")
    #         else:
    #             flash('Invalid Password; Please try again')
    #             return redirect(url_for('index'))
    #     else:
    #         flash('You are not a registered User. Request you to sign-up first')
    #         return redirect(url_for('index'))

@app.route("/search_result", methods=["POST", "GET"])
def search_result():
    selection_option_heading_1 = request.form.get("selection_option_heading").lower()
    search_string_1 = request.form.get("search_string").lower()
    search_string_1 = ("'%"+search_string_1+"%'")
    check_books_in_db = db2.execute(f"SELECT isbn, title, author, year FROM books WHERE {selection_option_heading_1} ILIKE {search_string_1}").fetchall()
    return render_template("search_result.html", results = check_books_in_db)   



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)