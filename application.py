import os
import secret
from os import environ
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from functools import wraps

user_database_url = environ.get('DATABASE_URL', secret.user_database_url)
books_database_url =  environ.get('HEROKU_POSTGRESQL_BLACK_URL', secret.books_database_url)

engine = create_engine(user_database_url)
engine2 = create_engine(books_database_url)
db = scoped_session(sessionmaker(bind=engine))
db2 = scoped_session(sessionmaker(bind=engine2))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

def ensure_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            flash("Please log in first")
            return redirect(url_for('index'))
        return fn(*args, **kwargs)
    return wrapper

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key =  environ.get('SECRET_KEY', secret.secret_key)
login = LoginManager(app)

bcrypt = Bcrypt(app)

@app.route("/", methods=('GET', 'POST'))
def index():
    return render_template("index.html")

# @app.route('/submit', methods=('GET', 'POST'))
# def submit():
#     form = MyForm()
#     if form.validate_on_submit():
#         return redirect(url_for('search_page'))
#     return render_template('submit.html', form=form)


@app.route("/search_page", methods=["POST", "GET"])
def search_pg():
    # return render_template("search_page.html")
    if request.method == "POST":
        if 'sign-up_form' in request.form:
            email = request.form.get("email")
            check_email_in_db = db.execute(
                "SELECT COUNT(*) FROM users WHERE email = :email", {"email": email}).fetchall()
            if check_email_in_db[0][0] == 1:
                flash("Sorry, this username has already been taken, please revisit the home page and try with a new email address")
                return redirect(url_for('index'))
            else:
                password = request.form.get("password")
                password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
                db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {
                        "email": email, "password": password})
                db.commit()
                session['user'] = str(email)
                return render_template("search_page.html")
        elif 'login_form' in request.form:
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
                    session['user'] = str(email)
                    # flash("Logged in as: " + email )  this is working and hence this is commented out
                    return render_template("search_page.html")
                else:
                    flash('Invalid Password; Please try again')
                    return redirect(url_for('index'))
            else:
                flash('You are not a registered User. Request you to sign-up first')
                return redirect(url_for('index'))
    elif request.method == "GET":
        if 'user' in session:
            return render_template("search_page.html")
        else:
            flash("Please log-in first")
            return redirect(url_for('index'))


@app.route("/search_result", methods=["POST", "GET"])
@ensure_logged_in
def search_result():
    selection_option_heading_1 = request.form.get("selection_option_heading").lower()
    search_string_1 = request.form.get("search_string").lower()
    search_string_1 = ("'%"+search_string_1+"%'")
    check_books_in_db = db2.execute(f"SELECT isbn, title, author, year FROM books WHERE {selection_option_heading_1} ILIKE {search_string_1}").fetchall()
    return render_template("search_result.html", results = check_books_in_db)   

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)