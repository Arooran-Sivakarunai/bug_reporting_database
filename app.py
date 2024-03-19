from flask import Flask
from flask import render_template

app = Flask(__name__)
#test
@app.route("/")
def hello_world():
    return render_template("log_in.html")

