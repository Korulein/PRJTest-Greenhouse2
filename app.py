from flask import Flask, jsonify, render_template, request, redirect
import datetime, serial, time, threading
from datetime import datetime

app = Flask(__name__)

data_lock = threading.Lock()

global user
global temp, hum, light
temp = "N/A"
hum = "N/A"
light = "N/A"

@app.route("/")
def login():
    return render_template("Login.html")

@app.route("/Login", methods=['POST'])
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
    return render_template("linker.html", user=user)

# Render Template Examples
@app.route('/Minerva')
def minerva():
    return render_template("namer.html", person_name="Minerva")

@app.route('/Falacer')
def falacer():
    return render_template("namer.html", person_name="Falacer")

@app.route("/Time")
def time_page():
    return render_template('Time.html')

# API route to return the current time and sensor data as JSON
@app.route("/get-time")
def get_time():
    current_time = timedata()

    # Safely read the sensor values with lock
    with data_lock:
        temperature = temp
        humidity = hum
        licht = light

    # Return the data as JSON
    return jsonify(
        time1=current_time,
        light1=licht,
        humidity1=humidity,
        temperature1=temperature
    )

# Function to get the current time
def timedata():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

# Function to continuously grab data from Arduino (runs in a background thread)
def grab():
    global temp, hum, light

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)  # Give some time to establish the connection

    while True:
        # Read the line of data from the Arduino
        arduino_data = ser.readline().decode('utf-8').strip()

        data_parts = arduino_data.split(",")

            # Extract temperature, humidity, and light level
        if len(data_parts) == 3:
            temp_val = data_parts[0].split(":")[1].strip()  # Extract temperature
            hum_val = data_parts[1].split(":")[1].strip()   # Extract humidity
            light_val = data_parts[2].split(":")[1].strip() # Extract light level

                    # Safely update the global variables with lock
            with data_lock:
                temp = temp_val
                hum = hum_val
                light = light_val

                    # Display the values
                print(f"Temperature: {temp}°C, Humidity: {hum}%, Light Level: {light}")

        # Delay to match Arduino sending frequency (every 2 seconds)
        time.sleep(2)


# Start the background thread to fetch data from the Arduino
if __name__ == "__main__":
    threading.Thread(target=grab, daemon=True).start()  # Start the grab function in a separate thread
    app.run(debug=True)
