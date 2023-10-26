from flask import Flask, render_template, request
import mysql.connector as c1234
import random
import webbrowser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/ValidateAdmin', methods=['POST'])
def ValidateAdmin():
    return render_template('registration.html')

@app.route('/ValidateUser', methods=['POST'])
def ValidateUser():
    name1 = request.form['uname']
    passw = request.form['password']
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from logindetails"
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    for i in records:
        if i[0] == name1 and i[1] == passw:
            return render_template('userDash.html')
    return render_template('registration.html')


@app.route('/Registration')
def Registration():
    return render_template('registration.html')

@app.route('/registerUser', methods=['POST'])
def registerUser():
    name1 = request.form['uname']
    email1 = request.form['email']
    passw = request.form['password']
    phonenum = request.form['phonenum']
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    mySql_insert_query = "INSERT INTO logindetails VALUES ('{}', '{}', '{}', '{}')".format(
        name1, passw, email1, phonenum)
    cursor = con.cursor()
    cursor.execute(mySql_insert_query)
    con.commit()
    return render_template('login.html')

app.run(debug=True)
