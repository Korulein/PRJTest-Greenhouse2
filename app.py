from flask import Flask, jsonify, render_template, request, redirect
import datetime
from datetime import datetime
import random

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("Login.html")

global user

@app.route("/Login", methods = ['POST'])
def register():
    global user
    username = request.form["username"]
    password = request.form["password"]
    user = username
    print("Username: " + str(username) + " Password: " + str(password))
    return redirect("/Redirect")

# Main page to fetch the links of all other pages
@app.route('/Redirect')
def linker():
    global user
    return render_template("linker.html", user = user)

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
    current_light= random.uniform(500.0, 750.0)
    formatted_float = format(current_light, '.10f')
    return jsonify(time1=current_time, light1=formatted_float)

# Function to get the current time
def timedata():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time