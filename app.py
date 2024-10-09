from flask import Flask, jsonify, render_template, request, redirect
import datetime, serial, time, threading
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Create a lock for thread safety when accessing shared resources
data_lock = threading.Lock()

# Initialize global variables
global user  # To store the current logged-in user's name
global sensor_data  # List to store readings from Arduino
sensor_data = []  # Empty list to hold sensor readings
max_readings = 15  # Limit for maximum readings to keep in memory

# Define the route for the login page
@app.route("/")
def login():
    return render_template("Login.html")

# Define the route for handling login requests
@app.route("/Login", methods=['POST'])
def register():
    global user
    username = request.form["username"]
    password = request.form["password"]
    user = username
    print("Username: " + str(username) + " Password: " + str(password))  # Print for debugging

    # Check for valid credentials
    if username == "Korulein":
        if password == "Minecraft678":
            return redirect("/Redirect")  # Redirect to the main dashboard if login is successful
    return redirect("/")  # Redirect back to login page on failure

# Define the route for the main dashboard page
@app.route('/Redirect')
def linker():
    global user  # Access the global user variable
    return render_template("linker.html", user=user)  # Render the dashboard template, passing the user

# Define the route for the time display page
@app.route("/Time")
def time_page():
    # Get the selected greenhouse from the request parameters, defaulting to '1' if not provided
    greenhouse_id = request.args.get('greenhouse', default='1')
    return render_template('Time.html', greenhouse_id=greenhouse_id)  # Render the time page template

# API route to return the current time and sensor data as JSON
@app.route("/get-time")
def get_time():
    current_time = timedata()

    # Safely read the sensor values with a lock to prevent race conditions
    with data_lock:
        readings = sensor_data.copy()  # Make a copy of current readings for processing
        averages = calculate_statistics(readings)  # Calculate averages from the readings

    # Return the data as JSON
    return jsonify(
        time=current_time,
        sensor_data=readings,
        averages=averages
    )

# Function to get the current time formatted as HH:MM:SS
def timedata():
    return datetime.now().strftime("%H:%M:%S")

# Function to calculate averages from sensor readings
def calculate_statistics(readings):
    # Extracting the sensor values from the readings
    light_values = [data['light'] for data in readings]
    humidity_values = [data['humidity'] for data in readings]
    temperature_values = [data['temperature'] for data in readings]

    # Average calculations with division by zero handling
    averages = [
        (sum(light_values) / len(light_values)) if len(light_values) > 0 else 0,
        (sum(humidity_values) / len(humidity_values)) if len(humidity_values) > 0 else 0,
        (sum(temperature_values) / len(temperature_values)) if len(temperature_values) > 0 else 0
    ]

    return averages  # Return only averages

# Function to continuously grab data from Arduino (runs in a background thread)
def grab():
    global sensor_data

    # Initialize the serial connection to Arduino
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(5)  # Give some time to establish the connection

    while True:
        # Read a line of data from the Arduino
        arduino_data = ser.readline().decode('utf-8').strip()  # Read and decode the data

        # Ensure there is valid data
        if arduino_data:
            print(f"Received: {arduino_data}")  # Print raw data from Arduino

            # Split the data based on commas found in Arduino code
            data_parts = arduino_data.split(",")

            if len(data_parts) == 3:  # Ensure we have exactly three data points
                try:
                    # Parse & Extract the sensor values from the data string
                    temp_val = float(data_parts[0].split(":")[1].strip())
                    hum_val = float(data_parts[1].split(":")[1].strip())
                    light_val = float(data_parts[2].split(":")[1].strip())

                    with data_lock:
                        # Add new reading to sensor_data
                        sensor_data.append({ # Store readings
                            'temperature': temp_val,
                            'humidity': hum_val,
                            'light': light_val,
                            'time': timedata()
                        })

                        # If the number of readings exceeds the limit, remove the oldest reading
                        if len(sensor_data) > max_readings:
                            sensor_data.pop(0)  # Remove the oldest reading

                    # Display the sensor values
                    print(f"Temperature: {temp_val}°C, Humidity: {hum_val}%, Light Level: {light_val}")

                except (IndexError, ValueError) as e:
                    print(f"Error processing data: {arduino_data} - {e}")  # Print any errors encountered

        # Delay to match Arduino sending frequency (every 5 seconds)
        time.sleep(5)

# Start the background thread to fetch data from the Arduino
if __name__ == "__main__":
    threading.Thread(target=grab, daemon=True).start()  # Start the grab function in a separate thread
    app.run(debug=True)  # Run the Flask application with debug mode enabled
