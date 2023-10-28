from flask import Flask, render_template, request
import mysql.connector as c1234
import random
import webbrowser
import random

app = Flask(__name__)

class Global:
    c = ""

g = Global()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/ValidateAdmin', methods=['POST'])
def ValidateAdmin():
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from admin"
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    text = []
    subject = []
    send = []
    key = []
    to = []
    for i in records:
        subject.append(i[1])
        text.append(i[2])
        key.append(i[3])
        send.append(i[0])
        to.append(i[4])
    actualSub = []
    actualTxt = []
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = key[i]
        for i in subjectDecrypt:
            for j in i:
                sub += chr((k.index(j) + 65))
            sub += ' '
        for i in textDecrypt:
            for j in i:
                txt += chr((k.index(j) + 65))
            txt += ' '
        actualSub.append(sub)
        actualTxt.append(txt)
    
    answer = []
    tbl = "<tr><td>To</td><td>Subject</td><td>Text</td><td>From</td></tr>"
    answer1 = [0] * (len(text) + 1)
    answer1[0] = tbl
    for i in range(len(text)):
        answer = []
        a = "<tr><td>%s</td>" % to[i]
        answer.append(a)
        a1 = "<td>%s</td>" % actualSub[i]
        answer.append(a1)
        a2 = "<td>%s</td>" % actualTxt[i]
        answer.append(a2)
        a3 = "<td>%s</td></tr>" % send[i]
        answer.append(a3)
        answer1[i + 1] = answer
    if len(answer1) == 1:
        contents = '''<!DOCTYPE html>
            <html>
            <head>
            <meta content = "text/html; charset = UTF-8"
            http-equip = "content-type">
            </head>
            <body>
            <center>
            <h3> No Recieved items found </h3>
            </center>
            </body>
            </html>
            '''
    else:
        contents = '''<!DOCTYPE html>
                <html>
                <head>
                <meta content = "text/html; charset = UTF-8"
                http-equip = "content-type">
                <style>
                td {
                    padding :0 15px;
                }
                </style>
                <title>Time Table</title>
                </head>
                <body>
                    <div class="card" id="generatePDF">

                <br><br>
                <center>
                <table border = 1>
                %s
                </table>
                <br><br>
                
                <button id="pdfButton"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzxA1IZaV_fN96xiySAwgY5iZiM-pIg9W9ig&usqp=CAU" style="height:30px;width:30px;"><b style="padding-bottom:5px;" class="text"> <center>&nbsp; &nbsp Download</center></b></button>
    
    </div>
    </center>
        <script>
        var button = document.getElementById("pdfButton");
        var makepdf = document.getElementById("generatePDF");
        button.addEventListener("click", function () {
            var mywindow = window.open("", "PRINT", "height=600,width=600");
            mywindow.document.write(makepdf.innerHTML);
            mywindow.document.close();
            mywindow.focus();
            mywindow.print();
            return true;
        });
    </script>

                </body>
                </html>
                ''' % (answer1)
    filename = 'demo39.html'

    def main(contents, filename):
        output = open(filename, "w")
        output.write(contents)
        output.close()
    main(contents, filename)
    webbrowser.open(filename)
    return render_template('demo3.html')

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
            g.c = i[2]
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

@app.route('/email', methods=['POST'])
def email():
    reciever = request.form['reciever']
    subject = request.form['subject']
    message = request.form['message']
    sender = g.c
    subject = subject.upper()
    message = message.upper()
    hm = {}
    key = ''
    alpha = [i for i in range(26)]
    for i in range(26):
        x = random.randint(0, len(alpha) - 1)
        x = alpha[x]
        hm[chr(i + ord('A'))] = chr(x + ord('A'))
        key += chr(x + ord('A'))
        alpha.remove(x)
    subject.upper()
    message.upper()
    subject = subject.split()
    encryptedSub = ''
    for i in subject:
        for j in i:
            encryptedSub += hm[j]
        encryptedSub += " "
    encryptedMessage = ''
    message = message.split()
    for i in message:
        for j in i:
            encryptedMessage += hm[j]
        encryptedMessage += " "
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    mySql_insert_query = "INSERT INTO admin VALUES ('{}', '{}', '{}', '{}', '{}')".format(
        sender, encryptedSub, encryptedMessage, key, reciever)
    cursor = con.cursor()
    cursor.execute(mySql_insert_query)
    con.commit()
    return render_template('login.html')
    

