from app import app
from flask import render_template

@app.route('/')
@app.route('/index/<name>')
def index(name="<<hello world>>"):
    return render_template("index.html",text=name)
@app.route("/autor")
def autor():
    return render_template("autor.html")
@app.route("/extraction")
def extraction():
    return render_template("opinion_extr.html")
@app.route("/lista")
def lista():
    return render_template("opinion_list.html")