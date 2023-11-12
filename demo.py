from flask import Flask, render_template, request, jsonify
import mysql.connector as c1234
import random
import webbrowser
import random
import language_tool_python  
import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
app = Flask(__name__)

# MySQL Database Configuration
con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
cursor = con.cursor()

@app.route('/')
def index():
    # Fetch all messages from the database
    cursor.execute("SELECT id, subject, text, sender FROM admin1")
    messages = cursor.fetchall()
    return render_template('inbox.html', messages=messages)

@app.route('/message/<int:message_id>')
def message(message_id):
    # Fetch the selected message from the database
    cursor.execute("SELECT subject, text FROM admin1 WHERE id = %s", (message_id,))
    message = cursor.fetchone()
    return render_template('message.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
