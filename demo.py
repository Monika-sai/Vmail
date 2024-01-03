from flask import Flask, render_template, request, jsonify
import mysql.connector as mysql
import random
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from gtts import gTTS
import os
import smtplib
import language_tool_python

app = Flask(__name__)

class Global:
    c = ""
    name = ""
    length = 0
    regName = ''
    regPass = ''
    regEmail = ''
    regPhone = ''
    otp = ''
    message = ''
    msgs = ''

g = Global()

class Database:
    def __init__(self):
        self.connection = mysql.connect(host="localhost", user="root", passwd="hari@9RUSHI", database="vmail")
        self.cursor = self.connection.cursor()

    def execute_query(self, query, fetch_all=False):
        self.cursor.execute(query)
        if fetch_all:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

class EmailSender:
    @staticmethod
    def send_email(sender_email, sender_password, recipient_email, subject, body):
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

class VmailApp:
    def __init__(self):
        self.db = Database()

    def generate_random_key(self):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=26))

    def encrypt_text(self, text, key):
        encrypted_text = ''
        for char in text:
            if char in key:
                encrypted_text += key[char]
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt_text(self, text, key):
        decrypted_text = ''
        for char in text:
            if char in key.values():
                decrypted_text += [k for k, v in key.items() if v == char][0]
            else:
                decrypted_text += char
        return decrypted_text

    def grammar_correction(self, text):
        tool = language_tool_python.LanguageTool('en-US')
        corrected_text = tool.correct(text)
        return corrected_text

    def send_otp_mail(self, recipient_email):
        sender_email = '20b01a05c6@svecw.edu.in'
        sender_password = 'hari@9RUSHI'
        smtp_server = 'smtp.gmail.com'

        otp = ''.join(str(random.randint(1, 9)) for _ in range(6))
        g.otp = otp

        subject = "Vmail : Thanks for your interest in Vmail"
        body = f"Please use this OTP to complete the registration process: {otp}"

        EmailSender.send_email(sender_email, sender_password, recipient_email, subject, body)

    def registration_successful_mail(self, recipient_email):
        sender_email = '20b01a05c6@svecw.edu.in'
        sender_password = 'hari@9RUSHI'
        smtp_server = 'smtp.gmail.com'

        subject = "Vmail : Registration Successful"
        body = "Your account has been created. Please login to continue."

        EmailSender.send_email(sender_email, sender_password, recipient_email, subject, body)

    def register_user(self, name, email, password, phone):
        query = f"SELECT * FROM logindetails WHERE uname = '{name}' OR password = '{password}' OR email = '{email}' OR mobilenum = '{phone}'"
        records = self.db.execute_query(query, fetch_all=True)

        if len(records) >= 1:
            raise Exception("Username or password already exists")

        self.send_otp_mail(email)

    def validate_user(self, name, password):
        query = "SELECT * FROM logindetails WHERE uname = '{}' AND password = '{}'".format(name, password)
        records = self.db.execute_query(query, fetch_all=True)

        if records:
            g.c = records[0][2]
            g.name = records[0][0]
            return True
        else:
            return False

    def send_mail(self, sender, receiver, subject, message, name, image=None):
        sender_email = '20b01a05c6@svecw.edu.in'
        sender_password = 'hari@9RUSHI'
        smtp_server = 'smtp.gmail.com'

        # Grammar correction
        subject = self.grammar_correction(subject)
        message = self.grammar_correction(message)

        # Encrypt subject and message
        key = self.generate_random_key()
        encrypted_subject = self.encrypt_text(subject, key)
        encrypted_message = self.encrypt_text(message, key)

        # Send the email
        EmailSender.send_email(sender_email, sender_password, receiver, f"Vmail : Message from {name}", f"You have got a message from {sender}. Message: {encrypted_message}. View in Vmail app.", )

        # Save the encrypted data to the database
        image_data, image_name = '', ''
        if image:
            image_data = image.read()
            image_name = image.filename

        my_sql_insert_query = "INSERT INTO admin2 (sender, subject, text, kys, receiver, name, image_data) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (sender, encrypted_subject, encrypted_message, key, receiver, image_name, image_data)

        self.db.execute_query(my_sql_insert_query, fetch_all=False)
        self.db.commit()

    def get_email_suggestions(self, prefix):
        query = f"SELECT email FROM logindetails WHERE email LIKE '{prefix}%' LIMIT 5"
        suggestions = [row[0] for row in self.db.execute_query(query, fetch_all=True)]
        return suggestions

    def autocomplete(self):
        prefix = request.args.get('prefix', '')
        suggestions = self.get_email_suggestions(prefix)
        return jsonify(suggestions=suggestions)

    def inbox(self):
        query = f"SELECT id, subject, text, sender, kys, timestamp_value FROM admin2 WHERE receiver = '{g.c}' ORDER BY timestamp_value DESC"
        messages = self.db.execute_query(query, fetch_all=True)
        return self.process_messages(messages)

    def process_messages(self, messages):
        subject = []
        text = []
        keys = []
        for i in messages:
            subject.append(i[1])
            text.append(i[2])
            keys.append(i[4])

        actual_text = []
        actual_sub = []

        for i in range(len(subject)):
            sub = ''
            txt = ''
            subject_decrypt = subject[i].split()
            text_decrypt = text[i].split()

            for j in range(len(subject_decrypt)):
                sub += self.decrypt_text(subject_decrypt[j], keys[i]) + ' '

            for k in range(len(text_decrypt)):
                txt += self.decrypt_text(text_decrypt[k], keys[i]) + ' '

            actual_sub.append(sub)
            actual_text.append(txt)

        return actual_sub, actual_text

