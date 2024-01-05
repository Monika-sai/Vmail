from flask import Flask, render_template, request
import sqlite3
from flask import Flask, render_template, request, jsonify, flash
import mysql.connector as c1234
import random
import webbrowser
import random
import language_tool_python  
import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from gtts import gTTS
import os
import spam_model

app = Flask(__name__)

# Connect to the database
con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
cursor = con.cursor()

# Flask route to handle displaying emails

@app.route('/')
def display_email():
    page_number = int(request.args.get('page', 1))
    emails_per_page = 3
    offset = (page_number - 1) * emails_per_page
    cursor.execute(f"select email from logindetails LIMIT {emails_per_page} OFFSET {offset}")
    emails = cursor.fetchall()
    cursor.execute(f"SELECT COUNT(*) FROM logindetails")
    total_emails = cursor.fetchone()[0]
    has_next_page = offset + emails_per_page < total_emails
    return render_template('inbox.html', emails=emails, page_number=page_number, has_next_page=has_next_page)


@app.route('/emails', methods=['GET'])
def display_emails():
    # Get the page number from the query parameters, default to 1
    page_number = int(request.args.get('page', 2))

    # Set the number of emails to display per page
    emails_per_page = 3

    # Calculate the offset based on the page number
    offset = (page_number - 1) * emails_per_page

    # Query the database for emails
    cursor.execute(f"select email from logindetails LIMIT {emails_per_page} OFFSET {offset}")
    emails = cursor.fetchall()

    # Check if there are more emails to determine if next page is needed
    cursor.execute(f"SELECT COUNT(*) FROM logindetails")
    total_emails = cursor.fetchone()[0]
    has_next_page = offset + emails_per_page < total_emails

    # Render the HTML template with the retrieved emails and pagination information
    return render_template('inbox.html', emails=emails, page_number=page_number, has_next_page=has_next_page)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