@app.route('/SendMail')
def SendMail():
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from admin"
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    text = []
    subject = []
    to = []
    key = []
    for i in records:
        if i[0] == g.c:
            subject.append(i[1])
            text.append(i[2])
            key.append(i[3])
            to.append(i[4])
    actualSub = []
    actualTxt = []
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = key[i]
        for i in subjectDecrypt:
            for j in i:
                sub += chr((k.index(j) + 65))
            sub += ' '
        for i in textDecrypt:
            for j in i:
                txt += chr((k.index(j) + 65))
            txt += ' '
        actualSub.append(sub)
        actualTxt.append(txt)
    
    answer = []
    tbl = "<tr><td>From</td><td>Subject</td><td>Text</td><td>To</td></tr>"
    answer1 = [0] * (len(text) + 1)
    answer1[0] = tbl
    for i in range(len(text)):
        answer = []
        a = "<tr><td>%s</td>" % g.c
        answer.append(a)
        a1 = "<td>%s</td>" % actualSub[i]
        answer.append(a1)
        a2 = "<td>%s</td>" % actualTxt[i]
        answer.append(a2)
        a3 = "<td>%s</td></tr>" % to[i]
        answer.append(a3)
        answer1[i + 1] = answer
    if answer1 == []:
        contents = '''<!DOCTYPE html>
            <html>
            <head>
            <meta content = "text/html; charset = UTF-8"
            http-equip = "content-type">
            </head>
            <body>
            <center>
            <h3> No sent items found </h3>
            </center>
            </body>
            </html>
            '''
    else:
        contents = '''<!DOCTYPE html>
                <html>
                <head>
                <meta content = "text/html; charset = UTF-8"
                http-equip = "content-type">
                <style>
                td {
                    padding :0 15px;
                }
                </style>
                <title>Time Table</title>
                </head>
                <body>
                    <div class="card" id="generatePDF">

                <br><br>
                <center>
                <table border = 1>
                %s
                </table>
                <br><br>
                
                <button id="pdfButton"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzxA1IZaV_fN96xiySAwgY5iZiM-pIg9W9ig&usqp=CAU" style="height:30px;width:30px;"><b style="padding-bottom:5px;" class="text"> <center>&nbsp; &nbsp Download</center></b></button>
    
    </div>
    </center>
        <script>
        var button = document.getElementById("pdfButton");
        var makepdf = document.getElementById("generatePDF");
        button.addEventListener("click", function () {
            var mywindow = window.open("", "PRINT", "height=600,width=600");
            mywindow.document.write(makepdf.innerHTML);
            mywindow.document.close();
            mywindow.focus();
            mywindow.print();
            return true;
        });
    </script>

                </body>
                </html>
                ''' % (answer1)
    filename = 'demo36.html'

    def main(contents, filename):
        output = open(filename, "w")
        output.write(contents)
        output.close()
    main(contents, filename)
    webbrowser.open(filename)
    return render_template('demo3.html')

@app.route('/RecievedMail')
def RecievedMail():
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from admin"
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    text = []
    subject = []
    send = []
    key = []
    for i in records:
        if i[4] == g.c:
            subject.append(i[1])
            text.append(i[2])
            key.append(i[3])
            send.append(i[0])
    actualSub = []
    actualTxt = []
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = key[i]
        for i in subjectDecrypt:
            for j in i:
                sub += chr((k.index(j) + 65))
            sub += ' '
        for i in textDecrypt:
            for j in i:
                txt += chr((k.index(j) + 65))
            txt += ' '
        actualSub.append(sub)
        actualTxt.append(txt)
    
    answer = []
    tbl = "<tr><td>To</td><td>Subject</td><td>Text</td><td>From</td></tr>"
    answer1 = [0] * (len(text) + 1)
    answer1[0] = tbl
    for i in range(len(text)):
        answer = []
        a = "<tr><td>%s</td>" % g.c
        answer.append(a)
        a1 = "<td>%s</td>" % actualSub[i]
        answer.append(a1)
        a2 = "<td>%s</td>" % actualTxt[i]
        answer.append(a2)
        a3 = "<td>%s</td></tr>" % send[i]
        answer.append(a3)
        answer1[i + 1] = answer
    if answer1 == []:
        contents = '''<!DOCTYPE html>
            <html>
            <head>
            <meta content = "text/html; charset = UTF-8"
            http-equip = "content-type">
            </head>
            <body>
            <center>
            <h3> No Recieved items found </h3>
            </center>
            </body>
            </html>
            '''
    else:
        contents = '''<!DOCTYPE html>
                <html>
                <head>
                <meta content = "text/html; charset = UTF-8"
                http-equip = "content-type">
                <style>
                td {
                    padding :0 15px;
                }
                </style>
                <title>Time Table</title>
                </head>
                <body>
                    <div class="card" id="generatePDF">

                <br><br>
                <center>
                <table border = 1>
                %s
                </table>
                <br><br>
                
                <button id="pdfButton"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzxA1IZaV_fN96xiySAwgY5iZiM-pIg9W9ig&usqp=CAU" style="height:30px;width:30px;"><b style="padding-bottom:5px;" class="text"> <center>&nbsp; &nbsp Download</center></b></button>
    
    </div>
    </center>
        <script>
        var button = document.getElementById("pdfButton");
        var makepdf = document.getElementById("generatePDF");
        button.addEventListener("click", function () {
            var mywindow = window.open("", "PRINT", "height=600,width=600");
            mywindow.document.write(makepdf.innerHTML);
            mywindow.document.close();
            mywindow.focus();
            mywindow.print();
            return true;
        });
    </script>

                </body>
                </html>
                ''' % (answer1)
    filename = 'demo37.html'

    def main(contents, filename):
        output = open(filename, "w")
        output.write(contents)
        output.close()
    main(contents, filename)
    webbrowser.open(filename)
    return render_template('demo3.html')

app.run(debug=True)