vmail_app = VmailApp()

@app.route('/')
def home():
    if g.c == "":
        return render_template('login.html')
    else:
        return render_template('home.html', name=g.name, msgs=g.msgs)

@app.route('/register/', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        g.regName = request.form['name']
        g.regPass = request.form['password']
        g.regEmail = request.form['email']
        g.regPhone = request.form['phone']

        vmail_app.register_user(g.regName, g.regEmail, g.regPass, g.regPhone)
        return render_template('otp.html')
    else:
        return render_template('register.html')

@app.route('/register2/', methods=["POST", "GET"])
def register2():
    if request.method == "POST":
        otp = request.form['otp']
        if otp == g.otp:
            my_sql_insert_query = "INSERT INTO logindetails (uname, password, email, mobilenum) VALUES (%s, %s, %s, %s)"
            val = (g.regName, g.regPass, g.regEmail, g.regPhone)
            vmail_app.db.execute_query(my_sql_insert_query, fetch_all=False)
            vmail_app.db.commit()

            vmail_app.registration_successful_mail(g.regEmail)
            return render_template('login.html', message="Registration Successful! Please login.")
        else:
            return render_template('otp.html', message="Invalid OTP. Please try again.")
    else:
        return render_template('otp.html')

@app.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        if vmail_app.validate_user(name, password):
            g.msgs, actual_text = vmail_app.inbox()
            return render_template('home.html', name=g.name, msgs=g.msgs, actual_text=actual_text)
        else:
            return render_template('login.html', message="Invalid Username or Password. Please try again.")
    else:
        return render_template('login.html')

@app.route('/compose/')
def compose():
    if g.c == "":
        return render_template('login.html', message="Please login to continue.")
    else:
        return render_template('compose.html', name=g.name)

@app.route('/sendmail/', methods=["POST"])
def sendmail():
    if request.method == "POST":
        sender = g.c
        receiver = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        name = g.name
        image = request.files['file']

        vmail_app.send_mail(sender, receiver, subject, message, name, image)

        g.msgs, actual_text = vmail_app.inbox()
        return render_template('home.html', name=g.name, msgs=g.msgs, actual_text=actual_text, message="Email sent successfully!")
    else:
        return render_template('home.html', name=g.name, msgs=g.msgs)

@app.route('/autocomplete/', methods=["GET"])
def autocomplete():
    return vmail_app.autocomplete()

if __name__ == '__main__':
    app.run(debug=True)
