"""
"""
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from flask_wtf import Form, RecaptchaField
from wtforms import StringField, TextField, validators

from request_book import reorganize_openlibrary_data, reorganize_manual_data

import requests
import json

import os

from ConfigParser import SafeConfigParser


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = "library.cfg"
CONFIG_PATH = os.path.join(PROJECT_ROOT, CONFIG_FILE)
CONFIG = SafeConfigParser()
CONFIG.read(CONFIG_PATH)

# Configuration Secrets
APP_SECRET_KEY = CONFIG.get("secrets", "APP_SECRET_KEY")
WTF_CSRF_SECRET_KEY = CONFIG.get("secrets", "WTF_CSRF_SECRET_KEY")
NEW_ISBN_SUBMIT_SECRET = CONFIG.get("secrets", "NEW_ISBN_SUBMIT_SECRET")
RECAPTCHA_PUBLIC_KEY = CONFIG.get("secrets", "RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = CONFIG.get("secrets", "RECAPTCHA_PRIVATE_KEY")

db_name = 'books.sqlite'
DB_DIR = "database"
sqlite_db = 'sqlite:////' + os.path.join(PROJECT_ROOT, 'database', db_name)

# haven't used this in the templates, currently using exact path on a few files.
# not even sure if this django style approach works with flask
STATIC_DIR = "static"

app = Flask(__name__)

app.secret_key = APP_SECRET_KEY

# flask will reload itself on changes when debug is True
# flask can execute arbitrary code if you set this True
app.debug = False

#sqlalchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_db
db = SQLAlchemy(app)

PAGINATE_BY_HOWMANY = 15

# == recaptcha ==
# recaptcha disabled - it is ready to be implemented now
#RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
#RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
#app.config['RECAPTCHA_USE_SSL'] = False



class Book(db.Model):
    """ Build a model based on the available fields in the openlibrary.org API.

    Notes:
        authors - will be stored as a long string, openlibrary delivers it as a list of objects.

    Additional info:
        curl 'https://openlibrary.org/api/books?bibkeys=ISBN:9780980200447&jscmd=data&format=json'
        using jscmd=data yields less info but is more stable
        using jscmd=details will give us book cover thumbnail, preview url, table of contents, and more

    Enhancements:
        use jscmd=details to get cover thumbnail... this could be a key piece of the template
    """
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(200), unique=False)
    authors = db.Column(db.String(200), unique=False)
    publish_date = db.Column(db.String(30), unique=False)
    number_of_pages = db.Column(db.String(10), unique=False)
    subjects = db.Column(db.String(5000), unique=False)
    openlibrary_medcover_url = db.Column(db.String(500), unique=False)
    openlibrary_preview_url = db.Column(db.String(500), unique=False)
    dewey_decimal_class = db.Column(db.String(50), unique=False)

    def __init__(self,  isbn,
                        title,
                        number_of_pages,
                        publish_date,
                        authors,
                        subjects,
                        openlibrary_medcover_url,
                        openlibrary_preview_url,
                        dewey_decimal_class):

        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publish_date = publish_date
        self.number_of_pages = number_of_pages
        self.subjects = subjects
        self.openlibrary_medcover_url = openlibrary_medcover_url
        self.openlibrary_preview_url = openlibrary_preview_url
        self.dewey_decimal_class = dewey_decimal_class

    def __repr__(self):
        return '<Title: >'.format(self.title)


class ISBNForm(Form):
    isbn = StringField('isbn', [validators.Length(min=10, max=13), validators.Regexp(r'^[0-9X]*$')])


class ManualForm(Form):
    """ WTForm class for manual submits.
    The description parameter is used for user-friendly text.
    """

    isbn = StringField('isbn', [validators.Length(min=10, max=13), validators.Regexp(r'^[0-9X]*$')], description='ISBN*')
    title = StringField('title', [validators.Length(min=1, max=200)], description='Title*')
    authors = StringField('authors', [validators.Length(min=1, max=200)], description='Author(s)*')
    publish_date = StringField('publish_date', [validators.Length(max=30)], description='Published')
    number_of_pages = StringField('number_of_pages', [validators.Length(max=10)], description='Pages')
    subjects = StringField('subjects', [validators.Length(max=5000)], description='Subjects')
    cover = StringField('cover_url', [validators.Optional(), validators.Length(max=500), validators.URL(require_tld=True)], description='Cover Image URL')
    preview_url = StringField('preview_url', [validators.Optional(), validators.Length(max=500), validators.URL(require_tld=True)], description='Preview URL')
    dewey_decimal_class = StringField('dewey_decimal_class', [validators.Length(max=50)], description='Dewey Decimal Class')


class ISBNSubmitForm(Form):
    secret = StringField('isbn', [validators.Length(min=1, max=200)])


class SampleForm(Form):
    name = StringField('name', validators=[validators.DataRequired()])

@app.route("/sampleform/", methods=('GET', 'POST'))
def sampleform():
    form = SampleForm()
    if form.validate_on_submit():
        return redirect("/sampleform")
    return render_template("sampleform.html", form=form)


@app.route("/test/")
def test():
    """ Test frontend integration
    """
    return render_template('test.html')


@app.route("/index/")
@app.route("/")
def home():
    return redirect(url_for('index', page=1))


