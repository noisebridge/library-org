"""
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import os

sqlite_db = 'sqlite:////' + os.path.join(os.getcwd(), 'tmp', 'db.sqlite')

app = Flask(__name__)

#sqlalchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_db
db = SQLAlchemy(app)


# flask will reload itself on changes when debug is True
# flask can execute arbitrary code if you set this True
app.debug = True 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Book(db.Model):
    """ Build a model based on the available fields in the openlibrary.org API.

    Notes: 
        authors - will be stored as a long string, openlibrary delivers it as a list of objects.

    Additional info:
        curl 'https://openlibrary.org/api/books?bibkeys=ISBN:9780980200447&jscmd=data&format=json'
        using jscmd=data yields less info but is more stable
        using jscmd=details will give us book cover thumbnail, preview url, table of contents, and more
    """
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(200), unique=True)
    authors = db.Column(db.String(200), unique=True)
    publish_date = db.Column(db.String(20), unique=True)
    number_of_pages = db.Column(db.String(20), unique=True)

    def __init__(self, isbn, title, authors, publish_date, number_of_pages):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publish_date = publish_date
        self.number_of_pages = number_of_pages

    def __repr__(self):
        return '<Title: {}>'.format(self.title)


@app.route("/hello")
@app.route("/hello/<name>")
def index(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    # flask can execute arbitrary python if you do this.
    # app.run(host='0.0.0.0') # listens on all public IPs. 

    app.run()


