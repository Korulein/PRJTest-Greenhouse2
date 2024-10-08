from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def linker():
    return "linker.html"

@app.route('/Minerva')
def minerva():
    return render_template("namer.html", person_name = "Minerva")
