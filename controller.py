"""
"""
from flask import Flask, render_template

app = Flask(__name__)

# flask will reload itself on changes when debug is True
# flask can execute arbitrary code if you set this True
app.debug = True 


@app.route("/")
def index(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    # flask can execute arbitrary python if you do this.
    # app.run(host='0.0.0.0') # listens on all public IPs. 

    app.run()


