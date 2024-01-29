from flask import Flask, render_template, request, redirect, url_for
import random
import time

app = Flask(__name__)

# In-memory storage for simplicity. In a production environment, use a database.
otp_data = {}

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        mobile_number = request.form['mobile_number']

        # Generate a random 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Store OTP along with mobile number and expiry time (5 minutes in this example)
        otp_data[mobile_number] = {'otp': otp, 'expiry_time': time.time() + 100}

        # Send OTP to the user (use a third-party SMS gateway or service)

        # Redirect to OTP verification page
        return redirect(url_for('verify_otp', mobile_number=mobile_number))

    return render_template('register.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    mobile_number = request.args.get('mobile_number')
    stored_data = otp_data.get(mobile_number)

    if stored_data:
        if request.method == 'POST':
            user_otp = request.form['otp']

            if stored_data['otp'] == user_otp and time.time() < stored_data['expiry_time']:
                # Valid OTP, proceed with registration
                del otp_data[mobile_number]  # Remove stored OTP after successful verification
                return "Registration successful!"
            else:
                return "Invalid OTP or OTP expired. Please try again."

        return render_template('verify_otp.html', mobile_number=mobile_number)

    return "Invalid mobile number. Please register again."

if __name__ == '__main__':
    app.run(debug=True)
