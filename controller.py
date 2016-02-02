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


@app.route("/hello")
@app.route("/hello/<name>")
def index(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    # flask can execute arbitrary python if you do this.
    # app.run(host='0.0.0.0') # listens on all public IPs. 

    app.run()