@app.route("/submit/", methods=("GET","POST"))
def submit(secret=None):
    secret_form = ISBNSubmitForm(request.form)
    if request.method == "GET":
        return redirect(url_for('new_isbn'))
    if request.method == "POST" and secret_form.validate():
        secret = secret_form.secret.data

    if secret != NEW_ISBN_SUBMIT_SECRET:
        return("Bad Secret, try again. This page will be more friendly later :-)")

    bookdata_list = session.get('bookdata', None)
    session.clear()
    if bookdata_list:
        bookdata_list = json.loads(bookdata_list)
        # this bookdata_list obviously needs to be a dict,
        # it wasn't originally clear if this code would
        # still exist after its first use.
        # this still may be true so I have not changed it yet.
        # note: this should probably be abstracted for use by request_book.py and here.
        bookdata = Book(*bookdata_list[0:9])
    else:
        return("no book!")

    try:
        db.session.add(bookdata)
        db.session.commit()
        session["newbookflash"] = True
        return redirect(url_for('detail', id=bookdata.id))

    except IntegrityError:
        db.session.rollback()
        return("book already exists. how did you get here?")


@app.route("/new/", methods=('GET', 'POST'))
def new_isbn(isbn=None):
    """ Allow a new ISBN to be added to the book database.
    """
    isbn_form = ISBNForm(request.form)
    secret_form = ISBNSubmitForm(request.form)
    if request.method == "GET":
        pass

    if request.method == "POST" and isbn_form.validate():
        isbn = isbn_form.isbn.data
        isbn_exists = Book.query.filter_by(isbn=isbn).first()

        if isbn_exists:
            return render_template("new_isbn.html", isbn_form=isbn_form, secret_form=secret_form, isbn=isbn, book=isbn_exists, isbn_exists=True)
        else:
            # make a book object, render it, and if the user submits, then ingest it.
            # SO -  we need to get the ingestion script repackaged so a single run of the ingester
            #       can be imported as a function.
            URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
            r = requests.get(URL.format(isbn=isbn))

            if(r.status_code == 200):

                if r.json():
                    bookdata_list = reorganize_openlibrary_data("ISBN:"+isbn, r.json()["ISBN:"+isbn])

                    session['bookdata'] = json.dumps(bookdata_list)

                    # this bookdata_list obviously needs to be a dict,
                    # it wasn't originally clear if this code would
                    # still exist after its first use.
                    # this still may be true so I have not changed it yet.
                    # note: this should probably be abstracted for use by request_book.py and here.
                    # KEY POINT: this is only done here too because we need to send it to the template.
                    bookdata = Book(*bookdata_list[0:9])
                    return render_template("new_isbn.html", isbn_form=isbn_form, secret_form=secret_form, isbn=isbn, book=bookdata, isbn_exists=False)

                    # this doesn't go here, this happens when the user verifies the book is right
                    #db.session.add(bookdata)
                else:
                    pass
                    # this is rendered as logic in the view lol
            else:
                pass
                # this is rendered as logic in the view lol

    return render_template("new_isbn.html", isbn_form=isbn_form, secret_form=secret_form, isbn=isbn)


@app.route("/new_manual/", methods=('GET', 'POST'))
def new_manual():
    """ Allow users to manually fill in book details and add them to the database.
    """
    manual_form = ManualForm(request.form)
    secret_form = ISBNSubmitForm(request.form)

    if request.method == 'GET':
        pass

    if request.method == "POST" and manual_form.validate():
        isbn_exists = Book.query.filter_by(isbn=manual_form.isbn.data).first()

        if isbn_exists:
            return render_template("new_manual.html", manual_form=manual_form, secret_form=secret_form, book=isbn_exists, isbn_exists=True)

        bookdata_list = reorganize_manual_data(manual_form)

        session['bookdata'] = json.dumps(bookdata_list)

        bookdata = Book(*bookdata_list[0:9])
        return render_template("new_manual.html", manual_form=manual_form, secret_form=secret_form, book=bookdata)


    return render_template("new_manual.html", manual_form=manual_form, secret_form=secret_form)


@app.route("/all/")
def all():
    """ Show everything on one page.

    This feature may eventually become a legacy feature.
    Useful if you wish to use a browser search tool rather than relying on the
    advanced search.
    Depends on the fields you want to search being visible in the template.
    """
    books = Book.query.order_by(Book.title.asc())
    return render_template('all.html', books=books)


@app.route("/detail/<int:id>/")
def detail(id=1):
    """ Show an individual work
    """

    newbookflash = session.get("newbookflash", False)
    session.clear()

    book = Book.query.get(id)
    return render_template('detail.html', book=book, newbookflash=newbookflash)


@app.route("/explore/")
def explore():
    """ Return a randomized all template.
    """
    books = Book.query.order_by(func.random())
    return render_template('explore.html', books=books)


@app.route("/index/<int:page>/", methods=["GET","POST"])
def index(page=1):
    """ Show an index of books, provide some basic searchability.

    The two features coded here, pagination and search, will probably be superceded
    by a different implementation.

    Options:
        javascript implementation with handlebars or moustache templating systems.
        any implementation that consumes this data from an rest/json API.
        the API is necessary anyways to allow others to interact with the app.
        allow real time search and weighted search.
        current search is too simple - sqlite query based substring search.

    """

    if request.method == "POST":
        s = request.form['search']
        return redirect(url_for('index', page=1, s=s))

    # preserve search throughout navigation
    s = request.args.get('s')

    # do a search if you have a search term
    # (make this more general for an all fields search)
    if s:
        books = Book.query.order_by(Book.title.asc()).filter(or_(Book.title.contains(s), Book.authors.contains(s), Book.subjects.contains(s))).paginate(page,PAGINATE_BY_HOWMANY,False)

    # return all books, currently sort by title ascending.
    else:
        books = Book.query.order_by(Book.title.asc()).paginate(page,PAGINATE_BY_HOWMANY,False)

    return render_template('index.html', books=books, s=s)

if __name__ == "__main__":
    # flask can execute arbitrary python if you do this.
    # app.run(host='0.0.0.0') # listens on all public IPs.

    app.run()
