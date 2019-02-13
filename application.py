import os

from flask import Flask, render_template, request
from redis import Redis
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    "postgresql://dipesh:dipesh123@db:5432/flights")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run('0.0.0.0', 4002)


