from flask import Flask, jsonify, render_template
import time
import datetime
from datetime import datetime
import random

app = Flask(__name__)

# Main page to fetch the links of all other pages
@app.route('/')
def linker():
    return "linker.html"

# Render Template Examples
@app.route('/Minerva')
def minerva():
    return render_template("namer.html", person_name = "Minerva")

@app.route('/Falacer')
def falacer():
    return render_template("namer.html", person_name = "Falacer"
                           )
@app.route("/Time")
def time_page():
    return render_template('Time.html')

# API route to return the current time as JSON
@app.route("/get-time")
def get_time():
    current_time = timedata()
    return jsonify(time1=current_time)

# Function to get the current time
def timedata():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

