from flask import Flask, render_template, request, redirect, jsonify

import json
import os

app = Flask(__name__)

# File paths
USERS_FILE = "users.json"
APPOINTMENTS_FILE = "appointments.json"

# Load and save data
def load_data(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# ---------------------------
# Routes
# ---------------------------

@app.route('/')
def home():
    return redirect('/login')

# ---------------------------
# Register Page
# ---------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle both JSON and normal form submissions
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        users = load_data(USERS_FILE)

        # Check if username exists
        if any(user['username'] == username for user in users):
            return render_template('register.html', error="⚠️ Username already exists!")

        users.append({"username": username, "password": password})
        save_data(USERS_FILE, users)
        return render_template('login.html', message="✅ Registered successfully! Please login.")

    return render_template('register.html')

# ---------------------------
# Login Page
# ---------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_data(USERS_FILE)

        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect('/book')
        return render_template('login.html', error="❌ Invalid credentials!")
    return render_template('login.html')

# ---------------------------
# Appointment Booking
# ---------------------------
@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        time = request.form.get('time')

        appointments = load_data(APPOINTMENTS_FILE)
        appointments.append({
            "name": name,
            "date": date,
            "time": time
        })
        save_data(APPOINTMENTS_FILE, appointments)

        return render_template('book_appointment.html', message="✅ Appointment booked successfully!")

    return render_template('book_appointment.html')

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
