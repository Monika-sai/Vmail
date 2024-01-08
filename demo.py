from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace the following with your MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hari@9RUSHI',
    'database': 'vmail',
}

# Establish a connection to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/')
def index():
    # Fetch all emails from the database
    cursor.execute("SELECT id, sender, subject FROM emails")
    emails = cursor.fetchall()
    return render_template('index.html', emails=emails)

@app.route('/search', methods=['POST'])
def search():
    # Get the search term from the form
    search_term = request.form['search']
    
    # Search for emails containing the search term in sender, subject, or message
    cursor.execute("SELECT id, sender, subject FROM emails WHERE sender LIKE %s OR subject LIKE %s OR message LIKE %s",
                   (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    search_results = cursor.fetchall()
    
    return render_template('index.html', emails=search_results, search_term=search_term)

@app.route('/email/<int:email_id>')
def view_email(email_id):
    # Fetch the details of the selected email
    cursor.execute("SELECT * FROM emails WHERE id = %s", (email_id,))
    email = cursor.fetchone()
    
    return render_template('email.html', email=email)

if __name__ == '__main__':
    app.run(debug=True)
